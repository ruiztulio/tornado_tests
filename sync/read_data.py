import urllib
import urllib2
import json

url = "http://corprocessu.com:8888/login?login=admin&pswd=81dc9bdb52d04dc20036dbd8313ed055"

def print_dict(valores):
    # Nos aseguramos que sea un diccionario
    if isinstance(valores, dict):
        for i in valores:
            print "%s : %s"%(i, valores.get(i))
    
def print_list(valores, index = False):
    # Nos aseguramos que sea una lista
    if isinstance(valores, list):
        # Si se quieren los valores de la lista sin indices
        if not index:
            for i in valores:
                print "%s "%(i)
        # Si se quieren con indices
        else:
            for i in xrange(len(valores)):
                print "%s : %s"%(i, valores[i])
            
    
# Simplementa se arma el request, esto no hace ninguna consulta
req = urllib2.Request(url)

# Ahora se intenta realizar la conexion con la url especificada
response = False
try:
    response = urllib2.urlopen(req)
except:
    print "Hubo un error al conectar con el servidor"


# Si se realizo la conexion
if response:
    # Leemos la respuesta
    the_page = response.read()
    
    # Convertimos el json a un diccionario python
    info = json.loads(the_page)
    
    # Se imprime el diccionario con sus claves
    for i in info:
        print "%s : %s"%(i, info.get(i))
        
        # Si el elemento que se acaba de leer es un diccionario
        print "Valores contenidos en %s "%i
        if isinstance(info.get(i), dict):
            print_dict(info.get(i))

        # Si el elemento que se acaba de leer es una lista
        if isinstance(info.get(i), list):
            print_list(info.get(i))
        
        
