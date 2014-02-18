# -*- coding: utf-8 -*-
#!/usr/bin/python

import sys
import time

from csv_parser import CsvParser
from manager import Manager


class ProductManager(Manager):
    def __init__(self, host, dbname, password, fileName, display=False):
        super(ProductManager, self).__init__(host, dbname, password)
        existing_prod_tmpl_records = self.prepare_ir_model_data('product.template')
        existing_prod_prod_records = self.prepare_ir_model_data('product.product')
        category_records = self.prepare_many2one('product.category')
        fields = ['name', 'description', 'weight_net', 'standard_price', 'list_price', 'type']
        
        c = CsvParser(fileName, delimiter=';')
        for row, count in c.rows():
            # product_template
            data_tmpl = {
                'sale_ok': True,
                'purchase_ok': True,
                'supply_method': 'buy',
                'procure_method': 'make_to_stock',
                'categ_id': category_records[row['category']]
            }
            
            for field in fields:
                data_tmpl[field] = row[field]
            
            ref = row['ref']
            product_tmpl_id = self.insertOrUpdate(
                    ref + '_product_template','product.template', data_tmpl, existing_prod_tmpl_records)
            
            # product_product
            data_product = {
                'default_code': ref,
                'name_template': row['name'],
                'active': True,
                'product_tmpl_id': product_tmpl_id,
            }
            product_product_id = self.insertOrUpdate(
                    ref, 'product.product', data_product, existing_prod_prod_records)
            
            if display == True:
                print(str(count) + ' --- ID: ' + str(product_product_id))


if __name__ == '__main__':
    if len(sys.argv) < 5:
        print('''
Usage:
    python insert_products.py [host] [database] [password] [file.csv]
        ''')
        sys.exit()
    else:
        t1 = time.time()
        pm = ProductManager(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], True)
        t2 = time.time()
        print('Duration: ' + time.strftime('%H:%M:%S', time.gmtime(t2-t1)))

