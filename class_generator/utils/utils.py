from decimal import Decimal

def copyListDicts(lines):
    res = []
    for line in lines:
        d = {}
        for l in line.keys():
            d.update({l : line[l]})
        res.append(d.copy())
    return res

def generate_insert(table, fields):
    sql = 'INSERT INTO %(name)s %(fields)s VALUES %(values)s'
    f = str(tuple(fields)).replace("'", "")
    v = str(tuple(['%s']*len(fields))).replace("'", "")
    print sql%{'name':table, 'fields': f, 'values':v}
    return sql%{'name':table, 'fields': f, 'values':v}
