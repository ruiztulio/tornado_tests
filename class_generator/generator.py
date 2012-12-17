import os
from utils.config_manager import ConfigManager

cm = ConfigManager()

def generate_get(config):
    vals = {'name':config.get('table'), 
            'fields':', '.join(config.get('fields')),
            'format':'%',
            }
    res = """
    def get(self, p):
        field_id = self.get_argument('id', False)
        try:
            if field_id:
                self.cursor.execute("SELECT %(fields)s FROM %(name)s WHERE id = %(format)ss", (field_id, ))
            else:
                self.cursor.execute("SELECT %(fields)s FROM %(name)s")
            res = copyListDicts( self.cursor.fetchall() )
            for r in res:
                r.update({'ref' : 'http://%(format)ss/%(name)s?id=%(format)ss'%(format)s(self.request.host, r.get('id'))})
            res = {'%(name)s':res, 'status':{'id' : 'OK', 'message' : ''}}
        except Exception as e:
            res = {'status':{'id' : 'ERROR', 'message' : 'Hubo un error, no se pudo realizar la consulta'}}
            gen_log.error("Error consultando", exc_info=True)
        self._send_response(res)
    
    """%vals
    return res
    
def generate_put(config):
    vals = {'name':config.get('table'), 
            'format':'%',
            'mandatory':'","'.join(config.get('mandatory'))}
    res = """
    def put(self, p):
        field_id = self.get_argument('id', False)
       
        fields = self.request.arguments.keys() 
        res = {'status' : {'id' : 'OK', 'message' : ''}}
        if len(fields) > 1 and field_id:
            sql = "UPDATE %(name)s SET"
            values = []
            for field in fields:
                if field != 'id':
                    sql += " " + field + " = %(format)ss, "
                    values.append(self.get_argument(field))
            sql = sql[:-2] + " WHERE id = %(format)ss"
            values.append(field_id)
            try:
                self.cursor.execute(sql, values)
            except Exception as e:
                res.update({'status':{'id' : 'ERROR', 'message' : 'Hubo un error, no se pudo actualziar el registro'}})
                gen_log.error("Error actualizando el registro", exc_info=True)
        else:
            if not field_id:
                res.update({'status':{'id' : 'ERROR', 'message' : 'El campo id es obligatorio'}})
            else:
                res.update({'status':{'id' : 'ERROR', 'message' : 'Nada que actualizar'}})
        self._send_response(res)
"""%vals
    return res

def generate_delete(config):
    vals = {'name':config.get('table'), 'format':'%'}
    res = """
    def delete(self, p):
        fields = self.request.arguments.keys() 
        field_id = self.get_argument('id', False)
        if not fields:
            params = self.request.body.split('&')
            for p in params:
                if 'id' in p:
                    product = p.split('=')
                    field_id = product[1]
                
        res = {'status' : {'id' : 'OK', 'message' : ''}}
        if field_id:
            try:
                self.cursor.execute("DELETE FROM %(name)s WHERE id = %(format)ss",
                                        (field_id,))
            except Exception as e:
                res.update({'status':{'id' : 'ERROR', 'message' : 'Hubo un error, no se pudo eliminar el registro'}})
                gen_log.error("Error eliminando el registro", exc_info=True)
        else:
            res.update({'status':{'id' : 'ERROR', 'message' : 'Hubo un error, en id es obligatorio'}})
        self._send_response(res)            
    """%vals
    return res
    
def generate_post(config):
    vals = {'name':config.get('table'), 
            'format':'%', 
            'mandatory':'","'.join(config.get('mandatory'))}
    res = """
    def post(self, p):
        obligatorios = ["%(mandatory)s"]
        fields = self.request.arguments.keys()
        f = []
        for field in obligatorios:
            if not field in fields:
                f.append(field)
        res = {'status' : {'id' : 'OK', 'message' : ''}}
        if not f:
            try:
                sql = generate_insert('%(name)s', fields)
                values = [self.get_argument(f) for f in fields]
                self.cursor.execute(sql,values)                                        
            except Exception as e:
                res.update({'status':{'id' : 'ERROR', 'message' : 'Hubo un error, no se pudo crear el registro'}})
                gen_log.error("Error agregando el registro", exc_info=True)
        else:
                res.update({'status':{'id' : 'ERROR', 'message' : 'No se pudo crear registro, faltan campos obligatorios %(format)ss'%(format)sstr(f)}})
            
        self._send_response(res)

    """%vals
    return res

def generate_insert(table, fields):
    sql = 'INSERT INTO %(name)s %(fields)s VALUES %(values)s RETURNING id'
    f = str(tuple(fields))
    v = str(tuple(['%s']*len(fields)))
    return sql%{'name':table, 'fields': f, 'values':v[:-2]}

def generate_all():
    path = os.path.dirname(os.path.realpath(__file__)) + '/output'

    if not os.path.isdir(path):
        print 'No existe el directorio de salida'
        os.mkdir('output')
    if not os.path.isfile('config.ini'):
        print 'No existe archivo de configuracion'
    models =  cm.get_tables_list(use=True)
    for model in models:
        methods=cm.get_methods(model[0])
        class_name=model[2]
        imports=cm.get('model', 'imports')
        base=cm.get('model', 'base')

        text_file = open("output/%s.py"%model[1], "w")
        text_file.write(imports)
        text_file.write("\n\ngen_log = logging.getLogger(\"tornado.general\")\n\n")
        text_file.write("")
        text_file.write("class %s(%s):"%(class_name, base))
        text_file.write("\n    SUPPORTED_METHODS = (\"%s\")"%'","'.join(methods))
        if 'GET' in methods:
            text_file.write(generate_get({'table':model[1], 'fields':cm.get_methods_fields('GET', model[0], use=True)}))
        if 'POST' in methods:
            text_file.write(generate_post({'table':model[1], 'mandatory': cm.get_methods_fields('POST', model[0], use=True)}))
        if 'DELETE' in methods:
            text_file.write(generate_delete({'table':model[1]}))
        if 'PUT' in methods:
            text_file.write(generate_put({'table':model[1], 'mandatory': cm.get_methods_fields('PUT', model[0], use=True)}))

        text_file.close()

        print base


