"""
This file contains the blocklist of JWT tokens.

An issue: if restart the app, would lose the data
Solutions: use a db as other tables
    or redis for maximum performance
"""


BLOCKLIST = set()