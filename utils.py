# Script to automate the installation of various components needed to report
# memory bandwidth
# Author: Sudipto Biswas (sbiswas7@in.ibm.com)

import getpass
import subprocess
import os
import sys
import time

# Install PcP


class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, new_path):
        self.new_path = os.path.expanduser(new_path)

    def __enter__(self):
        self.saved_path = os.getcwd()
        if self.saved_path != self.new_path:
            os.chdir(self.new_path)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.saved_path)


class su:
    """Context manager executing commands with a certain user"""
    def __init__(self, user):
        self.new_user = user

    def __enter__(self):
        self.curr_user = getpass.getuser()
        if self.curr_user != self.new_user:
            p = subprocess.Popen("su " + self.new_useruser,
                                 stdout=subprocess.PIPE, shell=True)
            p.communicate()

    def __exit__(self, etype, value, traceback):
        if self.curr_user != self.new_user:
            p = subprocess.Popen("su " + self.curr_user,
                                 stdout=subprocess.PIPE, shell=True)
            p.communicate()


class helper:
    @staticmethod
    def pack_exists(pack):
        if os.path.exists("/usr/bin/" + pack):
            return True

    @staticmethod
    def execute_command(command, need_sleep=None):
        try:
            p = subprocess.Popen(command,
                                 stdout=subprocess.PIPE, shell=True)
            if need_sleep:
                time.sleep(need_sleep)
            out, err = p.communicate()
            if err:
                print "Error while executing %s: %s" % (command, err)
            return out
        except OSError:
            print "Could not execute: %s" % command

    @staticmethod
    def git_clone(path, directory=None, branch=None):
        if directory:
            if os.path.isdir(directory):
                input = raw_input("The git directory exists."
                                  "Want to delete? : (Y/N)")
                if input == "Y":
                    helper.execute_command("rm -rf " + directory, 2)
                else:
                    print "Sorry, cannot proceed, "
                    "please delete the directory %s manually" % directory
                    sys.exit()

        if helper.pack_exists("git") and branch:
            helper.execute_command("git clone -b " + branch + " " + path)
        else:
            print "Please install git before proceeding"
            sys.exit()

    @staticmethod
    def git_checkout_specific_files(repo, path_files_dict):
        base_command = "git archive --remote=" + repo + " HEAD:"
        if helper.pack_exists("git"):
            for path, filename in path_files_dict.iteritems():
                full_command = base_command + path + " " + filename
                helper.execute_command(full_command)
