#! /usr/bin/env python3.4
# Author: Henri Chataing <chataing.henri@gmail.com>

import unittest

from webmail import WebmailApi, ApiError
from utils import srandom

class ApiTest(unittest.TestCase):

  @classmethod
  def setUpClass(self):
    self._api = WebmailApi()

  def test_folder(self):
    foldername = srandom(10)
    folder = self._api.folder_create(foldername)
    folderid = folder['id']
    self.assertEqual(foldername, folder['name'])
    # Can not create two folders with same name.
    self.assertRaises(ApiError, self._api.folder_create, foldername)
    # Folder get should return same folder.
    folderget = self._api.folder_get(folderid)
    self.assertEqual(folderid, folderget['id'])
    self.assertEqual(foldername, folderget['name'])
    # Deletion should succeed.
    self.assertEqual(self._api.folder_delete(folderid), {})
    # Second deletion should fail.
    self.assertRaises(ApiError, self._api.folder_delete, folderid)

  # TODO: history not included.
  def test_team(self):
    teamname = srandom(10)
    teamkey = self._api.team_insert(teamname)
    # Can not create two teams with same name.
    self.assertRaises(ApiError, self._api.team_insert, teamname)
    # Team get should return same team.
    teamget = self._api.team_get(teamkey)
    self.assertEqual(teamname, teamget['name'])
    self.assertEqual(teamkey, teamget['key'])
    # Renaming the team should succeed.
    self._api.team_update(teamkey, teamname+'-upd', 'update')
    teamget = self._api.team_get(teamkey)
    self.assertEqual(teamname+'-upd', teamget['name'])
    self.assertEqual('update', teamget['description'])
    # The team should be in the returned list.
    teamlist = self._api.team_list()
    self.assertTrue(teamkey in teamlist)
    # Deletion should succeed.
    self.assertEqual(self._api.team_delete(teamkey), {})
    # Later access should fail.
    self.assertRaises(ApiError, self._api.team_get, teamkey)
    # Second deletion should fail.
    self.assertRaises(ApiError, self._api.team_delete, teamkey)

  # TODO: history not included.
  def test_user(self):
    username = srandom(10)
    user = self._api.user_insert('Alpha', 'Beta', username, 'password')
    userkey = user['key']
    self.assertEqual(user['first_name'], 'Alpha')
    self.assertEqual(user['last_name'], 'Beta')
    self.assertEqual(user['username'], username)
    # Can not create two users with same name.
    self.assertRaises(ApiError, self._api.user_insert, 'A', 'B', username, 'password')
    # Test structure of return value, for differing formats.
    full = self._api.user_get(userkey, format='full')
    minimal = self._api.user_get(userkey, format='minimal')
    for field in ['status', 'creator', 'created', 'edited', 'teams', 'level', 'picture', 'sgn', 'blocked', 'salt']:
      self.assertIn(field, full)
      self.assertNotIn(field, minimal)
    for field in ['key', 'username', 'first_name', 'last_name', 'email']:
      self.assertIn(field, full)
      self.assertIn(field, minimal)
    # Check some values.
    self.assertEqual(full['username'], username)
    self.assertEqual(full['email']['address']['local'], username)
    # Update the user and check.
    self._api.user_update(userkey, 'AA BB', 10, status='admin')
    full = self._api.user_get(userkey)
    self.assertEqual(full['level'], 10)
    self.assertEqual(full['status'], {'admin': {}})
    # Update the teams and check.
    team0 = self._api.team_insert(srandom(10))
    team1 = self._api.team_insert(srandom(10))

    self._api.user_move(userkey, added_teams=[team0, team1], removed_teams=[])
    full = self._api.user_get(userkey)
    self.assertEqual(full['teams'].sort(), [team0, team1].sort())

    self._api.user_move(userkey, added_teams=[team0], removed_teams=[team1])
    full = self._api.user_get(userkey)
    self.assertEqual(full['teams'], [team0])

    self._api.user_move(userkey, added_teams=[team0, team1], removed_teams=[])
    full = self._api.user_get(userkey)
    self.assertEqual(full['teams'].sort(), [team0, team1].sort())

    self._api.team_delete(team0)
    self._api.team_delete(team1)
    # Deletion should succeed.
    self.assertEqual(self._api.user_delete(userkey), {})
    # Later access should fail.
    self.assertRaises(ApiError, self._api.user_get, userkey)
    # Second deletion should fail.
    self.assertRaises(ApiError, self._api.user_delete, userkey)

# Launch the tests.
if __name__ == "__main__":
  unittest.main()
