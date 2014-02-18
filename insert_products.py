# -*- coding: utf-8 -*-
#!/usr/bin/python

import sys
import time

from csv_parser import CsvParser
from manager import Manager


class ProductManager(Manager):
    def __init__(self, host, dbname, password):
        super(ProductManager, self).__init__(host, dbname, password)
        self.existing_prod_tmpl_records = self.prepare_ir_model_data('product.template')
        self.existing_prod_prod_records = self.prepare_ir_model_data('product.product')
        category_records = self.prepare_many2one('product.category')
        self.tmpl_fields = {
            'sale_ok': {'type': 0, 'value': True},
            'purchase_ok': {'type': 0, 'value': True},
            'supply_method': {'type': 0, 'value': 'buy'},
            'procure_method': {'type': 0, 'value': 'make_to_stock'},
            'list_price': {'type': 1, 'columnName': 'prix_vente_ht'},
            'description': {'type': 1, 'columnName': 'description'},
            'weight_net': {'type': 1, 'columnName': 'poids_net'},
            'standard_price': {'type': 1, 'columnName': 'prix_achat_ht'},
            'name': {'type': 1, 'columnName': 'nom'},
            'type': {'type': 1, 'columnName': 'type'},
            'categ_id': {'type': 2, 'columnName': 'categorie', 'records': category_records},
        }
    
    def run(self, fileName):
        c = CsvParser(fileName, delimiter=';')
        for row, count in c.rows():
            # product_template
            data_tmpl = self.build_data(row, self.tmpl_fields)
            ref = row['reference']
            product_tmpl_id = self.insertOrUpdate(
                    ref + '_product_template','product.template', data_tmpl, self.existing_prod_tmpl_records)
            
            # product_product
            data_product = {
                'default_code': ref,
                'name_template': row['nom'],
                'active': True,
                'product_tmpl_id': product_tmpl_id,
            }
            product_product_id = self.insertOrUpdate(
                    ref, 'product.product', data_product, self.existing_prod_prod_records)
            
            if __name__ == '__main__':
                print(str(count))


if __name__ == '__main__':
    if len(sys.argv) < 5:
        print('''
Usage:
    python insert.py [host] [database] [password] [file.csv]
        ''')
        sys.exit()
    else:
        t1 = time.time()
        pm = ProductManager(sys.argv[1], sys.argv[2], sys.argv[3])
        pm.run(sys.argv[4])
        t2 = time.time()
        print('Duration: ' + time.strftime('%H:%M:%S', time.gmtime(t2-t1)))

