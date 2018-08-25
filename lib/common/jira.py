# coding=utf-8
from __future__ import unicode_literals

import xlrd
import sys
import csv
import os
import consts
from collections import OrderedDict


def read_jira_excel(filepath=consts.jira_file):
    print 'Read excel: %s' % filepath
    workbook = xlrd.open_workbook(filepath)
    headers = []
    sheet = workbook.sheet_by_name('Sheet1')
    for row in sheet.get_rows():
        if len(headers) == 0:
            for cell in row:
                headers.append(cell.value)
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
    rows = read_jira_excel(consts.jira_file)
    for row in rows:
        print "Row: %s" % row


if __name__ == '__main__':
    sys.exit(main())
