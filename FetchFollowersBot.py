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
python FetchFollowersBot.py [options] [file of users or screenname]

Options:
- --user
Optional: Tells FetchFollowersBot to expect a single screen name instead of
a file

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

parser = argparse.ArgumentParser(description='A Twitter bot for collecting a \
list of a user\'s followers. ')
parser.add_argument('--user', help='Optional: Tells FetchFollowersBot to expect \
a single screen name', action='store_true')
parser.add_argument('input', help='Required: Specify a file name or single user \
screen name (with --user option) of the user you want a list of followers for. ')
