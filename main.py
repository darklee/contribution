# coding=utf-8
from __future__ import unicode_literals

from pyecharts import Page
import os
from lib.common import jira, consts
from lib.charts import balance_radar, balance_bar, special, special_vacancy


def main():
    os.chdir(os.path.dirname(__file__))
    page = Page("团队迭代情况")
    special.render(page)
    special_vacancy.render(page)
    balance_radar.render(page)
    balance_bar.render(page)
    page.render('target/page.html', template_name="lib/templates/simple_page.html")


main()
