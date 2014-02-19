# -*- coding: utf-8 -*-
#!/usr/bin/python

import sys
import time

from csv_parser import CsvParser
from manager import Manager


class CategoryManager(Manager):
    def __init__(self, host, dbname, password, fileName, display=False):
        super(CategoryManager, self).__init__(host, dbname, password)
        existing_category_records = self.prepare_ir_model_data('product.category')
        self.master_category_id = self.search('product.category', [('name', '=', 'All products')])[0]
        
        c = CsvParser(fileName)
        for row, count in c.rows():
            data = {
                'name': row['name'],
                'parent_id': self.getParent(row['parent']),
            }
            
            ref = row['ref']
            ID = self.insertOrUpdate(ref,'product.category', data, existing_category_records)
            
            if display == True:
                print(str(count) + ' --- ID: ' + str(ID))

    def getParent(self, parentName):
        ids = self.search('product.category', [('name', '=', row['parent'])])
        return ids[0] if len(ids) > 0 else self.master_category_id


if __name__ == '__main__':
    if len(sys.argv) < 5:
        print('''
Usage:
    python insert_categories.py [host] [database] [password] [file.csv]
        ''')
        sys.exit()
    else:
        t1 = time.time()
        m = CategoryManager(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], True)
        t2 = time.time()
        print('Duration: ' + time.strftime('%H:%M:%S', time.gmtime(t2-t1)))

