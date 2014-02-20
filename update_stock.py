# -*- coding: utf-8 -*-
#!/usr/bin/python

import sys
import time

from csv_parser import CsvParser
from manager import Manager


class StockManager(Manager):
    def __init__(self, host, dbname, password, fileName, display=False):
        super(StockManager, self).__init__(host, dbname, password)
        products_records = self.prepare_many2one('product.product', 'default_code')
        location_records = self.prepare_many2one('stock.location')
        uom_records = self.prepare_many2one('product.uom')
        location_fields = ['source', 'destination']
        
        c = CsvParser(fileName)
        for row, count in c.rows():
            data = {
                'product_id': products_records[row['ref']],
                'product_qty': row['qty'],
                'product_uom': uom_records[row['uom']],
                'location_id': location_records[row['source']],
                'location_dest_id': location_records[row['destination']],
                'state': 'done',
                'name': row['ref'],
            }
            
            ID = self.create('stock.move', data)
            
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
        m = StockManager(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], True)
        t2 = time.time()
        print('Duration: ' + time.strftime('%H:%M:%S', time.gmtime(t2-t1)))

