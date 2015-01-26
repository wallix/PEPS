#! /usr/bin/env python3.4
# Author: Henri Binsztok <niceisnice@gmail.com>

# cf. http://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console

import os, sys, getopt, argparse
import re, getpass
import time
from queue import Queue
import tokenize
import unittest

import imaplib, requests, mimetypes
imaplib._MAXLINE = 40000

import email, json
import chardet, base64, quopri

from email.parser import HeaderParser
from email.header import decode_header
hparser = HeaderParser()
email_pattern = re.compile(r'\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}\b', re.IGNORECASE)

from rauth import OAuth1Service, OAuth1Session
from flask import Flask, request, g
from multiprocessing import Process, Array, Manager
import ctypes

# from OpenSSL import SSL
import webbrowser

from utils import varconfig, timed
from webmail import WebmailApi, ApiError

######### GENERAL CONFIGURATION #############

CHARDET_MINCONF = 0.8
QP_SUPPORTED = False

################ MAIL IMPORT ################

# Argument parser.
parser = argparse.ArgumentParser(description='Import mails to PEPS.')
parser.add_argument(
  '-c', '--cmax',
  metavar='cmax', type=int, nargs='?', const=None, default=None,
  help='the number of mails to import (all by default)')
parser.add_argument(
  '-b', '--box',
  metavar='cmax', nargs='*', default=['inbox'],
  help='specifies boxes to import (defaults to "inbox")')

# Establish connection with IMAP server.
def imap():
  server = varconfig('imap_server', 'IMAP server: ')
  address = varconfig('mail_address', 'Address: ')
  password = getpass.getpass('Password: ')
  mail = imaplib.IMAP4_SSL(server)
  mail.login(address, password)
  return mail

# Decode an incoming byte string (guessing the encoding using chardet), and
# encode it again in a request compatible string (latin-1).
def _decode(raw):
  enc = chardet.detect(raw) # Detect encoding.
  data = ''
  cte = 'binary'
  if enc['encoding'] != 'ascii' and enc['encoding'] != 'latin-1':
    if QP_SUPPORTED:
      data = quopri.encodestring(raw).decode('latin-1')
      cte = 'quotable-printable'
    else:
      data = base64.b64encode(raw).decode('latin-1')
      cte = 'base64'
  else:
    data = raw.decode(enc['encoding'])
  return data, cte

# Retrieve the latest mail in the box and uploads it through the API.
# @param cmax the number of mails to upload. If None, all the mails are imported.
def upload_box(mail, api, cmax=None):
  result, data = mail.search(None, "ALL")
  if result == 'OK':
    ids = data[0].split() # Ids is a space separated string.
    ids.reverse()
    if cmax is None:
      cmax = len(ids)
    else:
      cmax = min(cmax, len(ids))
    i = 0
    tfetch = 0
    tupload = 0
    print('0.0 %', end='')
    for id in ids[:cmax]:
      # Fetch raw message.
      (result, data), elapsed = timed(mail.fetch, id, "(RFC822)") # fetch the email body (RFC822) for the given ID.
      tfetch += elapsed
      # Encode.
      raw = data[0][1] # Raw mail, in bytes.
      data, cte = _decode(raw)
      # Upload into API.
      try:
        result, elapsed = timed(api.message_insert, 'media', data, cte)
        tupload += elapsed
      except ApiError as err:
        print('\nFailed to upload one message: {}\n'.format(err))
      # Progress.
      i = i+1
      percent = i * 100 / cmax
      print('\r\033[0K{0:.2f} %'.format(percent), end='')
    print('\r\033[0KDone.\n-- fetch time: {}\n-- upload time {}'.format(tfetch, tupload))
  else:
    print('Could not access the mail box: {}'.format(result))

# Upload the last mail the given number of times (performance test).
def upload_test(mail, api, cmax=None):
  result, data = mail.search(None, "ALL")
  cmax = cmax or 1000
  if result == 'OK':
    ids = data[0].split() # Ids is a space separated string.
    result, data = mail.fetch(ids[-1], "(RFC822)") # fetch the email body (RFC822) for the last mail ID.
    raw = data[0][1] # Raw mail, in bytes.
    data, cte = _decode(raw)

    print('0.0 %', end='')
    for i in range(cmax):
      # Upload into Api.
      api.message_insert('media', data, cte)
      # Progress.
      i = i+1
      percent = i * 100 / cmax
      print('\r\033[0K{0:.2f} %'.format(percent), end='')
    print('\r\033[0KDone.')
  else:
    print('Could not access the mail box: {}'.format(result))

# Run either of the commands.
def _run(argv, func):
  try:
    args = parser.parse_args(argv)
    mail = imap()
    api = WebmailApi()
    boxes = args.box
    cmax = args.cmax
    for box in boxes:
      print('Uploading "{}"'.format(box))
      mail.select(box)
      func(mail, api, cmax=cmax)
  except imaplib.IMAP4.error:
    print('Unable to establish connection with the server')
    return None

# Parse command line arguments.
def upload(argv):
  _run(argv, upload_box)

# Run an upload test.
def test(argv):
  _run(argv, upload_test)

############### FILE IMPORT #################

# Upload the contents of a local folder through the file API.
def upload_dir(path, where, api, rec=False):
  # Contains the list of files to upload.
  queue = Queue()
  # Pop an element from the queue, and deal with it.
  def upload(rec):
    (path, where) = queue.get()
    if os.path.isdir(path) and rec:
      files = os.listdir(path=path)
      for f in files:
        queue.put((path+'/'+f, where+'/'+f))
    elif os.path.isfile(path):
      try:
        mimetype, encoding = mimetypes.guess_type(path)
        mimetype = mimetype or 'application/octet-stream'
        raw = open(path, mode='rb').read()
        data, cte = _decode(raw)
        api.file_upload(where, data, mimetype, cte)
      except Exception as err:
        print('Failed to upload file {}: {}'.format(path, err))
  # Initialize the queue, and lauch the loop.
  queue.put((path, where))
  upload(True)
  while not queue.empty():
    upload(rec)

#############################################

# cf. http://www.tutorialspoint.com/python/python_command_line_arguments.htm
def main(argv):
  command = ''
  try:
    opts, args = getopt.getopt(argv, 'hc:')
  except getopt.GetoptError:
    help(2)
  for opt, arg in opts:
    if opt == '-h':
       help(0)
    elif opt in ("-c"):
      command = arg
  if command == 'unseen' or command == 'allto' or command == 'getone' or command == 'import':
    run(command)

if __name__ == "__main__":
  if not sys.argv[1:]:
    print('Please enter a command.\n  Accepted commands are: import, test')
  else:
    command, *argv = sys.argv[1:]
    if command == 'import':
      upload(argv)
    elif command == 'test':
      test(argv)
    else:
      print('Unknown command "{}".\n  Accepted commands are: import, test'.format(command))
