# coding=utf-8
from __future__ import unicode_literals


# 青木团队迭代贡献计算
""" 
特殊贡献值主要为角色贡献，按每月预估工作占比进行估算，设定值为百分比
故事按估算的故事点进行贡献值计算
故障有故事点的按故事点进行计算，没有的按对应issue_contribution_points进行计算
故障验证和提交故障按对应issue_contribution_points的贡献值进行计算
贡献点数根据故事点和特殊贡献补偿合并计算获得
贡献分数根据贡献分值范围平衡计算获得，范围越大越能体现贡献和价值，范围越小越和谐
评价分根据贡献分数对项目分进行分配获得
每个人保留0.5分在最后PTL/SM进行分配，用以调整评价和抹平分数，或者某些特殊情况，如新员工
PTL/SM的贡献值在计算考核分数占用时，不计算特殊贡献部份的分数？？？避免占用团队过多的分数资源，影响分数分配？？？
"""

import os


# ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
# 迭代冲刺调整区
jira_file = '%s/../../target/jira.xlsx' % os.path.dirname(__file__)

sprint_invest = 20  # 月平均投入按20人天估算，用于做特殊贡献值补偿计算
sprint_appraise_score_total = float(32)  # 每个月从项目得到的评价分
# 迭代冲刺调整区
# ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑


# ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
# 贡献值计算调整区

# 贡献分数计算范围
# 范围越大越能体现贡献和价值，但对团队协作和团结可能产生负面影响
# 范围越小越和谐，吃大锅饭，但会降低对积极工作同学的正向反馈，打击工作积极性
base_contribution_score = 50  # 团队基础贡献值分数，什么事都不干的基线分
max_contribution_score = 100  # 团队最大贡献值分数

member_names = [
    "黎明",
    "何敬",
    "梅瑜",
    "付繁虎",
    "陈秋曲",
    "刘芙蓉",
    "赵冠雄",
    "练昌勇",
    "陈欢"
]

appraise_members = [
    "何敬",
    "梅瑜",
    "付繁虎",
    "陈秋曲"
]

appraise_other_members = [
    "刘芙蓉",
    "赵冠雄",
    "练昌勇",
    "陈欢"
]

# 特殊角色补偿贡献计算
# MP 估算人月投入占比
special_contribution_points = {
    "代码评审(PORTAL/COBI)": 10,
    "代码评审(GI/CMDB)": 15,
    "用例评审(ROBOT/MANUAL)": 20,
    "QA": 30,
    "CM": 5,
    "BA(PORTAL/COBI)": 20,
    "BA(GI/CMDB)": 10,
    "防火墙:(PORTAL/COBI)": 30,
    "防火墙:(GI/CMDB)": 40,
    "新员工指导": 10,
    "PTL/SM": 70  # 多少合适？？？能够有30%的开发投入？？？
}

# 每个相关的issue计算对应的贡献值(SP*N)
# SP 估算故事点
issue_contribution_points = {
    "故障修复": 1,
    "故障验证": 0.5,
    "故障提交": 0.5
}

special_contribution = {
    "何敬":  ["CM"],
    "梅瑜":  ["BA(PORTAL/COBI)", "代码评审(PORTAL/COBI)", "防火墙:(PORTAL/COBI)"],
    "付繁虎":  ["BA(GI/CMDB)", "代码评审(GI/CMDB)", "新员工指导"],
    "刘芙蓉":  ["QA", "用例评审(ROBOT/MANUAL)", "新员工指导"],
    "黎明":  ["PTL/SM"]
}

# 每个人保留0.5分用于最后调整分配
sprint_appraise_score = sprint_appraise_score_total - len(appraise_members) * 0.5
# 贡献值计算调整区
# ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑


# ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
# JIRA Excel 字段定义
jira_issue_key = "Issue Key"
jira_issue_story_point = "故事点"
jira_issue_type = "任务类型"
jira_issue_assigner = "处理人"
jira_issue_reporter = "报告人"
jira_issue_verifier = "验证人"
jira_issue_type_bug = "BUG"
jira_issue_type_story = "故事"
# JIRA Excel 字段定义
# ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
