#! /usr/bin/env python
"""

"""
import configparser
import subprocess


class RepoManager(object):
    
    def __init__(self):

        #self.action = null
        #self.uoptions = null
        #self.repofile = self.getRepoFile()
        self.repofile = 'sample.ini'


    def getRepoFile(self):
        #search the filesystem to look for the repo file
        pass


    def parseRepoFile(self):

        #return a list of available repository names
        if self.repofile:
            config = configparser.ConfigParser()
            config.read(self.repofile)
            available_repos  = config.sections()

            #if not available_repos:
            #use subprocess.call to run the yum repolist command           


    def startshell(self):
        #clean the user input based on type
        #return uoptions and action
        pass


    def processRequest(self, action, choosenlist, uoptions):
        pass


def managerepo():
    rm = RepoManager()
    print(rm.parseRepoFile())


if __name__ == '__main__':
    managerepo()
