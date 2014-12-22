#! /usr/bin/env python3

"""
copyright (c) 2014 by Nixarus.
See LICENSE for more details.

Created by Nixarus. [http://www.nixarus.com]
"""

import configparser
import subprocess
import sys
import os
from collections import OrderedDict


REPOPATH = "/etc/yum.repos.d"
REPOFILE = "redhat.repo"

class RepoManager(object):
    
    def __init__(self):

        self.actions = ["Enable", "Disable"]
        self.confirm = ["Yes", "No"]
        self.repofile = self.getRepoFile()

    def getRepoFile(self):
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


    def parseRepoFile(self):
        """Returns an id formated dictionary of available repository names"""

        if self.repofile:
            config = configparser.ConfigParser()
            config.read(self.repofile)
            available_repos  = config.sections()
            
            repo_dict = OrderedDict()
            i = 1

            for item in available_repos:
                repo_dict.update({str(i):item})
                i=i+1
            return repo_dict

    
    def id_to_repolist(self, string_of_id):
        if string_of_id:
            return string_of_id.split(',')


    def display_available_repo(self, repodict, header=True):
        
        if header:
            subprocess.call('clear',shell=True)
            print("\nWelcome to RepoMan, these are your available repositories: ")
            print("###########################################################\n")
        
        if repodict:
            print("#\t\tRepository Name")
            for k in repodict.keys():
                print(str(k)+"\t\t"+repodict[k])
            
            print("\nPlease press cntrl+c at any point to exit")
            print("\n\n")

    def display_confirmation(self, repolist):
    
        for repo in repolist:
            print("(X)\t\t"+repo)
            
        
    def startshell(self):
       
        sysrepofiles = self.parseRepoFile()

        if sysrepofiles:
            self.display_available_repo(sysrepofiles)

            while True:
                user_action = input("What repository action would you like to perform? " + str(self.actions) + ": ")
                if user_action.lower() in [i.lower() for i in self.actions]:
                    break
                else:
                    print("Please type your option: enable or disable")


            while True:

                user_options = input("Please provide the repository numbers, seperated by comma: ")

                if user_options:
                    id_list = self.id_to_repolist(user_options)
                
                    actionable_repos = []

                    for id in id_list:
                        if id in sysrepofiles.keys():
                            actionable_repos.append(sysrepofiles[id])
                        else:
                            print("Invalid input")
                    if actionable_repos:
                        break

            while True:

                self.display_confirmation(actionable_repos)
                user_confirm = input("We should " + user_action + " the above repos? " + str(self.confirm) + ": ")
                
                if user_confirm.lower() in [i.lower() for i in self.confirm]:
                    
                    if user_confirm.lower() =="yes":
                        self.processRequest(user_action, actionable_repos)
                        break
                    else:
                        sys.exit(0)
                
        else:
            print("Sorry we could not find any repository listed")
            print("Please register the system with (Certificate-based) RHN and run yum repolist")
            print("\n\n")
            sys.exit(0)


    def processRequest(self, action, repolist):
       
        if action.lower() == "enable":
            continous_form = "Enabling"
        if action.lower() == "disable":
            continous_form = "Disabling"

        print("\n")
        print("Processing repositories. Please wait, this might take some time...")
        print("------------------------------------------------------------------")
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
    rm.startshell()


if __name__ == '__main__':
    
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram is exiting...")

