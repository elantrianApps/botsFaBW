
# -*- coding: utf-8 -*-
#!/usr/bin/python

"""
Usage:
Contains methods required by various scripts, including MessageBot

Dependencies:
- python2.7.x
- python-twitter library
    --(https://python-twitter.readthedocs.io/en/latest/installation.html)
- a Twitter "app" attached to your Twitter account, which creates API access keys
    -- This can be done at https://apps.twitter.com/
    -- See https://python-twitter.readthedocs.io/en/latest/getting_started.html
    for more info and a tutorial

Author:
Copyright 2017 Elizabeth Lagesse <github.com/elantrian> <www.elizabethlagesse.com>

This file is part of botsForABetterWorld.

    botsForABetterWorld is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    botsForABetterWorld is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with botsForABetterWorld.  If not, see <http://www.gnu.org/licenses/>.

"""

import sys
import time
from types import *
import operator
import random
import argparse
import fnmatch
import twitter


#initialize a (pseudo)random number generator for staggering API calls
random.seed()

def stdout_redirector(stream):
    old_stdout = sys.stdout
    sys.stdout = stream
    try:
        yield
    finally:
        sys.stdout = old_stdout


class BotTools:
    def __init__(self,args):
        self.args = args
        self.create = self.creator()

    def creator (self):
        """
        Creates authenticated API instance using input from the command line
        Returns: self.create (which is the API instance)
        """
        self.myName = raw_input("What is your name? ") or "Nameless(:-/)"
        print "-------------"
        print "Make sure you have your Consumer and Access keys for the Twitter API"
        print "(Go to https://apps.twitter.com/ to make an app or get keys. I'll wait...)"
        print "-------------"
        thisConsumerKey = raw_input("Please enter the Consumer Key (also called 'API Key'): ")
        thisConsumerSecret = raw_input("...and the Consumer Secret (also called 'API Secret'): ")
        thisAccessTokenKey = raw_input("Please enter the Access Token Key: ")
        thisAccessTokenSecret = raw_input("...and the Access Token Secret: ")
        if (thisConsumerKey and thisConsumerSecret and thisAccessTokenKey and thisAccessTokenSecret):
            try:
                self.create = twitter.Api(consumer_key=thisConsumerKey,
                    consumer_secret=thisConsumerSecret,
                    access_token_key=thisAccessTokenKey,
                    access_token_secret=thisAccessTokenSecret, sleep_on_rate_limit=True)
                return self.create
            except:
                # if the authentication section produces an error,
                # it's probably a twitter issue
                print "-----***-----"
                print "It looks like you've got an authentication or account \
                problem with Twitter. Please check your API keys and try again. \
                It may also be helpful to check your account status."
                print "-----***-----"
                quit()
        else:
            # if they press enter without providing a value, prompt and give info
            print "-----***-----"
            print "Please try again, and specify all requested keys!"
            print "Go to https://apps.twitter.com/ to setup an app or get keys."
            print "See https://python-twitter.readthedocs.io/en/latest/getting_started.html \
            if you need more info."
            print "-----***-----"
            quit()

    def fileToList (self):
        """
        Reads a file, creating a list element from each line, cleaning as it goes.
        Returns: fileLines (list of user IDs or screen names)
        """
        fileLines = []
        # each file line becomes an element in a list
        with open(self.args.file) as myFile:
            for line in myFile:
                line = line.strip()
                line = line.replace(",","")
                fileLines.append(line)
        return fileLines


    def fetchFollowers (self):
        """
        Collects list of followers.

        Default (no file provided): All followers of the authenticated user
        Optional: Followers listed in a text file provided at the command line
        Returns: followersList (list of user IDs or screen names from specified source)
        """
        if self.args.file:
            # if a file is provided, use those followers
            followersList = self.fileToList()
            print "Generated list of followers from file provided "
        else:
            # if no file, gather all followers for authenticated user
            followersList = self.create.GetFollowerIDs()
            print "Generated list of followers for the authenticated user "
        return followersList

    def fetchMessage (self):
        """
        Collects message text from a file provided at the command line.

        """
        try:
            with open(self.args.messageText) as myFile:
                self.messageToSend = myFile.read()
                return self.messageToSend
        except:
            print "-----***-----"
            print "Error: Please include a text file containing your message and try again.\n"
            print "(Use -h for more information)"
            print "-----***-----"
            quit()

    def messageFollowers (self):
        """
        Messages all followers in the list returned by fetchFollowers, with the
        message text returned by fetchMessage.
        """
        thisAPIInst = self.create
        followersList = self.fetchFollowers()
        messageToSend = self.fetchMessage()
        followerCount = 0
        alreadyMessaged = []
        for follower in followersList:
            try:
                # check if it's a screen name or user ID
                # send message
                if self.args.SN:
                    self.create.PostDirectMessage(messageToSend, screen_name=follower)
                else:
                    self.create.PostDirectMessage(messageToSend, user_id=follower)
                # update counters and record of sent messages
                followerCount +=1
                alreadyMessaged.append(follower)
                # sleep for a randomly chosen interval between 61 and 79 seconds
                # avoids the appearance of spam (sending requests too rapidly/evenly)
                if followerCount > 1:
                    sleeptime = 60 + random.randrange(1,20)
                    print "Waiting "+str(sleeptime)+" seconds"
                    time.sleep(sleeptime)
                else:
                    pass
            except:
                # if the twitter API throws an error, show user info on limits
                print "-----***-----"
                print "Something has gone wrong!"
                print "Specifically: "
                print "     "+str(sys.exc_info()[1])
                print "- If you've exceeded your API limit, see:"
                print "     https://dev.twitter.com/rest/public/rate-limiting"
                print "(Any progress has been saved to sentMessagesPARTIAL.txt)"
                print "-----***-----"
                # make sure to save progress!
                with open("sentMessagesPARTIAL.txt", 'a') as f:
                    for item in alreadyMessaged:
                        f.write(str(item))
                        f.write(", \n")
                quit()
        # if all messages send sucessfully, save a list of followers contacted
        with open("sentMessages.txt", 'a') as f:
            for item in alreadyMessaged:
                f.write(str(item))
                f.write(", \n")
        print str(followerCount)+" of " + str(self.myName) +"'s followers were messaged with the following: "
        print "-------------"
        print messageToSend
        print "-------------"


    def fetchFollowersPaged(self):
        """
        Collects a list of followers of a user/organization (by screen_name),
        in pages of 5000

        Requires a file name to be specified when script is called (as the 'file'
        argument, ie: self.args.file)

        """
        thisAPIInst = self.create
        try:
            orgList = self.fileToList()
        except:
            print "-----***-----"
            print "Error: Please include a text file containing the names of users and try again.\n"
            print "(Use -h for more information)"
            print "-----***-----"
            quit()

        #for each organization, page through followers 5,000 at a time
        for org in orgList:
            iterator = 1
            nextCursor = -1
            while nextCursor !=0: #keep going until there are no more results
                print "Retrieving results page "+str(iterator)+" for "+str(org))
                orgResults = thisAPIInst.GetFollowerIDsPaged(screen_name=org, cursor=nextCursor, count=5000)
                #output results to text file
                with open("foundFollowers.txt", 'a') as f:
                    for item in orgResults[-1]:
                        f.write(str(item)+", \n")
                print "Page "+str(iterator)+" results written sucessfully to foundFollowers.txt."
                iterator +=1
                nextCursor = orgResults[0]
        print "-------------"
        print "Done!"
        print "All results written to foundFollowers.txt"
        print "-------------"


    def fetchHashtagUsers(self):
        """
        Search for all users who've used one or more of a list of hashtags
        A single hashtag can be specified at the command line, or a text file
        can be used with one tag per line.

        Note: Generally the last 5-10 days of status data is available from Twitter

        List is output to file by number of followers (most-least)
        Dictionary of users with tags and number of followers is returned
        (key: screenname)
        """
        thisAPIInst = self.create
        if self.args.ht:
            hashList
            hashList = self.args.ht
        else:
            hashList = ['lonelyHashtag']

        #Dictionary to store all SNs found (key-Screenname:value-[[hashtags], number of followers])
        hashDict = {}

        #iterate over all hashtags of interest
        for hashEntry in hashList:
            print "searching for #"+hashEntry
            thisQuery = "q=%23"+ hashEntry + "&count=100"
            #get data
            hashResults = thisAPIInst.GetSearch(raw_query=thisQuery)
            #iterate over every status returned, grab the screennames,
            #and add to hashDict
            for status in hashResults:
                #an object parsing CF, as elements of the status obj
                #aren't addressable (sigh)
                statusString = str(status)
                splitStatus = statusString.split(',')
                snList = fnmatch.filter(splitStatus, ' "screen_name*')
                snPosterList = snList[0].split('"')
                snPoster = snPosterList[-2]

                #finally add the damn thing to the hashDict
                if snPoster in hashDict:
                    if hashEntry in hashDict[snPoster][0]:
                        pass
                    else:
                        hashDict[snPoster][0].append(hashEntry)
                else:
                    hashDict[snPoster] = [[hashEntry]]

        #gather the number of followers of each person found
        for name in hashDict.keys():
            thisUser = thisAPIInst.GetUser(screen_name=name)
            hashDict[name].append(thisUser.followers_count)

        #save formatted and sorted results to a text file
        dictlist = []

        #saves a list of users (order: most-least followers)
        #includes which hashtag(s) they used and how many followers they have
        #example: user,['tag1', 'tag2'],564
        with open("hashtagUsers.txt", 'a') as f:
            for key, value in hashDict.iteritems():
                dictlist.append([key,value])
            dictlist.sort(key=lambda sublist:sublist[1][1], reverse=True)
            for item in dictlist:
                f.write(str(item[0])+","+str(item[1][0])+","+str(item[1][1])+", \n")
        print "-------------"
        print "All results for hashtag search written to hashtagUsers.txt"
        print "-------------"
        return hashDict
