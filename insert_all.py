# -*- coding: utf-8 -*-
#!/usr/bin/python

import sys
import time

from insert_customers import CustomerManager
from insert_categories import CategoryManager
from insert_products import ProductManager

if __name__ == '__main__':
    if len(sys.argv) < 7:
        print('''
Usage:
    python insert_all.py [host] [database] [password] [clientsFile.csv] [categoriesFile.csv] [productsFile.csv]
        ''')
        sys.exit()
    else:
        t1 = time.time()
        m1 = CustomerManager(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], True)
        m2 = CategoryManager(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[5], True)
        m3 = ProductManager(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[6], True)
        t2 = time.time()
        print('Duration: ' + time.strftime('%H:%M:%S', time.gmtime(t2-t1)))

