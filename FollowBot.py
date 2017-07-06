# -*- coding: utf-8 -*-
#!/usr/bin/python

"""
-----***-----

Warning!:
This project is a work in progress - what you get may not work out of the proverbial box :)

Twitter places limits on automated activity to prevent abuse.
You undertake ALL activity at YOUR OWN RISK.

-----***-----

Usage:
Call at command line as follows:
python FollowBot.py [options] [file of users to follow]

Requires a list of user IDs  (or screen names using --SN option)in a text file,
1 per line

Options:
- --SN
allows for a file containing screen names (@ Twitter handles) instead of ID #s

-----***-----

Warning!:
If you attempt to follow a large number of people, you will be asked if you
would like to follow people SLOWLY in the background.

-- Note: If you choose this option, you might still be banned.This is at the
sole discretion of Twitter. Twitter might also change their policies at any time.
Continue at your own risk.

-- Note: Depending on how many people you are trying to follow, you may still
hit an overall account limit, even if you are slow-following.
See https://support.twitter.com/articles/68916 for more information.

-----***-----

Dependencies:
- botTools module (expects botTools.py in the same directory)
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

import argparse
from botTools import *


parser = argparse.ArgumentParser(description='A Twitter bot for following \
                                new friends. ')
parser.add_argument('file', help='Required: File with user IDs, one per line')
parser.add_argument('--SN', help='Optional: Tells FollowBot to expect a file with \
                    Screen Names, rather than default (User IDs)',
                    action='store_true')

args = parser.parse_args()

newInst = BotTools(args)
newInst.followNewFriends()
