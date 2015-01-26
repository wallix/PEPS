#! /usr/bin/env python3.4
# Author: Henri Chataing <chataing.henri@gmail.com>

import getpass, time
import ctypes

# from OpenSSL import SSL
import webbrowser, requests, json
from rauth import OAuth1Service, OAuth1Session
from flask import Flask, request, g
from multiprocessing import Process, Array, Manager

from utils import varconfig

########### SERVER CONFIGURATION ############

# Path to the server certificate.
verify = '../../data/server.crt'

# Verifier callback.
oauth_callback = 'http://localhost:5000/callback'

# Token verifier !
manager = Manager()
oauth_verifier = manager.Value(ctypes.c_char_p, '')

# Server configuration. Necessary to receive the verifier.
def run_server(oauth_verifier):
  app = Flask(__name__)
  @app.route('/callback')
  def callback():
    verifier = request.args.get('oauth_verifier')
    if verifier:
      oauth_verifier.value = verifier
    return 'Acquired verifier'
  app.run()

# Server object.
server = None
# Create new server if necessary, and start it.
def start_server():
  global server
  if server is None:
    oauth_verifier.value = ''
    server = Process(target=run_server, args=(oauth_verifier,))
  server.start()
# Terminate server and join.
def terminate_server():
  global server
  if not server is None:
    server.terminate()
    server.join()
    server = None

################ REST API ###################

# Internal Errors.
class ApiError(Exception):
  def __init__(self, code, method, error=None):
    self.code = code
    self.error = error
    self.method = method
  def __repr__(self):
    return 'ApiError({}, {}, {})'.format(self.code, self.method, repr(self.error))
  def __str__(self):
    return '{} <{}>: {}'.format(self.method, self.code, repr(self.error))

class WebmailApi:
  session = None
  # Precomputed API urls.
  _base_url = ''
  _upload_url = ''

  # The class "constructor" - It's actually an initializer
  def __init__(self, host='localhost', port='4443'):
    if port == '443' or port == '':
      self._base_url = 'https://{}/api/v0'.format(host, port)
      self._upload_url = 'https://{}/upload/api/v0'.format(host, port)
    else:
      self._base_url = 'https://{}:{}/api/v0'.format(host, port)
      self._upload_url = 'https://{}:{}/upload/api/v0'.format(host, port)

    consumer_key = varconfig('consumer_key', 'OAuth Consumer key: ', printval=False)
    consumer_secret = varconfig('consumer_secret', 'OAuth Consumer secret: ', printval=False)

    # Consumer key is undefined, switching to regular login.
    if consumer_key == '':
      username = input('PEPS Login: ')
      password = getpass.getpass('Password: ')
      data = {'username': username, 'password': password}
      headers = {'content-type': 'application/json'}
      res = requests.post('{}/login'.format(self._base_url), data=json.dumps(data), headers=headers, verify=verify)
      try:
        token = res.json()['token']
        self.session = OAuth1Session('', '', access_token=token, access_token_secret='')
        print('Api has been successfully configured')
      except Exception as err:
        print('Api: Configuration error: {}'.format(err))
        self.session = None

    # Consumer key has been provided, standard OAuth flow.
    else:
      peps = OAuth1Service(
        name='webmail-api-test',
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        request_token_url='{}/oauth/request_token'.format(self._base_url),
        access_token_url='{}/oauth/access_token'.format(self._base_url),
        authorize_url='{}/oauth/authorize'.format(self._base_url),
        base_url=self._base_url
      )

      print("---> Initiate OAuth1 connection")
      request_token, request_token_secret = peps.get_request_token(verify=verify, params={'oauth_callback': oauth_callback})

      print("---> Request token")
      authorize_url = peps.get_authorize_url(request_token, verify=verify, params={'oauth_callback': oauth_callback})

      print("---> Authorize token")
      print('Visit this URL in your browser: {url}'.format(url=authorize_url))

      webbrowser.open(authorize_url) # Authenticate the user.
      start_server() # Open the server to receive the verifier.
      # oauth_verifier = input('Enter oauth_verifier from browser: ')
      # Waiting for the token verifier...
      tries = 0
      while oauth_verifier.value == '' and tries < 30:
        time.sleep(1)
        tries = tries + 1
      terminate_server()
      if oauth_verifier.value == '':
        print('I waited too long for your password, now I am leaving...')
      else:
        print("---> Create session")
        self.session = peps.get_auth_session(
          request_token, request_token_secret,
          method='POST',
          verify=verify,
          params={'oauth_verifier': oauth_verifier.value},
          headers={'content-type': 'application/json'},  # These two things are necessary to
          data='{}'                                      # prevent rauth from using the body to pass the oauth tokens.
        )
        print('Api has been successfully configured !')

  # Intercept JSON parsing errors, as well as error status codes.
  def _extract(self, result, method):
    try:
      data = result.json()
      if result.status_code == 200:
        return data
      elif 'error' in data:
        raise ApiError(result.status_code, method, error=data['error'])
      else:
        raise ApiError(result.status_code, method)
    except ValueError:
      raise ApiError(result.status_code, method, error='Malformed response')

  ### Folders. ###

  # List folders.
  def folder_list(self):
    result = self.session.get('{}/users/me/folders'.format(self._base_url), verify=verify)
    return self._extract(result, 'folder.list')

  # Get single folder.
  def folder_get(self, id):
    result = self.session.get('{}/users/me/folders/{}'.format(self._base_url, id), verify=verify)
    return self._extract(result, 'folder.get')

  # Delete a folder.
  def folder_delete(self, id):
    result = self.session.delete('{}/users/me/folders/{}'.format(self._base_url, id), verify=verify)
    return self._extract(result, 'folder.delete')

  def folder_create(self, name):
    data = json.dumps({'name': name})
    result = self.session.post('{}/users/me/folders'.format(self._base_url), verify=verify, headers={'content-type': 'application/json'}, data=data)
    return self._extract(result, 'folder.create')

  def folder_update(self, id, newname):
    data = json.dumps({'name': newname})
    result = self.session.put('{}/users/me/folders/{}'.format(self._base_url, id), verify=verify, headers={'content-type': 'application/json'}, data=data)
    return self._extract(result, 'folder.update')

  ### Tags. ###

  # List folders.
  def tag_list(self):
    result = self.session.get('{}/users/me/tags'.format(self._base_url), verify=verify)
    return self._extract(result, 'tag.list')

  # Get single folder.
  def tag_get(self, id):
    result = self.session.get('{}/users/me/tags/{}'.format(self._base_url, id), verify=verify)
    return self._extract(result, 'tag.get')

  # Delete a folder.
  def tag_delete(self, id):
    result = self.session.delete('{}/users/me/tags/{}'.format(self._base_url, id), verify=verify)
    return self._extract(result, 'tag.delete')

  def tag_create(self, data):
    data = json.dumps(data)
    result = self.session.post('{}/users/me/tags'.format(self._base_url), verify=verify, headers={'content-type': 'application/json'}, data=data)
    return self._extract(result, 'tag.create')

  def tag_update(self, id, data):
    data = json.dumps(data)
    result = self.session.put('{}/users/me/tags/{}'.format(self._base_url, id), verify=verify, headers={'content-type': 'application/json'}, data=data)
    return self._extract(result, 'tag.update')

  ### Messages. ###

  def message_trash(self, id):
    result = self.session.post('{}/users/me/messages/{}/trash'.format(self._base_url, id), verify=verify, headers={'content-type': 'text/plain'}, data='')
    return self._extract(result, 'message.trash')

  def message_untrash(self, id):
    result = self.session.post('{}/users/me/messages/{}/untrash'.format(self._base_url, id), verify=verify, headers={'content-type': 'text/plain'}, data='')
    return self._extract(result, 'message.untrash')

  def message_delete(self, id):
    result = self.session.delete('{}/users/me/messages/{}'.format(self._base_url, id), verify=verify, headers={'content-type': 'text/plain'}, data='')
    return self._extract(result, 'message.delete')

  def message_get(self, id):
    result = self.session.get('{}/users/me/messages/{}'.format(self._base_url, id), verify=verify, headers={'content-type': 'text/plain'}, data='')
    return self._extract(result, 'message.get')

  def message_list(self, maxResults=None, pageToken=None, labelId='INBOX'):
    params = {'labelIds': labelId}
    if not maxResults is None:
      params['maxResults'] = maxResults
    if not pageToken is None:
      params['pageToken'] = pageToken
    result = self.session.get('{}/users/me/messages'.format(self._base_url), verify=verify, headers={'content-type': 'text/plain'}, params=params)
    return self._extract(result, 'message.list')

  def message_modify(self, id, change):
    data = json.dumps(change)
    result = self.session.post('{}/users/me/messages/{}/modify'.format(self._base_url, id), verify=verify, headers={'content-type': 'application/json'}, data=data)
    return self._extract(result, 'message.modify')

  def message_insert(self, upload_type, data, cte):
    ct = 'text/plain'
    if upload_type == 'media':
      ct = 'message/rfc822'
    elif upload_type == 'multipart':
      ct = 'application/json'
    else:
      print('Unrecognized upload type')
      return None
    result = self.session.post(
      '{}/users/me/messages'.format(self._upload_url),
      verify=verify,
      headers={'content-type': ct, 'content-transfer-encoding': cte},
      params={'uploadType': upload_type},
      data=data)
    return self._extract(result, 'message.insert')

  def message_attachment(self, id, attachment):
    result = self.session.get('{}/users/me/messages/{}/attachments/{}'.format(self._base_url, id, attachment), verify=verify, headers={'content-type': 'text/plain'}, data='')
    return self._extract(result, 'message.attachment')

  ### History. ###

  def message_history(self, startHistoryId, labelId=None, pageToken=None, maxResults=None):
    params = {'startHistoryId': startHistoryId}
    if labelId:
      params['labelId'] = labelId
    if pageToken:
      params['pageToken'] = pageToken
    if maxResults:
      params['maxResults'] = maxResults
    result = self.session.get('{}/users/me/history'.format(self._base_url), verify=verify, headers={'content-type': 'text/plain'}, params=params)
    return self._extract(result, 'message.history')

  ### Drafts. ###

  # def draft_insert(self):
  #   result = self.session.post('{}/users/me/drafts'.format(self._base_url), verify=verify, headers={'content-type': 'text/plain'})
  #   return result.json()

  def draft_delete(self, id):
    result = self.session.delete('{}/users/me/drafts/{}'.format(self._base_url, id), verify=verify, headers={'content-type': 'text/plain'})
    return self._extract(result, 'draft.delete')

  def draft_get(self, id):
    result = self.session.get('{}/users/me/drafts/{}'.format(self._base_url, id), verify=verify, headers={'content-type': 'text/plain'})
    return self._extract(result, 'draft.get')

  # def draft_list(self)
  #   result = self.session.get('{}/users/me/drafts/'.format(self._base_url), verify=verify, headers={'content-type': 'text/plain'})
  #   return result.json()

  # def draft_update(self, id)
  #   result = self.session.put('{}/users/me/drafts/'.format(self._base_url), verify=verify, headers={'content-type': 'text/plain'})
  #   return result.json()

  def draft_send(self, id):
    data = json.dumps({'id': id})
    result = self.session.post('{}/users/me/drafts/send'.format(self._base_url), verify=verify, headers={'content-type': 'application/json'}, data=data)
    return self._extract(result, 'message.send')

  ### Users. ###

  def user_get(self, key, format='full'):
    result = self.session.get('{}/users/{}'.format(self._base_url, key), verify=verify, headers={'content-type': 'text/plain'}, data='', params={'format': format})
    return self._extract(result, 'user.get')

  def user_update(self, key, fullname, level, status='lambda'):
    data = json.dumps({'fullname': fullname, 'level': level, 'status': status})
    result = self.session.put('{}/users/{}'.format(self._base_url, key), verify=verify, headers={'content-type': 'application/json'}, data=data)
    return self._extract(result, 'user.update')

  def user_move(self, key, added_teams=[], removed_teams=[]):
    data = json.dumps({'addedTeamKeys': added_teams, 'removedTeamKeys': removed_teams})
    result = self.session.put('{}/users/{}/move'.format(self._base_url, key), verify=verify, headers={'content-type': 'application/json'}, data=data)
    return self._extract(result, 'user.move')

  def user_delete(self, key):
    result = self.session.delete('{}/users/{}'.format(self._base_url, key), verify=verify, headers={'content-type': 'text/plain'}, data='')
    return self._extract(result, 'user.delete')

  def user_insert(self, firstName, lastName, username, password, level=1, teams=[]):
    data = json.dumps({
      'firstName': firstName, 'lastName': lastName, 'username': username,
      'password': password, 'level': level, 'teams': teams
    })
    result = self.session.post('{}/users'.format(self._base_url), verify=verify, headers={'content-type': 'application/json'}, data=data)
    return self._extract(result, 'user.insert')

  # Fixme: teamKeys can only take one argument at present, else signature is wrong.
  def user_list(self, maxResults=None, pageToken=None, teamKeys=None):
    # Request takes care of None-valued parameters, as well as value lists.
    params = {}
    if not maxResults is None:
      params['maxResults'] = maxResults
    if not pageToken is None:
      params['pageToken'] = pageToken
    if not teamKeys is None:
      params['teamKeys'] = teamKeys
    result = self.session.get('{}/users'.format(self._base_url), verify=verify, headers={'content-type': 'text/plain'}, data='', params=params)
    return self._extract(result, 'user.list')

  def user_history(self, startHistoryId, maxResults=None):
    params = {'startHistoryId': startHistoryId, 'maxResults': maxResults}
    # if maxResults:
    #   params['maxResults'] = maxResults
    result = self.session.get('{}/users/history'.format(self._base_url), verify=verify, headers={'content-type': 'text/plain'}, params=params)
    return self._extract(result, 'user.history')

  ### Teams. ###

  def team_get(self, key):
    result = self.session.get('{}/teams/{}'.format(self._base_url, key), verify=verify, headers={'content-type': 'text/plain'})
    return self._extract(result, 'user.get')

  def team_insert(self, name, parent=None, description=''):
    data = {'name':  name, 'description': description, 'parent': parent}
    if parent is None:
      data['parent'] = {'none': {}}
    else:
      data['parent'] = {'some': parent}
    data = json.dumps(data)
    result = self.session.post('{}/teams'.format(self._base_url), verify=verify, headers={'content-type': 'application/json'}, data=data)
    return self._extract(result, 'team.insert')

  def team_update(self, key, name, description):
    data = json.dumps({'name': name, 'description': description})
    result = self.session.put('{}/teams/{}'.format(self._base_url, key), verify=verify, headers={'content-type': 'application/json'}, data=data)
    return self._extract(result, 'team.update')

  def team_delete(self, key):
    result = self.session.delete('{}/teams/{}'.format(self._base_url, key), verify=verify, headers={'content-type': 'text/plain'})
    return self._extract(result, 'team.delete')

  def team_list(self):
    result = self.session.get('{}/teams'.format(self._base_url), verify=verify)
    return self._extract(result, 'team.list')

  def team_history(self, startHistoryId, maxResults=None):
    params = {'startHistoryId': startHistoryId}
    if maxResults:
      params['maxResults'] = maxResults
    result = self.session.get('{}/teams/history'.format(self._base_url), verify=verify, headers={'content-type': 'text/plain'}, params=params)
    return self._extract(result, 'team.history')

  ### Files ###

  def file_get(self, path):
    result = self.session.get('{}/files/{}'.format(self._upload_url, path), verify=verify, headers={'content-type': 'text/plain'})
    return self._extract(result, 'file.get')

  def file_metadata(self, path, list=False, file_limit=10000):
    params = {'list': list, 'file_limit': file_limit}
    result = self.session.get('{}/files/metadata/{}'.format(self._base_url, path), verify=verify, headers={'content-type': 'text/plain'}, data='', params=params)
    return self._extract(result, 'file.metadata')

  def file_upload(self, path, data, mimetype, cte):
    # params = {'list': list, 'file_limit': file_limit}
    headers = {
      'content-type': mimetype,
      'content-transfer-encoding': cte
    }
    result = self.session.post('{}/files_put/{}'.format(self._upload_url, path), verify=verify, headers=headers, data=data)
    return self._extract(result, 'file.upload')

  def file_move(self, from_path, to_path, root=''):
    headers = {'content-type': 'text/plain'}
    params = {'from_path': from_path, 'to_path': to_path, 'root': root}
    result = self.session.post('{}/fileops/move'.format(self._base_url), verify=verify, headers=headers, params=params)
    return self._extract(result, 'file.move')

  def file_copy(self, from_path, to_path, root=''):
    headers = {'content-type': 'text/plain'}
    params = {'from_path': from_path, 'to_path': to_path, 'root': root}
    result = self.session.post('{}/fileops/copy'.format(self._base_url), verify=verify, headers=headers, params=params)
    return self._extract(result, 'file.copy')

  def file_delete(self, path):
    headers = {'content-type': 'text/plain'}
    params = {'path': path}
    result = self.session.post('{}/fileops/delete'.format(self._base_url), verify=verify, headers=headers, params=params)
    return self._extract(result, 'file.delete')
