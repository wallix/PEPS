% IMAP import tool

# Introduction

The python script [imap.py](https://github.com/MLstate/applications/blob/alpha/webmail/import-tool/imap.py) implements a binding to the REST api of webmail, as well as helper functions to import
existing mail boxes using IMAP protocol.

# Sample usage

    ./imap.py upload -c 1000

# Configuration

Configuration is put in a python script `config.py` in the same directory, with the following variables defined:

``` python
# IMAP
imap_server = 'imap.gmail.com'
mail_address = 'ann.onymous@gmail.com'

# OAuth
consumer_key = '123'
consumer_secret = '456'
```

All the fields are optional, and undefined values will be prompted at runtime.

# Command line

API functions can be manually accessed through the Python console as well. To launch the console:
``` bash
python3 -i imap.py
```
If the configuration file `config.py` is present, its values will be imported. API methods are accessed through a WebmailAPI object, which manages the connection parameters and pre-formats some of the requests' inputs.
For example:
```
>>> webmail = WebmailApi()
..
>>> webmail.folder_list()
[{'name': 'Inbox', 'id': 'INBOX'}, {'name': 'Starred', 'id': 'STARRED'}, ...]
```

WebmailApi() implements two distinct methods of connecting to the API:

* If you possess a pair of `consumer_key`, `consumer_secret`, you can either add them to `config.py` or enter them as requested. The connection will then follow the standard OAuth1 connection flow.
* Else, you can connect to PEPS using your usual `username` and `password`, as requested by a prompt.

The created object can be used exactly the same after the initial configuration.

# Dependencies

Install Python3 and dependencies: chardet, rauth and flask. For instance, on OSX:

```bash
brew install python3
pip3 install chardet rauth flask
```
