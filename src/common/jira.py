# coding=utf-8
from __future__ import unicode_literals

import xlrd
import sys
import csv
import os
import json
import envs
import utils
from collections import OrderedDict


# 计算获得所有成员的贡献值
def get_members_contribution():
    members = OrderedDict()
    for who in envs.member_names:
        member = OrderedDict()
        member["name"] = who
        member["contribution-list"] = calc_contribution(who)
        member["contribution"] = {
            "total":  sum(
                map(lambda e: e[1], member["contribution-list"].items())),  # 总的贡献值
            "special": sum(
                map(lambda e: e[1], filter(lambda e: e[0] in envs.special_contribution_points, member["contribution-list"].items())))  # 特殊角色补偿贡献值
        }
        members[who] = member

    all_contribution_points = []
    for m in members.values():
        all_contribution_points.append(m["contribution"]["total"])
    max_contribution_point = max(all_contribution_points)
    for who in members:
        member = members[who]
        member["contribution-score"] = {
            "total": utils.calc_contribution_score(member["contribution"]["total"], max_contribution_point),
            "special": utils.calc_contribution_score(member["contribution"]["special"], max_contribution_point)
        }

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

    done_jira_issues = filter(
        lambda row: row[envs.jira_issue_status] == 'Done', jira_issues)
    done_assignee_jira_issues = filter(
        lambda row: utils.is_jira_user(row[envs.jira_issue_assigner], who), done_jira_issues)

    doing_jira_issues = filter(
        lambda row: row[envs.jira_issue_status] not in ('Done', 'Cancelled'), jira_issues)
    doing_assignee_jira_issues = filter(
        lambda row: utils.is_jira_user(row[envs.jira_issue_assigner], who), doing_jira_issues)

    doing_story_points = sum(map(lambda row: float('%.1f' % (utils.parse_float(row[envs.jira_issue_story_point]) * (0 if type(row[envs.jira_issue_progress]) != float else row[envs.jira_issue_progress]))), filter(
        lambda row: row[envs.jira_issue_type] != envs.jira_issue_type_bug, doing_assignee_jira_issues)))
    contribution['部份完成'] = float('%.1f' % doing_story_points)

    story_points = sum(map(lambda row: utils.parse_float(row[envs.jira_issue_story_point]), filter(
        lambda row: row[envs.jira_issue_type] == envs.jira_issue_type_story, done_assignee_jira_issues)))
    contribution['故事'] = float('%.1f' % story_points)

    task_points = sum(map(lambda row: utils.parse_float(row[envs.jira_issue_story_point]), filter(
        lambda row: row[envs.jira_issue_type] not in (envs.jira_issue_type_bug, envs.jira_issue_type_story), done_assignee_jira_issues)))
    contribution['任务'] = float('%.1f' % task_points)

    # BUG如果有估算的按估算，无估算的按默认issue_contribution_points['故障修复']点
    bug_points = sum(map(lambda row: utils.parse_float(row[envs.jira_issue_story_point]) if utils.parse_float(row[envs.jira_issue_story_point]) > 0 else envs.issue_contribution_points['故障修复'], filter(
        lambda row: row[envs.jira_issue_type] == envs.jira_issue_type_bug, done_assignee_jira_issues)))
    contribution['故障处理'] = float('%.1f' % bug_points)

    # 报告BUG的点数
    report_bug_points = sum(map(lambda row: envs.issue_contribution_points['故障提交'], filter(
        lambda row: utils.is_jira_user(row[envs.jira_issue_reporter], who) and row[envs.jira_issue_type] == envs.jira_issue_type_bug, done_jira_issues)))
    contribution['故障提交'] = float('%.1f' % report_bug_points)

    # 验证BUG的点数
    verify_bug_points = sum(map(lambda row: envs.issue_contribution_points['故障验证'], filter(
        lambda row: utils.is_jira_user(row[envs.jira_issue_verifier], who) and row[envs.jira_issue_type] == envs.jira_issue_type_bug, done_jira_issues)))
    contribution['故障验证'] = float('%.1f' % verify_bug_points)

    return contribution


# 计算成员的特殊贡献补偿值，主要是部份角色补偿
def calc_special_contribution(who):
    contribution = OrderedDict()
    if who in envs.special_contribution:
        for n in envs.special_contribution[who]:
            point = round(
                envs.special_contribution_points[n] / float(100) * envs.sprint_invest)
            contribution[n] = point
    return contribution


def read_jira_excel(filepath=envs.jira_file):
    print 'Read excel: %s' % filepath
    workbook = xlrd.open_workbook(filepath)
    headers = []
    sheet = workbook.sheet_by_name('general_report')
    for idx, row in enumerate(sheet.get_rows()):
        if idx < 3:
            continue  # 忽略开头的几行无效数据
        if len(headers) == 0:
            for cell in row:
                headers.append(cell.value)
            if headers[0] != 'Project':
                raise ValueError('Unexcepted jira excel header start')
        else:
            data = OrderedDict()
            for idx, cell in enumerate(row):
                data[headers[idx]] = cell.value
            yield data


def read_jira_csv(filepath):
    with open(filepath) as f:
        reader = csv.reader(f)
        for row in reader:
            yield row


def main():
    rows = read_jira_excel(envs.jira_file)
    for row in rows:
        print "Row: %s" % row


if __name__ == '__main__':
    sys.exit(main())


jira_issues = list(read_jira_excel())
members_contribution = get_members_contribution()
