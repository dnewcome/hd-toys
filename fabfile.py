from fabric.api import local

def test():
    """ Run tests in the GAE environment """
    local("nosetests --with-gae --logging-level=ERROR")