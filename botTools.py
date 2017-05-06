
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
github.com/elantrian
"""

import sys
import twitter
import time
import random
import argparse

#initialize a (pseudo)random number generator for staggering API calls
random.seed()


class BotTools:
    def __init__(self,args):
        self.args = args

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
        Collects list of followers to message.
        Default (no file provided): All followers of the authenticated user
        Optional: Followers listed in a text file provided at the command line
        Returns: followersList (list of user IDs or screen names from specified source)
        """
        if self.args.file:
            # if a file is provided, use those followers
            followersList = self.fileToList()
            print "Generated list of followers to message from file provided"
        else:
            # if no file, gather all followers for authenticated user
            followersList = self.create.GetFollowerIDs()
            print "Generated list of followers to message from Twitter "
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
        thisAPIInst = self.creator()
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
