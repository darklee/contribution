# coding=utf-8
from __future__ import unicode_literals

from pyecharts import Bar
from ..common import envs, jira, utils
from collections import OrderedDict


def render_a(page):
    members = jira.members_contribution

    names = []
    contribution_score = []

    for who in envs.appraise_members:
        member = members[who]
        names.append(who)
        contribution_score.append(member['contribution-score']['total'])
    appraise_score = utils.calc_appraise_scores(contribution_score)

    bar = Bar("评价可分配分数(A)")
    names = names + ['PTL保留']
    appraise_score = appraise_score + \
        [envs.sprint_appraise_score_total - sum(appraise_score)]
    bar.add("分数", names, appraise_score,
            is_legend_show=False, is_convert=True)

    page.add(bar)

def render_b(page):
    members = jira.members_contribution

    names = []
    contribution_score = []

    for who in envs.appraise_other_members:
        member = members[who]
        names.append(who)
        contribution_score.append(member['contribution-score']['total'])
    other_appraise_score = utils.calc_appraise_other_scores(contribution_score)

    bar = Bar("评价可分配分数(B)")
    names = names + ['PTL保留']
    appraise_score = other_appraise_score + \
        [envs.sprint_appraise_score_total - sum(other_appraise_score)]
    bar.add("分数", names, appraise_score,
            is_legend_show=False, is_convert=True)

    page.add(bar)


def render(page):
    render_a(page)
    render_b(page)
