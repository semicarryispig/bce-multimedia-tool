"""
Media auth plugin for HTTPie.

"""
import os
import sys

from httpie import ExitStatus
from httpie.plugins import AuthPlugin
from httpie.compat import bytes
from mediaauth import MediaAuth


KEY = 'ACCESS_KEY_ID'
SECRET = 'SECRET_ACCESS_KEY'


class BytesHeadersFriendlyMediaAuth(MediaAuth):
    """
    extends MediaAuth
    """
    def __call__(self, r):
        for k, v in r.headers.items():
            if isinstance(v, bytes):
                r.headers[k] = v.decode('utf8')
        return super(BytesHeadersFriendlyMediaAuth, self).__call__(r)


class MediaAuthPlugin(AuthPlugin):
    """
    media auth plugin
    """
    name = 'media auth'
    auth_type = 'media'
    description = ''
    auth_require = False
    prompt_password = True

    def get_auth(self, username=None, password=None):
        """
        get auth
        """
        access_key = os.environ.get(KEY) if username is None else username
        secret = os.environ.get(SECRET) if password is None else password
        if not access_key or not secret:
            missing = []
            if not access_key:
                missing.append(KEY)
            if not secret:
                missing.append(SECRET)
            sys.stderr.write(
                'httpie-media-auth error: missing {1}\n'
                    .format(self.name, ' and '.join(missing))
            )
            sys.exit(ExitStatus.PLUGIN_ERROR)

        return BytesHeadersFriendlyMediaAuth(access_key, secret)
