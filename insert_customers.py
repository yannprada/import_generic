# -*- coding: utf-8 -*-
#!/usr/bin/python

import sys
import time

from csv_parser import CsvParser
from manager import Manager


class CustomerManager(Manager):
    def __init__(self, host, dbname, password, fileName, display=False):
        super(CustomerManager, self).__init__(host, dbname, password)
        existing_partners_records = self.prepare_ir_model_data('res.partner')
        title_records = self.prepare_many2one('res.partner.title')
        country_records = self.prepare_many2one('res.country')
        fields = ['name', 'street', 'zip', 'city', 'phone', 'mobile', 'fax', 'email', 'website', 'customer', 'is_company']
        
        c = CsvParser(fileName)
        for row, count in c.rows():
            data = {
                'title': title_records[row['title']],
                'country': country_records[row['country']],
            }
            
            for field in fields:
                data[field] = row[field]
            
            ref = row['ref']
            ID = self.insertOrUpdate(ref,'res.partner', data, existing_partners_records)
            
            if display == True:
                print(str(count) + ' --- ID: ' + str(ID))


if __name__ == '__main__':
    if len(sys.argv) < 5:
        print('''
Usage:
    python insert_customers.py [host] [database] [password] [file.csv]
        ''')
        sys.exit()
    else:
        t1 = time.time()
        cm = CustomerManager(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], True)
        t2 = time.time()
        print('Duration: ' + time.strftime('%H:%M:%S', time.gmtime(t2-t1)))

