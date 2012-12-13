import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os.path
import sys
sys.path.append('./lib')
from tornado.options import (define, options)
#sys.path.append('./')
from utils.list_tables import (list_databases, list_tables, save_tables)
from utils.initializer import create_tables
from utils.config_manager import ConfigManager
import ConfigParser

cm = ConfigManager()

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
        options.pg_dbname = cm.get('database', 'database')
        options.pg_user = cm.get('database', 'user')
        options.pg_port = cm.get('database', 'port')
        options.pg_pass = cm.get('database', 'password')
        options.pg_host = cm.get('database', 'host')

        tornado.web.Application.__init__(self, handlers, **settings)

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
                html = "%s <option value=\"%s\" %s>%s</option>"%(html, db.get('name'), db.get('name')==options.pg_dbname and  "selected=\"selected\"" or "" ,db.get('name'))
            html = "%s</select>"%html
        elif action == 'initialize':
            create_tables()
            html = ''
        elif action == 'list_tables':
            tables = cm.get_tables_list()
            html = self.render_string("table_list.html", tables=tables)
        #elif action == 'list_tables_config':

        self.write(html)
        

class ConfigHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("frm_config.html", common = common, options = options)

    def post(self):
        if self.get_argument('action') == 'update_config':
            print "Actualizando config"
            cm.set({'host': str(self.get_argument('host', '')),
                    'password' : str(self.get_argument('password', '')),
                    'database' : str(self.get_argument('database', '')),
                    'user' : str(self.get_argument('user', '')),
                    'port' : int(self.get_argument('port', 5432))})

            options.pg_dbname = cm.get('database', 'database')
            options.pg_user = cm.get('database', 'user')
            options.pg_port = cm.get('database', 'port')
            options.pg_pass = cm.get('database', 'password')
            options.pg_host = cm.get('database', 'host')
            message = {'id': 'success', 'message': 'Actualizada configuracion correctamente'}
        elif self.get_argument('action') == 'update_table_list':
            message = {'id': 'success', 'message': 'Lista obtenida correctamente'}
            tables= self.get_arguments('tables')
            save_tables(tables)
        self.render("message.html", message=message)

def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

# Se ejecuta la funcion main
if __name__ == "__main__":
    main()
