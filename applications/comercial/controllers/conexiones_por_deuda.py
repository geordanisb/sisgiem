# -*- coding: utf-8 -*-
def index():
    #db.conexiones_por_deuda.id.readable = 1
    titulo = "Conexiones por deuda desde SIPREC"
    grid = SQLFORM.grid(db.conexiones_por_deuda)
    return response.render("default/index.html",
                           dict(titulo=titulo, contenido=grid, link_activo="sop_comercial"))

def detalles():
    id = request.args(0,cast=int)
    titulo = "Detalles de la Conexión por deuda"
    cargo = db.conexiones_por_deuda(id)
    contenido = ""
    if cargo:
        btn_back = A(I(_class="glyphicon glyphicon-arrow-left")," Regresar",_href=request.env.HTTP_REFERER,_class="btn btn-default")
        contenido = DIV(btn_back, SQLFORM(db.conexiones_por_deuda,cargo,readonly=True))
    return response.render("default/index.html",
                           dict(titulo=titulo, contenido=contenido, link_activo="sop_comercial"))

@auth.requires(auth.has_membership("administrador") or auth.has_membership("editor_comercial"))
def importar():
    import os, sys

    sys.path.append(os.path.join("site-packages", "xlrd"))
    titulo = "Importar Conexiones por deuda desde SIPREC"
    uploadfolder = os.path.join(request.folder, 'uploads')

    form = SQLFORM.factory(Field("file", "upload", label="Archivo desde SIPREC", requires=IS_NOT_EMPTY(), uploadfolder=uploadfolder))
    if form.process().accepted:
        try:
            path = os.path.join(uploadfolder, form.vars.file)
            importar_(path)
            os.unlink(path)
        except Exception, e:
            redirect(URL('error', 'index', vars=dict(error=str(e))))
        else:
            redirect(URL('index'))

    contenido = form
    return response.render("default/index.html", dict(titulo=titulo, contenido=contenido,link_activo="sop_comercial"))

def importar_(archivo):
    from xlrd import open_workbook
    import datetime
    tabla = "conexiones_por_deuda"
    book = open_workbook(archivo)
    sheet = book.sheet_by_index(0)
    campos = db[tabla]._fields[1:]
    db[tabla].truncate('RESTART IDENTITY CASCADE')

    for row in range(4, sheet.nrows):
        valores = sheet.row_values(row,1)
        from xlrd import xldate

        dict_ = dict(zip(campos, valores))
        dict_["servicio"] = dict_["servicio"].replace(" ","")
        fecha = xldate.xldate_as_tuple(dict_["fecha_conexion"], 0)
        dict_["fecha_conexion"] = datetime.datetime(*fecha)

        db[tabla].insert(**dict_)