# -*- coding: utf-8 -*-

from fabric.api import run, sudo


def kernel_name():
    run('uname -a')


def install_git():
    sudo('apt-get install git')
