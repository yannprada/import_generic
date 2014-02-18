# -*- coding: utf-8 -*-
#!/usr/bin/python

import xmlrpclib


class Manager(object):
    '''
Manager
=======

Manage the insertion of data into a database.
    '''
    def __init__(self, host, dbname, password):
        self.sock = xmlrpclib.ServerProxy(host + '/xmlrpc/object', allow_none=True)
        self.uid = 1
        self.db = dbname
        self.pwd = password
    
    def insertOrUpdate(self, ref, model, data, checkList):
        '''
Check the table ir_model_data to see if the ref exist, then insert or update in the given model.
ref: external reference
model: name of the related model
data: data to insert/update
return: id
        '''
        if ref in checkList:
            ID = checkList[ref]
            self.write(model, [ID], data)
        else:
            ID = self.create(model, data)
            data_model = {
                'name': ref,
                'model': model,
                'res_id': ID,
            }
            ir_model_data_id = self.create('ir.model.data', data_model)
        return ID
    
    def list_to_object(self, data, fieldKey, fieldValue):
        '''
Transform a list of objects like this:
[{name: Dupont, ref: ex12t}, ...]
into an object like this one:
{Dupont: ex12t, ...}
        '''
        result = {}
        for item in data:
            result[item[fieldKey]] = item[fieldValue]
        return result
    
    def prepare_many2one(self, model):
        '''
Search all the records for a given model, then returns an object with name as key and id as value.
Usefull when a name is given in the csv file for a many2one relation.
        '''
        ids = self.search(model, [])
        data = self.read(model, ids, ['name'])
        data = self.list_to_object(data, 'name', 'id')
        data[''] = False
        return data
    
    def prepare_ir_model_data(self, model):
        '''
Search all the records in ir.model.data for a given model, then returns an object with ref as key and id as value.
        '''
        ids = self.search('ir.model.data', [('model', '=', model)])
        data = self.read('ir.model.data', ids, ['name', 'res_id'])
        return self.list_to_object(data, 'name', 'res_id')
    
    def search(self, model, args):
        return self.sock.execute(self.db, self.uid, self.pwd, model, 'search', args)    
    
    def read(self, model, ids, fields):
        return self.sock.execute(self.db, self.uid, self.pwd, model, 'read', ids, fields)    
    
    def create(self, model, data):
        return self.sock.execute(self.db, self.uid, self.pwd, model, 'create', data)    
    
    def write(self, model, ids, data):
        return self.sock.execute(self.db, self.uid, self.pwd, model, 'write', ids, data)    
    
    def unlink(self, model, ids):
        return self.sock.execute(self.db, self.uid, self.pwd, model, 'unlink', ids)

