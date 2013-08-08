from contextlib import contextmanager
from fabric.api import local, run, env, put, prefix

# Use ssh config from ~/.ssh/config
env.use_ssh_config = True
env.hosts = ['DO-Blog']
env.activate = 'source /var/local/virtualenvs/Blog/bin/activate'
env.remote_tar = "/tmp/tar-name"
env.local_dist = "./dist"
env.local_tar = "./dist/tar-name"



def test():
    local("nosetests -dv")


def remote_id():
    run("id")


def package():
    local("python setup.py sdist")


def clean():
    local("rm -r {}".format(env.local_dist))


def push(local_path=env.local_tar,
         remote_path=env.remote_tar):
    put(local_path, remote_path)


@contextmanager
def virtualenv():
    with prefix(env.activate):
        yield


def install():
    with virtualenv():
        run('pip install {}'.format(env.remote_tar))


def deploy():
    test()
    package()
    push()
    clean()
    install()
