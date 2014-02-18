# -*- coding: utf-8 -*-
#!/usr/bin/python

import sys
import time

from csv_parser import CsvParser
from manager import Manager


class CustomerManager(Manager):
    def __init__(self, host, dbname, password):
        super(CustomerManager, self).__init__(host, dbname, password)
        self.existing_partners_records = self.prepare_ir_model_data('res.partner')
        title_records = self.prepare_many2one('res.partner.title')
        country_records = self.prepare_many2one('res.country')
        self.fieldsNames = {
            'name': {'type': 1, 'columnName': 'name'},
            'street': {'type': 1, 'columnName': 'street'},
            'zip': {'type': 1, 'columnName': 'zip'},
            'city': {'type': 1, 'columnName': 'city'},
            'phone': {'type': 1, 'columnName': 'phone'},
            'mobile': {'type': 1, 'columnName': 'mobile'},
            'fax': {'type': 1, 'columnName': 'fax'},
            'email': {'type': 1, 'columnName': 'email'},
            'website': {'type': 1, 'columnName': 'website'},
            'customer': {'type': 1, 'columnName': 'customer'},
            'is_company': {'type': 1, 'columnName': 'is_company'},
            'title': {'type': 2, 'columnName': 'title', 'records': title_records},
            'country': {'type': 2, 'columnName': 'country', 'records': country_records},
        }
    
    def run(self, fileName):
        c = CsvParser(fileName)
        for row, count in c.rows():
            data = self.build_data(row, self.fieldsNames)
            ref = row['ref']
            ID = self.insertOrUpdate(ref,'res.partner', data, self.existing_partners_records)
            
            if __name__ == '__main__':
                print(str(count) + ' --- ID: ' + str(ID))


if __name__ == '__main__':
    if len(sys.argv) < 5:
        print('''
Usage:
    python insert.py [host] [database] [password] [file.csv]
        ''')
        sys.exit()
    else:
        t1 = time.time()
        cm = CustomerManager(sys.argv[1], sys.argv[2], sys.argv[3])
        cm.run(sys.argv[4])
        t2 = time.time()
        print('Duration: ' + time.strftime('%H:%M:%S', time.gmtime(t2-t1)))

