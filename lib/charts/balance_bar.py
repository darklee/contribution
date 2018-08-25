# coding=utf-8
from __future__ import unicode_literals

from pyecharts import Bar
from ..common import consts, jira, utils
from collections import OrderedDict


def render(page):
    members = jira.members_contribution
    bar = Bar("贡献值均衡详情")
    attr = consts.member_names
    contribution_types_dict = OrderedDict(consts.special_contribution_points)
    reduce(lambda result, next: contribution_types_dict.update(next), map(
        lambda e: e['contribution-list'], members.values()))
    contribution_types = list(contribution_types_dict.keys())
    contribution_types.reverse()

    for ct in contribution_types:
        series = []
        for name in consts.member_names:
            cl = members[name]['contribution-list']
            point = 0
            if ct in cl:
                point = cl[ct]
            series.append(point)
        bar.add(ct, attr, series, is_stack=True,
                is_legend_show=False, is_convert=True)
    page.add(bar)
