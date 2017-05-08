.. botsFaBW documentation master file, created by
   sphinx-quickstart on Sun May  7 17:36:36 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.
#################################
botsForABetterWorld Documentation
#################################
\ **This project (and these doc pages) is an active work in progress!**\


www.botsForABetterWorld.com


Features
========

MessageBot
----------
Sends Twitter Direct Messages to specified (or all) followers of an authenticated
user

* Staggered API calls avoid being flagged as spam or hitting rate limit

  * Twitter limits DM's to 1000/day and 15/15 min. MessageBot will prevent you
    from exceeding your 15 min limit, and will simply pause and wait when you
    hit your daily limit. Note that messaging hundreds or thousands of followers
    will take hours to days. This isn't a limitation of MessageBot, It's a feature
    of Twitter that makes messaging bearable!

  * DMs are meant for humans, so we try to make your messages less robotic.
    That's why we stagger the calls by a randomized number of seconds, and generally
    slow them down. If you disable this feature, you will almost certainly be
    flagged as spam within seconds. (you have been warned)

* You choose a list of followers (specified 1 per line in a text file), or all of
  the followers for the authenticated user
* You can choose to use twitter handles/screen names instead of the unique
  numerical Twitter ID


Installation
============
(coming soon)

Support
=======

- Issue Tracker: https://github.com/elantrian/botsFaBW/issues

License
=======

Copyright 2017 Elizabeth Lagesse

* https://github.com/elantrian
* https://www.elizabethlagesse.com

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
along with botsForABetterWorld.  If not, see http://www.gnu.org/licenses/.


.. toctree::
   :maxdepth: 2
   :caption: Contents:
