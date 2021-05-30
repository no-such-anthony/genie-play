# username: "%CALLABLE{mylib_callable.env_or_ask(username)}"
# password: "%CALLABLE{mylib_callable.env_or_ask(password)}"
# https://pubhub.devnetcloud.com/media/pyats/docs/topology/creation.html

import os

def env_or_ask(a):
    return f"%ASK{{{a.capitalize()}}}" if f'PYATS_{a.upper()}' not in os.environ else f"%ENV{{PYATS_{a.upper()}}}"
