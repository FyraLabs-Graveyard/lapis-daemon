metadata = {
    'name': 'Mock',
    'description': 'RPM Mock builder support'
}
from typing import ChainMap
from git import config
import mockbuild.external
import mockbuild.util
# import lapis.logger as logger
import git
import os

# It's 2021 and Mock still doesn't have a python interface. And it's literally written in Python.
# So we're using the shell to do the dirty work because fuck you.

# The closest we have to a python interface for mock is the mock.util.run() function, which is literally a shell wrapper.

link = 'https://copr-be.cloud.fedoraproject.org/results/cappyishihara/ultramarine/fedora-35-x86_64/02957818-qogir-theme/qogir-theme-git020821-1.fc35.src.rpm'

def init(buildroot):
    # run mock init
    mockbuild.util.run('mock -r %s --rootdir %s --init' % (buildroot[config], buildroot))

# reminder to self: require mock-scm for git support

# git clone function
# requires python3-GitPython
def git_clone(url,path):
    # do a recursive clone
    # use gitpython
    git.Repo.clone_from(url, path, depth=1, recursive=True)
    # print output
    print('Cloned %s to %s' % (url, path))

def build_git(url ,clonepath, buildroot, path='/var/lib/mock/lapis', outdir='result', subdir=None):
    """
    Arguments:
    url -- the git url
    clonepath -- the path to clone the git repo to
    buildroot -- the path to the mock buildroot
    path -- the path to the mock repo
    outdir -- the path to the output SRPM directory
    subdir -- the path to the subdirectory to build in
    """
    try:
        git_clone(url,clonepath) #
        # except if the repo is already cloned
    except git.exc.GitCommandError as e:
        print(e)
    try:
        command = 'mock'

        if subdir is not None:
            # add cd clonepath + <subdir> && before the command
            command = 'cd %s/%s &&' % (clonepath, command)

        args = [
            '-r', buildroot,
            '--rootdir', path,
            '--resultdir', outdir,
            '--buildsrpm '
            # find the spec file in the clonepath, then pass it to mock as an absolute path
            '--spec $(readlink -f $(find %s -name *.spec))' % clonepath,
            # --source is basename of the spec file
            '--source $(dirname $(readlink -f $(find %s -name *.spec)))' % clonepath,
            # Enable network building by default
            '--enable-network'
        ]
        cmd = ' '.join([command] + args)
        print('running ' + cmd)
        mockbuild.util.run(cmd)
    except mockbuild.external.CommandError as e:
        print(e)

build_git(
'https://gitlab.ultramarine-linux.org/dist-pkgs/budgie-desktop/budgie-desktop-view.git',
'/tmp/budgie-desktop-view',
'fedora-35-x86_64',
'/var/lib/mock/lapis',
'result'
)