#! /usr/bin/env python3.4
# Author: Henri Chataing <chataing.henri@gmail.com>

import time, random, string

# Import script configuration.
try:
  import config
except:
  config = None

# Time a function execution.
def timed(fun, *args, **kwargs):
  start = time.process_time()
  result = fun(*args, **kwargs)
  elapsed = time.process_time() - start
  return result, elapsed

# Access configuration variables.
def varconfig(name, prompt, printval=True):
  try:
    var = eval('config.{}'.format(name))
    if printval:
      print('{}{}'.format(prompt, var))
    return var
  except:
    return input(prompt)

# Return a random string.
def srandom(length):
  try:
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))
  except:
    return '[random:{}]'.format(length)
