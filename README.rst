voteit.statistics README
========================

Show some statistics for user contributions, like number of proposals,
discussion posts or other things users have done.

* Project page & source code: `<https://github.com/VoteIT/voteit.statistics>`_


Installation
------------

Simply include the file in the VoteIT paster config file. There should
be a section called plugins - add 'voteit.statistics' to it.
After restart, 'Statistics" should be a visible alternative in the meeting menu.

This package has no persistence what so ever, so it won't change anything in
VoteIT and will be removed completely when it isn't included.


Configuration
=============

The only option available right now is to change the content types that should display statistics.

  statistics.ctypes = <list of content types here>

Will default to:

  statistics.ctypes =
    Proposal
    Discussion
    Vote

Feedback, questions, bugs etc?
------------------------------

Go to `www.voteit.se <https://www.voteit.se>`_ for contact information. The dev team should be listed there.

If you find a bug, please report it at
`<https://github.com/VoteIT/voteit.statistics/issues>`_
or simply email robin@betahaus.net

