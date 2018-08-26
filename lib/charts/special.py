# coding=utf-8
from __future__ import unicode_literals

from pyecharts import Bar
from ..common import envs, jira, utils


def render(page):
    # pip install jupyter-echarts-pypkg==0.1.1 解决Y坐标不正确的问题
    bar = Bar("角色工作占比贡献补偿(%)")
    attr = envs.member_names
    for special in envs.special_contribution_points:
        series = []
        for member in envs.member_names:
            point = 0
            if member in envs.special_contribution:
                if special in envs.special_contribution[member]:
                    point = envs.special_contribution_points[special]
            series.append(point)
        bar.add(special, attr, series, is_stack=True,
                yaxis_max=100, is_legend_show=False)
    page.add(bar)
