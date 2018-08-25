# coding=utf-8
from __future__ import unicode_literals

from ..common import consts, jira, utils
from pyecharts import Radar
import json
import re
from collections import OrderedDict

jira_issues = list(jira.read_jira_excel())


# 计算获得所有成员的贡献值
def get_members_contribution():
    members = OrderedDict()
    for who in consts.member_names:
        member = OrderedDict()
        member["name"] = who
        member["contribution-list"] = calc_contribution(who)
        member["contribution"] = {
            "total":  sum(
                map(lambda e: e[1], member["contribution-list"].items())),  # 总的贡献值
            "special": sum(
                map(lambda e: e[1], filter(lambda e: e[0] in consts.special_contribution_points, member["contribution-list"].items())))  # 特殊角色补偿贡献值
        }
        members[who] = member
    print json.dumps(members, indent=2, ensure_ascii=False)
    return members


# 计算成员的贡献值
def calc_contribution(who):
    contribution = OrderedDict()
    contribution.update(calc_special_contribution(who))
    contribution.update(calc_issue_contribution(who))
    return contribution


# 计算成员的迭代贡献值
def calc_issue_contribution(who):
    contribution = OrderedDict()
    # 非BUG全部按估算故事点数进行计算
    whos_jira_issues = filter(
        lambda row: utils.is_jira_user(row[consts.jira_issue_assigner], who), jira_issues)

    story_points = sum(map(lambda row: row[consts.jira_issue_story_point], filter(
        lambda row: row[consts.jira_issue_type] != consts.jira_issue_type_bug, whos_jira_issues)))
    contribution['故事点'] = story_points

    # BUG如果有估算的按估算，无估算的按默认issue_contribution_points['故障修复']点
    bug_points = sum(map(lambda row: row[consts.jira_issue_story_point] if (type(row[consts.jira_issue_story_point]) in [int, float] and row[consts.jira_issue_story_point] > 0) else consts.issue_contribution_points['故障修复'], filter(
        lambda row: row[consts.jira_issue_type] == consts.jira_issue_type_bug, whos_jira_issues)))
    contribution['故障处理'] = bug_points

    # 报告BUG的点数
    report_bug_points = sum(map(lambda row: consts.issue_contribution_points['故障提交'], filter(
        lambda row: utils.is_jira_user(row[consts.jira_issue_reporter], who), jira_issues)))
    contribution['故障提交'] = report_bug_points

    # 验证BUG的点数
    verify_bug_points = sum(map(lambda row: consts.issue_contribution_points['故障验证'], filter(
        lambda row: utils.is_jira_user(row[consts.jira_issue_verifier], who), jira_issues)))
    contribution['故障验证'] = verify_bug_points

    return contribution


# 计算成员的特殊贡献补偿值，主要是部份角色补偿
def calc_special_contribution(who):
    contribution = OrderedDict()
    if who in consts.special_contribution:
        for n in consts.special_contribution[who]:
            point = round(
                consts.special_contribution_points[n] / float(100) * consts.sprint_invest)
            contribution[n] = point
    return contribution


# 根据各成员的实际贡献值，按贡献值分数基线值和最大值进行比例换算，计算出贡献值分数
# real_contribution_point 是某个成员迭代中的贡献值
# max_point 是所有成员当前迭代贡献值中取最大
def calc_contribution_serie(real_contribution_point, max_point):
    serie = consts.base_contribution_score + (consts.max_contribution_score - consts.base_contribution_score) * \
        (real_contribution_point / float(max_point))
    return round(serie)


def render_balance(page):
    members = get_members_contribution()

    all_contribution_points = []
    for m in members.values():
        all_contribution_points.append(m["contribution"]["total"])
    max_contribution_point = max(all_contribution_points)

    schema = []
    contribution_series_total = []
    contribution_series_special = []

    for who in members:
        member = members[who]
        schema.append((member["name"], consts.max_contribution_score))
        contribution_series_total.append(calc_contribution_serie(
            member["contribution"]["total"], max_contribution_point))
        contribution_series_special.append(calc_contribution_serie(
            member["contribution"]["special"], max_contribution_point))

    radar = Radar('团队贡献值均衡情况')
    radar.config(schema)
    radar.add("特别贡献值", [contribution_series_special],
              is_area_show=True, area_opacity=0.5)
    radar.add("合计贡献值", [contribution_series_total],
              is_area_show=True, area_opacity=0.5)
    page.add(radar)
