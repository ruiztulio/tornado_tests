#!/usr/bin/python
# -*- coding: utf-8 -*-

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os.path
import sys
sys.path.append('./lib')
from tornado.options import (define, options)
import psycopg2
import psycopg2.extras
#from handlers import (base, products, clients, database)
from handlers import (base, database)
from database import (DatabaseManagerBase, DatabaseManagerPostgres)
define("title", default="Pagina del servidor", help="Page title", type=str)
define("company_name", default="La compania", help="Company name", type=str)
define("port", default=8888, help="run on the given port", type=int)

define("pg_user", default="postgres", help="User for database", type=str)
define("pg_pass", default="postgres", help="User password for database", type=str)
define("pg_host", default="localhost", help="Database server", type=str)
define("pg_dbname", default="sales_sync", help="Database Name", type=str)
define("pg_port", default=5432, help="Database server", type=int)
define("DabaseManager", default=DatabaseManagerPostgres, help="Database server", type= DatabaseManagerBase)

common={
    'title':options.title,
    'company_name':options.company_name,
}

class Application(tornado.web.Application):
    def __init__(self):

        handlers = [
            (r"/", MainHandler),
            (r"/form/([^/]*)", FormHandler),
#            (r"/products([^/]*)", products.ProductHandler),
#            (r"/clients([^/]*)", clients.ClientHandler),
            (r"/database([^/]*)", database.DatabaseHandler),
        ]

        settings = dict(
            template_path = os.path.join(os.path.dirname(__file__), "templates"),
            static_path = os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies = False,
            autoescape = "xhtml_escape",
            debug = True,
        )

        tornado.web.Application.__init__(self, handlers, **settings)
        self.conn = psycopg2.connect("host=%s dbname=%s password=%s user=%s port=%s"%
                            (options.pg_host, options.pg_dbname, options.pg_pass, options.pg_user, options.pg_port))
        self.conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

class MainHandler(tornado.web.RequestHandler):
    """
    En caso de que se desee servir paginas estaticas o plantillas creadas
    para la aplicacion se ejecuta el metodo render y se le indica que plantilla
    es la que va a renderizar y enviar al servidor
    """
    def get(self):
        self.render("index.html", common = common)

class FormHandler(base.BaseHandler):
    """
    En caso de que se desee servir paginas estaticas o plantillas creadas
    para la aplicacion se ejecuta el metodo render y se le indica que plantilla
    es la que va a renderizar y enviar al servidor
    """
    def get(self, param):
        res = {}
        if param:
            self.cursor.execute("SELECT * FROM products WHERE id = %s", (param, ))
            res = copyListDicts( self.cursor.fetchall())
        self.render("form.html", res = res and res[0] or {})

def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

# Se ejecuta la funcion main
if __name__ == "__main__":
    main()
