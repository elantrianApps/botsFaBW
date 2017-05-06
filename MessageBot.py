# -*- coding: utf-8 -*-
#!/usr/bin/python

"""
Usage:
Call at command line as follows:
python MessageBot.py [options] [message file]

Options:
- --file
allows for a list of user IDs in a text file (default: all followers), 1 per line
- --SN
allows for a file containing screen names (@ Twitter handles) instead of ID #s

Dependencies:
- botTools module (expects botTools.py in the same directory)
- python2.7.x
- python-twitter library
    --(https://python-twitter.readthedocs.io/en/latest/installation.html)
- a Twitter "app" attached to your Twitter account, which creates API access keys
    -- This can be done at https://apps.twitter.com/
    -- See https://python-twitter.readthedocs.io/en/latest/getting_started.html
    for more info and a tutorial

Features:
- Staggered API calls avoid being flagged as spam or hitting rate limit
    - Twitter limits DM's to 1000/day and 15/15 min. MessageBot will prevent you
    from exceeding your 15 min limit, and will simply pause and wait when you
    hit your daily limit. Note that messaging hundreds or thousands of followers
    will take hours to days. This isn't a limitation of MessageBot, It's a feature
    of Twitter that makes messaging bearable!
    - DMs are meant for humans, so we try to make your messages less robotic.
    That's why we stagger the calls by a random number of seconds, and generally
    slow them down. If you disable this feature, you will almost certainly be
    flagged as spam within seconds. (you have been warned)
- You choose a list of followers (specified 1 per line in a text file), or all of
the followers for the authenticated user
- You can choose to use twitter handles/screen names instead of the unique
numerical Twitter ID

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


import argparse
from botTools import *


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
