#!/usr/bin/env python
#-*- coding:utf-8 _*-

"""
@File       : checkdata.py
@version    : 0.1
@Author     : kelvin
@Time       : 2020-04-24

--------------------------------------------------------------------
@Changes log:
    2020-04-24 : 0.1 Create
"""
import logging
import operator

import excel_data as db

def output_report(args=None):
    records = db.__db_bugs_records__
    #days = sorted({r[db.FIELD_UPDATE_DATE] for rec in records_list for r in rec})

    bug_ids = {r[db.BUGS_FIELD_ID] for r in db.__db_bugs_records__}

    logging.debug(bug_ids)

    records = sorted_records(db.__db_bugs_records__, db.FIELD_UPDATE_DATE, order_desc=True)
    #records = sorted(db.__db_bugs_records__, key=operator.itemgetter(db.FIELD_UPDATE_DATE), reverse=False)



    abnormal_bug_ids =[]
    for id in bug_ids:
        records_by_bugid = [r for r in records if r[db.BUGS_FIELD_ID] == id]

        if len(records_by_bugid) > 0 and records_by_bugid[0][db.FIELD_STATUS] in ('新建', '解决中'):
            abnormal_bug_ids.append(id)

            logging.debug(' - {0}'.format(id))
            for r in records_by_bugid:
                logging.debug('  {0}'.format(r))


def sorted_records(records, fields, order_desc=False):
    recs = sorted(records, key=operator.itemgetter(fields), reverse=order_desc)
    return recs