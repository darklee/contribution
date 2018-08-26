# coding=utf-8
from __future__ import unicode_literals

from pyecharts import Bar
from ..common import envs, jira, utils


def render(page):
    bar = Bar("特殊工作占比贡献补偿(%)")
    for special in envs.special_contribution_points:
        series = []
        special_point = envs.special_contribution_points[special]
        for name in envs.member_names:
            point = 0
            if name in envs.special_contribution and special in envs.special_contribution[name]:
                point = special_point
            series.append(point)
        bar.add(special, envs.member_names, series, is_stack=True,
                yaxis_max=100, is_legend_show=False)
    page.add(bar)
