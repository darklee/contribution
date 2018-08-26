# coding=utf-8
from __future__ import unicode_literals

from ..common import envs, jira, utils
from pyecharts import Radar
import json
import re
from collections import OrderedDict


# 根据各成员的实际贡献值，按贡献值分数基线值和最大值进行比例换算，计算出贡献值分数
# real_contribution_point 是某个成员迭代中的贡献值
# max_point 是所有成员当前迭代贡献值中取最大
def calc_contribution_serie(real_contribution_point, max_point):
    serie = envs.base_contribution_score + (envs.max_contribution_score - envs.base_contribution_score) * \
        (real_contribution_point / float(max_point))
    return round(serie)


def render(page):
    members = jira.members_contribution

    all_contribution_points = []
    for m in members.values():
        all_contribution_points.append(m["contribution"]["total"])
    max_contribution_point = max(all_contribution_points)

    schema = []
    contribution_series_total = []
    contribution_series_special = []

    for who in members:
        member = members[who]
        schema.append((member["name"], envs.max_contribution_score))
        contribution_series_total.append(calc_contribution_serie(
            member["contribution"]["total"], max_contribution_point))
        contribution_series_special.append(calc_contribution_serie(
            member["contribution"]["special"], max_contribution_point))

    radar = Radar('贡献值得分均衡情况')
    radar.config(schema)
    radar.add("特别贡献值", [contribution_series_special],
              is_area_show=True, area_opacity=0.3)
    radar.add("合计贡献值", [contribution_series_total],
              is_area_show=True, area_opacity=0.3)
    page.add(radar)
