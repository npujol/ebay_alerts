from six.moves.urllib.parse import urlparse


def get_relative_url(absolute_uri):
    return urlparse(absolute_uri).path
