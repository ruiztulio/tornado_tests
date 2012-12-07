import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os.path
import sys
sys.path.append('./lib')
from tornado.options import (define, options)
#sys.path.append('./')
from utils.list_tables import list_databases
from utils.initializer import create_tables
import psycopg2
import psycopg2.extras
from utils.list_tables import list_tables
import ConfigParser

define("title", default="Generador de clases", help="Page title", type=str)
define("company_name", default="La compania", help="Company name", type=str)
define("port", default=8881, help="run on the given port", type=int)

define("pg_user", default="postgres", help="User for database", type=str)
define("pg_pass", default="postgres", help="User password for database", type=str)
define("pg_host", default="localhost", help="Database server", type=str)
define("pg_dbname", default="rest_sales", help="Database server", type=str)
define("pg_port", default=5432, help="Database server", type=int)

common={
    'title':options.title,
    'company_name':options.company_name,
}

class Application(tornado.web.Application):
    def __init__(self):

        handlers = [
            (r"/", MainHandler),
            (r"/config", ConfigHandler),
            (r"/database", DatabaseHandler),
        ]

        settings = dict(
            cookie_secret="43oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            login_url="/auth/login",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=False,
            autoescape="xhtml_escape",
            debug=True,
        )

        tornado.web.Application.__init__(self, handlers, **settings)
        self.conn = psycopg2.connect("host=%s dbname=%s password=%s user=%s port=%s"%
                            (options.pg_host, options.pg_dbname, options.pg_pass, options.pg_user, options.pg_port))
        self.conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        config = ConfigParser.ConfigParser()
        config.read('config.ini')
        configs = {'show_initialize' : False}
        if not os.path.isfile(config.get('application', 'dbname')):
            configs.update({'show_initialize' : True})
        self.render("orbit.html", common = common, config=configs)

class DatabaseHandler(tornado.web.RequestHandler):
    def get(self):
        action = self.get_argument('action', False)
        if action == 'list':
            html = "<select name=\"database\">"
            dbs = list_databases()
            for db in dbs:
                html = "%s <option value=\"%s\">%s</option>"%(html, db.get('name'), db.get('name'))
            html = "%s</select>"%html
        elif action == 'initialize':
            create_tables()
            html = ''
        elif action == 'list_tables':
            tables = list_tables('rest_sales')
            html = self.render_string("table_list.html", tables=tables)

        self.write(html)
        

class ConfigHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("frm_config.html", common = common)

    def post(self):
        options.pg_host = str(self.get_argument('host', ''))
        options.pg_dbname = str(self.get_argument('database', ''))
        options.pg_pass = str(self.get_argument('password', ''))
        options.pg_user = str(self.get_argument('user', ''))
        options.pg_port = int(self.get_argument('port', 5432))
        message = {'id': 'success', 'message': 'Actualizada configuracion correctamente'}
        self.render("message.html", message=message)

def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

# Se ejecuta la funcion main
if __name__ == "__main__":
    main()
