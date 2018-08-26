# coding=utf-8
from __future__ import unicode_literals

from ..common import envs, jira, utils
from pyecharts import Radar
import json
import re
from collections import OrderedDict


# 展示迭代中所有成员的贡献分数的均衡雷达图
def render(page):
    members = jira.members_contribution

    all_contribution_points = []
    for m in members.values():
        all_contribution_points.append(m["contribution"]["total"])
    max_contribution_point = max(all_contribution_points)

    schema = []
    contribution_score_total = []
    contribution_score_special = []

    for who in members:
        member = members[who]
        schema.append((member["name"], envs.max_contribution_score))
        contribution_score_total.append(utils.calc_contribution_score(
            member["contribution"]["total"], max_contribution_point))
        contribution_score_special.append(utils.calc_contribution_score(
            member["contribution"]["special"], max_contribution_point))

    radar = Radar('贡献值均衡情况(得分)')
    radar.config(schema)
    radar.add("特别贡献值", [contribution_score_special],
              is_area_show=True, area_opacity=0.3)
    radar.add("合计贡献值", [contribution_score_total],
              is_area_show=True, area_opacity=0.3)
    page.add(radar)
