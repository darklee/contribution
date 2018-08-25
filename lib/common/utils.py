# coding=utf-8
from __future__ import unicode_literals

import re


def is_jira_user(jira_user, who):
    jira_user_pattern = '.*%s.*' % who
    return re.match(jira_user_pattern, jira_user) != None

print "1.5".isdigit()