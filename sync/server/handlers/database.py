#!/usr/bin/python
# -*- coding: utf-8 -*-

from tornado.options import options
import logging
import base
import json

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
            if not table or not dm.search_table(table):
                res = {'status': {'id': 'ERROR', 'message': 'Ne se encuentra la tabla'}}
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
        #elif action == 'list_tables_config':
        self._send_response(res)

    def post(self, p):
        dm = options.DabaseManager()
        action = self.get_argument('action', False)
        res = {}
        if action == 'sync_this':
            res.update({'status': {'id': 'OK', 'message': ''}})
            data = json.loads(self.get_argument('data', None))
            if data:
                for d in data:
                    print d.get('id')
        self._send_response(res)


