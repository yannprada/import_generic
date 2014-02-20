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
        self.many2one_records = {
            'title': self.prepare_many2one('res.partner.title'),
            'country': self.prepare_many2one('res.country'),
        }
    
    def insert(self, raw_data, many2one_data, ref):
        data = {field: raw_data[field] for field in raw_data}
        for field in many2one_data:
            data[field] = self.many2one_records[field][many2one_data[field]]
        
        return self.insertOrUpdate(ref,'res.partner', data, self.existing_partners_records)


class MyCustomerManager(CustomerManager):
    def __init__(self, host, dbname, password, fileName, display=False):
        super(MyCustomerManager, self).__init__(host, dbname, password)
        
        c = CsvParser(fileName)
        for row, count in c.rows():
            raw_data = {
                'name': row['name'],
                'street': row['street'],
                'zip': row['zip'],
                'city': row['city'],
                'phone': row['phone'],
                'mobile': row['mobile'],
                'fax': row['fax'],
                'email': row['email'],
                'website': row['website'],
                'customer': self.booleanFromString(row['customer']),
                'is_company': self.booleanFromString(row['is_company']),
            }
            many2one_data = {
                'title': row['title'],
                'country': row['country'],
            }
            ID = self.insert(raw_data, many2one_data, row['ref'])
            
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
        m = MyCustomerManager(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], True)
        t2 = time.time()
        print('Duration: ' + time.strftime('%H:%M:%S', time.gmtime(t2-t1)))

