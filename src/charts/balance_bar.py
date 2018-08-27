# coding=utf-8
from __future__ import unicode_literals

from pyecharts import Bar
from ..common import envs, jira, utils
from collections import OrderedDict


def render(page):
    # pip install jupyter-echarts-pypkg==0.1.1 解决is_convert后Y坐标名称不正确的问题
    members = jira.members_contribution
    bar = Bar("贡献值均衡详情(点数)")
    attr = envs.member_names
    contribution_types_dict = OrderedDict(envs.special_contribution_points)
    reduce(lambda result, next: contribution_types_dict.update(next), map(
        lambda e: e['contribution-list'], members.values()))
    contribution_types = list(contribution_types_dict.keys())
    contribution_types.reverse()

    for ct in contribution_types:
        series = []
        for name in envs.member_names:
            cl = members[name]['contribution-list']
            point = 0
            if ct in cl:
                point = cl[ct]
            series.append(point)
        bar.add(ct, attr, series, is_stack=True,
                is_legend_show=False, is_convert=True)
    page.add(bar)
