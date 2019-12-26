from OpenSSL import crypto
from pymaid.conf import settings

from core import g


def preload_crypto_data():
    stack = g.crypto_stack = crypto._lib.sk_X509_new_null()
    root_cert = settings.get('ROOT_CERT', ns='crypto')
    ca_cert = settings.get('CA_CERT', ns='crypto')
    server_cert = settings.get('SERVER_CERT', ns='crypto')
    server_key = settings.get('SERVER_KEY', ns='crypto')
    assert root_cert and ca_cert and server_cert and server_key, \
        (root_cert, ca_cert, server_cert, server_key)

    for cert in (root_cert, ca_cert):
        with open(cert) as fp:
            cert = crypto.load_certificate(crypto.FILETYPE_PEM, fp.read())
            crypto._lib.sk_X509_push(stack, cert._x509)

    with open(server_cert) as fp:
        g.crypto_cert = crypto.load_certificate(crypto.FILETYPE_PEM, fp.read())
    with open(server_key) as fp:
        g.crypto_key = crypto.load_privatekey(crypto.FILETYPE_PEM, fp.read())


def preload():
    preload_crypto_data()
