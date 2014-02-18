import_generic
==============

An xmlrpc script to insert or update data into an openerp 7 database

**csv_parser**

A csv parser (parse nothing for now, just give all the rows one by one)

**manager**

Contain the ServerProxy and the socket, plus some usefull methods.

**insert_something**

The insertion scripts. Modify these to suit your needs, or create a new one.

##TODO:

* generalize for res.partner (suppliers, customers)
* later, the script will be able to connect partners together (contacts into companies for example)