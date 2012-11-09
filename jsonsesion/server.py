import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os.path
import sys
from tornado.options import (define, options)
import psycopg2
import psycopg2.extras
from tornado.escape import (json_decode, json_encode)

define("title", default="Pagina de prueba", help="Page title", type=str)
define("company_name", default="La compania", help="Company name", type=str)
define("port", default=8888, help="run on the given port", type=int)

define("pg_user", default="testrest", help="User for database", type=str)
define("pg_pass", default="123", help="User password for database", type=str)
define("pg_host", default="localhost", help="Database server", type=str)
define("pg_dbname", default="rest_sales", help="Database server", type=str)
define("pg_port", default=5432, help="Database server", type=int)

def copyListDicts(lines):
    res = []
    for line in lines:
        d = {}
        for l in line.keys():
            d.update({l : line[l]})
        res.append(d.copy())
    return res

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/login([^/]*)", LoginHandler),
        ]
        settings = dict(
            cookie_secret="43oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            login_url="/auth/login",
            xsrf_cookies=False,
            autoescape="xhtml_escape",
        )
        tornado.web.Application.__init__(self, handlers, **settings)
        self.conn = psycopg2.connect("host=%s dbname=%s password=%s user=%s port=%s"%
                            (options.pg_host, options.pg_dbname, options.pg_pass, options.pg_user, options.pg_port))
        self.conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

class LoginHandler(tornado.web.RequestHandler):
    @property
    def cursor(self):
        return self.application.cur

    def _get_login(self):
        sql = "SELECT * FROM cor_seg_users"
        if self.login and self.pswd:
            sql += " WHERE "
            sql = self.cursor.mogrify(sql + " login = %s and pswd = %s", (self.login, self.pswd,))
        print sql
        self.cursor.execute(sql)
        res = copyListDicts( self.cursor.fetchall())
        ret = {}
        if res:
            ret.update({'login':res, 'status':{'id':'OK', 'message':''}})
        else:
            ret.update({'login':[], 'status':{'id':'ERROR', 'message':'Nombre de usuario y/o clave incorrecto'}})
        return  ret

		
    def _login_callback(self):
        res = self._get_login()
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        #res = json.dumps(res, default=json_handler)
        res = json_encode(res)
        if self.callback:
            res = "%s(%s)"%(self.callback, res,)
        self.write(res)
        print res
        self.finish()

    @tornado.web.asynchronous
    def get(self, *args, **kwargs):
        print self.request.headers
        self.login = self.get_argument('login', '')
        self.pswd = self.get_argument('pswd', '')
        self.callback = self.get_argument('callback', '')
        self._login_callback()

class MainHandler(tornado.web.RequestHandler):
    """
    En caso de que se desee servir paginas estaticas o plantillas creadas
    para la aplicacion se ejecuta el metodo render y se le indica que plantilla
    es la que va a renderizar y enviar al servidor
    """
    def get(self):
        print self.request.headers
        self.render("index.html", common = common)


def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

# Se ejecuta la funcion main
if __name__ == "__main__":
    main()
