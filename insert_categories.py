# -*- coding: utf-8 -*-
#!/usr/bin/python

import sys
import time

from csv_parser import CsvParser
from manager import Manager


class CategoryManager(Manager):
    def __init__(self, host, dbname, password):
        super(CategoryManager, self).__init__(host, dbname, password)
        self.existing_category_records = self.prepare_ir_model_data('product.category')
        self.master_category = self.search('product.category', [('name', '=', 'All products')])[0]
    
    def run(self, fileName):
        c = CsvParser(fileName)
        for row, count in c.rows():
            data = { 'name': row['Name'] }
            
            ids = self.search('product.category', [('name', '=', row['Parent Category'])])
            if len(ids) > 0:
                data['parent_id'] = ids[0]
            else:
                data['parent_id'] = self.master_category
            
            ref = row['External ID']
            ID = self.insertOrUpdate(ref,'product.category', data, self.existing_category_records)
            
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
        cm = CategoryManager(sys.argv[1], sys.argv[2], sys.argv[3])
        cm.run(sys.argv[4])
        t2 = time.time()
        print('Duration: ' + time.strftime('%H:%M:%S', time.gmtime(t2-t1)))

