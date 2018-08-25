# coding=utf-8
from __future__ import unicode_literals

from pyecharts import Page
import os
from lib.common import jira, consts
from lib.charts import balance


def main():
    os.chdir(os.path.dirname(__file__))
    page = Page()
    balance.render_balance(page)
    page.render('target/page.html')


main()
