import pathlib
import http_session_file
from knappe.testing import DictSource
from knappe.auth import WSGISessionAuthenticator
from knappe.middlewares import auth
from knappe.middlewares.session import HTTPSession
from knappe_example.app import Application


authentication = auth.Authentication(
    authenticator=WSGISessionAuthenticator([
        DictSource({"admin": "admin"})
    ]),
    filters=(
        auth.security_bypass({"/login"}),
        auth.secured(path="/login")
    )
)

session = HTTPSession(
    store=http_session_file.FileStore(pathlib.Path('./session'), 300),
    secret='secret',
    salt='salt',
    cookie_name='session',
    secure=False,
    TTL=300
)


app = Application(middlewares=(session, authentication))


if __name__ == "__main__":
    import bjoern
    bjoern.run(app, "127.0.0.1", 8000)
