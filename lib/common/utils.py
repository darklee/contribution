# coding=utf-8
from __future__ import unicode_literals

import re
import envs

# 判断一个JIRA用户是否是某个团队成员


def is_jira_user(jira_user, who):
    jira_user_pattern = '.*%s.*' % who
    return re.match(jira_user_pattern, jira_user) != None


# 根据各成员的实际贡献值，按贡献值分数基线值和最大值进行比例换算，计算出贡献值分数
# real_contribution_point 是某个成员迭代中的贡献值
# max_point 是所有成员当前迭代贡献值中取最大
def calc_contribution_score(real_contribution_point, max_point):
    score = envs.base_contribution_score + (envs.max_contribution_score - envs.base_contribution_score) * \
        (real_contribution_point / float(max_point))
    return round(score)


# 根据各成员的实际贡献值，计算贡献分数，再根据贡献分数分配考核评价点数
def calc_appraise_scores(contribution_scores):
    sum_contribution_score = sum(contribution_scores)
    factor = float(envs.sprint_appraise_score) / sum_contribution_score
    return map(lambda score: float('%.1f' % (score * factor)), contribution_scores)


def calc_appraise_other_scores(contribution_scores):
    sum_contribution_score = sum(contribution_scores)
    factor = envs.sprint_appraise_other_score / sum_contribution_score
    return map(lambda score: float('%.1f' % (score * factor)), contribution_scores)
