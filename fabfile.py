from os.path import join
from contextlib import contextmanager
from fabric.api import local, run, env, put, prefix

package_folder = "blog"
version = local(
    """sed -E "s/__version__\s*=\s*['\\"]([0-9.]*)['\\"]/\\1/;tx;d;:x" {}/__init__.py""".format(
        package_folder),
    capture=True)
# Use ssh config from ~/.ssh/config
env.use_ssh_config = True
env.hosts = ['DO-Blog']
env.activate = 'source /var/local/blog/bin/activate'
env.local_config = "./production.yaml"
env.remote_config = "/var/local/blog/config.yaml"
env.package_name = "blog-{}.tar.gz".format
env.remote_setup = "/tmp/Blog-{}/setup.py".format
env.local_dist = "./dist"
env.remote_dir = "/tmp"


def remote_ls():
    run('ls')


def test():
    """
    Run the unittests.
    """
    local("nosetests -dv")


def update_version():
    """
    Parse the __init__ file, and prompt for an updated version number.
    """
    global version
    local("grep \"__version__ = '.*'\" blog/__init__.py")
    version = raw_input("New Version: ")
    command = (
        "sed -i \"s/__version__ = '.*'/__version__ = '{}'/\" blog/__init__.py"
        .format(version))
    local(command)


def package():
    """
    Create the package tarball.
    """
    local("python setup.py sdist")


def clean():
    """
    Delete the local package tarball.
    """
    local("rm -r {}".format(env.local_dist))


def push(local_path=None,
         remote_path=None):
    """
    Copy the tarball to the deployment server.
    """
    global version
    filename = env.package_name(version)
    if local_path is None:
        local_path = join(env.local_dist, filename)
    if remote_path is None:
        remote_path = join(env.remote_dir, filename)
    put(local_path, remote_path)


@contextmanager
def virtualenv():
    """
    Activate the virtual environment.
    """
    with prefix(env.activate):
        yield


def install():
    """
    Remotely install the package.
    """
    global version
    with virtualenv():
        run('pip install {}'.format(join(env.remote_dir,
                                         env.package_name(version))))


def install_setup():
    """
    Remotely unpagkage and install the package.
    """
    global version
    run("tar -C /tmp -xvf {}".format(join(env.remote_dir,
                                          env.package_name(version))))
    run("python {} install".format(env.remote_setup(version)))


def reload_nginx():
    """
    Reload the nginx server.
    """
    run('sudo service nginx reload')


def uwsgi_reload():
    """
    Reload the uwsgi server.
    """
    run("sudo uwsgi --reload /var/local/blog/blog.pid")


def push_config():
    """
    Copy the configuration to the remote server.
    """
    push(env.local_config, env.remote_config)


def deploy():
    """
    Test and deploy the package, and reload uwsgi to update it.
    """
    #test()
    update_version()
    package()
    push()
    clean()
    install()
    push_config()
    uwsgi_reload()
