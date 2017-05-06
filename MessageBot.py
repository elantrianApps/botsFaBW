# -*- coding: utf-8 -*-
#!/usr/bin/python

import argparse
from botTools import *



"""

Usage:
Call at command line as follows:
1.a) With a file full of ** user IDs ** (one per line, no commas/etc) to be messaged:
- python MessageBot.py <myMessage.txt> <followersToMessage.txt>
1.a) With a file full of ** Screen Names ** (one per line, no commas/etc) to be messaged:
- python MessageBot.py -SN <myMessage.txt> <followersToMessage.txt>
1.b) Collecting followers of a particular user and messaging all of them:
- python MessageBot.py <myMessage.txt>
2) Follow user prompts to enter API credentials

Requires:
- botTools module (expects botTools.py in the same directory)
- python2.7.x
- python-twitter library
    --(https://python-twitter.readthedocs.io/en/latest/installation.html)
- a Twitter "app" attached to your Twitter account, which creates API access keys
    -- This can be done at https://apps.twitter.com/
    -- See https://python-twitter.readthedocs.io/en/latest/getting_started.html
    for more info and a tutorial

Features:


Author: github.com/elantrian
"""
parser = argparse.ArgumentParser(description='A Twitter bot for sending \
                                messages to your followers. ')
parser.add_argument('messageText', help='Required: File with your message text')
parser.add_argument('--SN', help='Optional: Tells MessageBot to expect a file with \
                    Screen Names, rather than default (User IDs)',
                    action='store_true')
parser.add_argument('--file', help='Optional: File with followers to message, instead of all',
                    default=False, )


args = parser.parse_args()

newInst = BotTools(args)
newInst.messageFollowers()
