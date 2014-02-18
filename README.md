import
======

An xmlrpc script to insert customers into an openerp 7 database

**csv_parser**

A csv parser (parse nothing for now, just give all the rows one by one)

**manager**

Contain the ServerProxy and the socket, plus some usefull methods.

**insert**

The insertion script. Modify this to suit your needs.

##TODO:

* generalize for res.partner (suppliers, clients)
* later, the script will be able to connect partners together (contacts into companies for example)