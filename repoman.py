#! /usr/bin/env python

"""
copyright (c) 2014 by Nixarus. See LICENSE for more details.
Created by Nixarus. [http://www.nixarus.com]
"""

import configparser
import subprocess
import os
import sys
from collections import OrderedDict


REPOPATH = "/etc/yum.repos.d"
REPOFILE = "redhat.repo"


if sys.version_info[0] < 3:
    input = raw_input


class RepoManager(object):

    def __init__(self):
        self.actions = ["Enable", "Disable"]
        self.confirm = ["Yes", "No"]
        self.repofile = self.get_repofile()


    def get_repofile(self):
        """search the filesystem to look for the repo file"""

        if os.path.isdir(REPOPATH):
            try:
                os.chdir(REPOPATH)
            except OSError:
                print("Yum repository path does not exist. Please ensure this is a RHEL or RHEL variant system")
                sys.exit(0)

        if os.path.isfile(REPOFILE):
            return REPOFILE
        else:
            print("Repository file does not exist. Please confirm this is a RHEL system")
            sys.exit(0)


    def parse_repofile(self):
        """Returns an id formated dictionary of available repository names"""
        
        if self.repofile:
            config = configparser.ConfigParser()
            config.read(self.repofile)
            available_repos  = config.sections()
            repo_dict = OrderedDict()

            for index, item in enumerate(available_repos):
                repo_dict.update({str(index + 1):item})
            return repo_dict


    def display_available_repos(self, repodict, header=True):
        
        if header:
            subprocess.call('clear',shell=True)
            print("\nWelcome to RepoMan, these are your available repositories: ")
            print("#"*58)
        if repodict:
            print("#\t\tRepository Name")
            for k in repodict.keys():
                print(str(k)+"\t\t"+repodict[k])
            print("\nPlease press cntrl+c at any point to exit")
            print("\n\n")

    def display_confirmation(self, repolist):
        for repo in repolist:
            print("(X)\t\t"+repo)
            
        
    def start_shell(self):
        sysrepofiles = self.parse_repofile()
        if sysrepofiles:
            self.display_available_repos(sysrepofiles)
            while True:
                user_action = input("What repository action would you like to perform? " + str(self.actions) + ": ")
                if user_action.lower() in [i.lower() for i in self.actions]:
                    break
                else:
                    print("Please type your option: enable or disable")

            while True:
                user_options = input("Please provide the repository numbers, seperated by comma: ")
                if user_options:
                    id_list = user_options.split(',')
                    actionable_repos = []
                    for id in id_list:
                        if id in sysrepofiles.keys():
                            actionable_repos.append(sysrepofiles[id])
                        else:
                            print("'"+str(id)+"' is an Invalid input")
                    if actionable_repos:
                        break

            while True:

                print("-"*25+"Valid Repos"+"-"*30)
                self.display_confirmation(actionable_repos)
                user_confirm = input("We should " + user_action + " the above repo(s) only? " + str(self.confirm) + ": ")
                if user_confirm.lower() in [i.lower() for i in self.confirm]:
                    if user_confirm.lower() =="yes":
                        self.process_request(user_action, actionable_repos)
                        break
                    else:
                        sys.exit(0)
        else:
            print("Sorry we could not find any repository listed")
            print("Please register the system with (Certificate-based) RHN and run yum repolist")
            print("\n\n")
            sys.exit(0)


    def process_request(self, action, repolist):
        if action.lower() == "enable":
            continous_form = "Enabling"
        if action.lower() == "disable":
            continous_form = "Disabling"

        print("\n")
        print("Processing repositories. Please wait, this might take some time...")
        print("-"*66)
        print("\n")        

        for repo in repolist:
            print(continous_form+" the " + repo + " repository")
            es = subprocess.call('subscription-manager repos --'+action+" "+repo , shell=True)
            if es != 0:
               print("\nSomething went wrong.\nPlease confirm this is a RHEL 6 or 7 based System. Thank you.")
            print("--\n")

        print("Done!")

def main():
    rm = RepoManager()
    rm.start_shell()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram is exiting...")
