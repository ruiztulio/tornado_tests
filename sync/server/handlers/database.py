#!/usr/bin/python
# -*- coding: utf-8 -*-

from tornado.options import options
import logging
import base
import json
from syncronizer_base import SyncronizerBase

gen_log = logging.getLogger("tornado.general")

class DatabaseHandler(base.BaseHandler):
    def get(self, p):
        dm = options.DabaseManager()
        action = self.get_argument('action', False)
        res = {}
        if action == 'list_tables':
            tables = dm.list_tables()
            res = {'status': {'id': 'OK', 'message': ''}, 'tables': tables}
        elif action == 'query':
            table = self.get_argument('table', False)
            ids = self.get_argument('ids', False)
            if not table or not dm.search_table(table):
                res = {'status': {'id': 'ERROR', 'message': 'Ne se encuentra la tabla'}}
            elif ids:
                rows = dm.query(table, ids=json.loads(ids))
                res = {'status': {'id': 'OK', 'message': ''}, 'rows': rows}
            else:
                rows = dm.query(table)
                res = {'status': {'id': 'OK', 'message': ''}, 'rows': rows}
        elif action == 'query_sync':
            table = self.get_argument('table', False)
            if not table or not dm.search_table(table):
                res = {'status': {'id': 'ERROR', 'message': 'Ne se encuentra la tabla'}}
            else:
                rows = dm.query_sync(table)
                res = {'status': {'id': 'OK', 'message': ''}, 'rows': rows}
        else:
        	res = {'status': {'id': 'ERROR', 'message': 'Metodo no encontrado'}}
        self._send_response(res)

    def post(self, p):
        action = self.get_argument('action', False)
        res = {}
        table = self.get_argument('table', None)
        data = json.loads(self.get_argument('data', None))
        if action == 'sync_this':
            res.update({'status': {'id': 'OK', 'message': ''}})
            if data:
                sync = SyncronizerBase(options.DabaseManager)
                r = sync.sync_this(data, table)
                res.update({'response' :  r})
        elif action == 'sync':
            res.update({'status': {'id': 'OK', 'message': ''}})
            sync = SyncronizerBase(options.DabaseManager)
            r = sync.sync(data, table)
            res.update({'response' :  r})
        elif action == 'upload':
            dm = options.DabaseManager()
            dm.save(data, table)
        else:
            res.update({'status': {'id': 'ERROR', 'message': 'Accion no reconocida %s'%action}})
        self._send_response(res)


