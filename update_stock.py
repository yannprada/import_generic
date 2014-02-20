# -*- coding: utf-8 -*-
#!/usr/bin/python

import sys
import time

from csv_parser import CsvParser
from manager import Manager


class StockManager(Manager):
    def __init__(self, host, dbname, password):
        super(StockManager, self).__init__(host, dbname, password)
        self.product_records = self.prepare_many2one('product.product', 'default_code')
        self.location_records = self.prepare_many2one('stock.location')
        self.uom_records = self.prepare_many2one('product.uom')
    
    def update_stock(self, product_ref, product_qty, product_uom, source, destination, state, name):
        data = {
            'product_id': self.product_records[product_ref],
            'product_qty': product_qty,
            'product_uom': self.uom_records[product_uom],
            'location_id': self.location_records[source],
            'location_dest_id': self.location_records[destination],
            'state': state,
            'name': name,
        }
        
        return self.create('stock.move', data)


class MyStockManager(StockManager):
    def __init__(self, host, dbname, password, fileName, display=False):
        super(MyStockManager, self).__init__(host, dbname, password)
        data = self.all_records('product.product', ['default_code', 'name_template'])
        product_records = self.list_to_object(data, 'default_code', 'name_template')
        
        c = CsvParser(fileName)
        for row, count in c.rows():
            name = '[' + row['ref'] + '] ' + product_records[row['ref']]
            ID = self.update_stock(row['ref'], row['qty'], row['uom'], row['source'], row['destination'], 'done', name)
            
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
        m = MyStockManager(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], True)
        t2 = time.time()
        print('Duration: ' + time.strftime('%H:%M:%S', time.gmtime(t2-t1)))

