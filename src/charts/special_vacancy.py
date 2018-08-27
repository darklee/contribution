# coding=utf-8
from __future__ import unicode_literals

from pyecharts import Bar
from ..common import envs, jira, utils


# 展示部分没有人负责的空缺的特殊工作
def render(page):
    bar = Bar("特殊工作空缺")
    attr = []
    series = []
    for special in envs.special_contribution_points:
        vacancy = True
        special_point = envs.special_contribution_points[special]
        for name in envs.member_names:
            if name in envs.special_contribution and special in envs.special_contribution[name]:
                vacancy = False
        if vacancy:
            attr.append(special)
            series.append(special_point)
    bar.add("空缺", attr, series, is_stack=True,
            yaxis_max=100, is_legend_show=False, bar_category_gap="%s%%" % max(20, 100 - len(series) * 10))
    # 如果有空缺才显示此图形
    if len(attr) > 0:
        page.add(bar)
