#!/usr/bin/env python

import sys
import tempfile
import subprocess

def execute_shell(command):
    '''Execute shell line and return output'''
    splitted_command = command.split(' ')
    if sys.version_info[0] == 2:
        # two opens are required otherwise the read get an error
        fd_tmp_out, tmp_output = tempfile.mkstemp()
        with open(tmp_output, "wb") as f:
            ret = subprocess.call(splitted_command, stdout=f, stderr=subprocess.STDOUT)
        if ret != 0:
            raise RuntimeError('Bad shell command execution: ' + command)
        with open(tmp_output, "r") as f:
            output = ("".join(f.readlines())).strip().split('\n')
        return output
    else:
        refs = subprocess.check_output(splitted_command).decode('UTF-8').split('\n')
        refs.remove('')
        return refs
