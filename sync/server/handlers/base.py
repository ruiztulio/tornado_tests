import tornado.web
import json
import logging
from utils import json_handler

gen_log = logging.getLogger("tornado.general")

class BaseHandler(tornado.web.RequestHandler):

    @property
    def cursor(self):
        return self.application.cur

    def _send_response(self, res):
        self.set_header("Content-Type", "application/json")
        try:
        	self.write(json.dumps(res, default=json_handler))
        except Exception:
            res.update({'status':{'id' : 'ERROR', 'message' : 'Hubo un error, no se pudo ejecutar la operacion'}})
            self.write(json.dumps(res))
            gen_log.error('Error ejecutando la operacion', exc_info=True)
        self.finish()
