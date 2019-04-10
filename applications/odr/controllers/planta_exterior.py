create = deletable = editable = auth.has_membership('editor_odr')
def index():
    titulo = "Planta Exterior - Acciones"
    contenido = MENU(response.menu_pe)
    return response.render("default/index.html", dict(titulo=titulo, contenido=contenido))

def facilidades_pe():
    titulo = "Facilidades de Planta Exterior"
    db.facilidades_pe.id.readable = 0
    form = SQLFORM.grid(db.facilidades_pe)
    return response.render("default/index.html", dict(titulo=titulo, contenido=form))

def servicios_nauta_hogar():
    titulo = "Servicios Nauta Hogar"
    db.servicios_nauta_hogar.id.readable = 0
    query = db.servicios_nauta_hogar.servicio_pe ==  db.facilidades_pe.servicio
    form = SQLFORM.grid(query)
    return response.render("default/index.html", dict(titulo=titulo, contenido=form))

def importar_servicios_comercializables():
    import os, sys
    sys.path.append(os.path.join("site-packages", "xlrd"))
    titulo = "Importar servicios comercializables"
    uploadfolder = os.path.join(request.folder, 'uploads')
    v=[]
    form = SQLFORM.factory(
        Field('servicios', 'upload', label="Importar Servicios Nauta Hogar (archivo de una sola columna)",
              requires=IS_NOT_EMPTY(error_message="Seleccione el archivo (csv)."), uploadfolder=uploadfolder),

    )
    if form.process().accepted:
        try:
            path = os.path.join(uploadfolder, form.vars.servicios)

            from xlrd import open_workbook
            tabla = "servicios_nauta_hogar"
            book = open_workbook(path)
            sheet = book.sheet_by_index(0)
            db[tabla].truncate('RESTART IDENTITY CASCADE')
            for row in range(0, sheet.nrows):
                valores = sheet.row_values(row, 0)
                servicio = str(valores[0]).split(".")[0]
                record = db(db.facilidades_pe.servicio == servicio).select().first()
                if (record):
                    record = db(db[tabla].servicio_pe == servicio).select().first()
                    if(not record):
                        db[tabla].insert(servicio_pe=servicio)
                    else:
                        v.append(dict(error="ya existe el servicio nauta",servicio=servicio))
                else:
                    v.append(dict(error="no existe la facilidad",servicio=servicio))
            os.unlink(path)
        except Exception, e:
            redirect(URL('error', 'index', vars=dict(error=str(e))))
        """else:
            redirect(URL('planta_exterior', 'servicios_nauta_hogar'))"""

    return response.render("default/index.html", dict(titulo=titulo, contenido=DIV(form,v)))

def importar_facilidades():
    import os, sys

    sys.path.append(os.path.join("site-packages", "xlrd"))
    titulo = "Importar archivo facilidades de Planta Ext. desde SIPREC"
    uploadfolder = os.path.join(request.folder, 'uploads')
    cont = ""
    v = []
    form = SQLFORM.factory(
        Field('facilidades', 'upload', label="Facilidades de Planta Ext. desde SIPREC",
              requires=IS_NOT_EMPTY(error_message="Seleccione el archivo (csv)."), uploadfolder=uploadfolder),

    )
    if form.process().accepted:
        try:
            path = os.path.join(uploadfolder, form.vars.facilidades)
            cont = popular_facilidades_pe(path)
            os.unlink(path)
        except Exception, e:
            redirect(URL('error', 'index', vars=dict(error=str(e))))
        """else:
            redirect(URL('planta_exterior', 'facilidades_pe'))"""

    return response.render("default/index.html", dict(titulo=titulo, contenido=DIV(form,cont)))

def popular_facilidades_pe(archivo):
    from xlrd import open_workbook
    from Excepciones import NotCentral

    tabla = "facilidades_pe"
    book = open_workbook(archivo)
    sheet = book.sheet_by_index(0)
    campos = db[tabla]._fields[1:]
    #db[tabla].truncate('RESTART IDENTITY CASCADE')
    v = []
    count = sheet.nrows
    for row in range(11, sheet.nrows):
        try:
            valores = sheet.row_values(row, 0)
            ruta = valores[18].split(",")

            servicio = str(valores[2]).replace(" ","")
            tipo_servicio = valores[4]
            sector = valores[8]
            no_traza = valores[15]
            soporte = valores[16]
            par_en_rack = ruta[0]
            cable = ruta[1]
            par = ruta[2]
            terminal = ruta[3]
            direccion = valores[22]
            circuito_de_linea = valores[23]
            sitio = valores[24]
            central = valores[25]
            record = db(db[tabla].servicio == servicio).select().first()
            if(not record):
                db[tabla].insert(servicio=servicio,tipo_servicio=tipo_servicio,sector=sector,no_traza=no_traza,soporte=soporte,par_en_rack=par_en_rack,cable=cable,par=par,terminal=terminal,direccion=direccion,circuito_de_linea=circuito_de_linea,\
                             sitio=sitio,central=central)
            else:
                if valores[21].replace(" ","") != "1":
                    record.update_record(servicio=servicio,tipo_servicio=tipo_servicio,sector=sector,no_traza=no_traza,soporte=soporte,par_en_rack=par_en_rack,cable=cable,par=par,terminal=terminal,direccion=direccion,circuito_de_linea=circuito_de_linea,\
                             sitio=sitio,central=central)
        except Exception,e:
            v.append(str(e))


    return v