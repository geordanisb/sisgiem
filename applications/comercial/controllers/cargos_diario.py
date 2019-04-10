# -*- coding: utf-8 -*-
def index():
    titulo = "Cargos Diarios desde SGC"
    grid = SQLFORM.grid(db.cargos_diario)
    return response.render("default/index.html",
                           dict(titulo=titulo, contenido=grid, link_activo="sop_comercial"))

def detalles():
    id = request.args(0,cast=int)
    titulo = "Detalles del Cargo Diario"
    cargo = db.cargos_diario(id)
    contenido = ""
    if cargo:
        btn_back = A(I(_class="glyphicon glyphicon-arrow-left")," Regresar",_href=request.env.HTTP_REFERER,_class="btn btn-default")
        contenido = DIV(btn_back, SQLFORM(db.cargos_diario,cargo,readonly=True))
    return response.render("default/index.html",
                           dict(titulo=titulo, contenido=contenido, link_activo="sop_comercial"))

def cargos_por_conexion_emp_mlc():
    query = (db.cargos_diario.servicio == db.conexiones_por_deuda.servicio)
    query &= db.cargos_diario.moneda == "MLC"
    query &= ((db.cargos_diario.oficina == 301) | (db.cargos_diario.oficina == 320))

    titulo = "Cargos por conexión Sector Empresarial en MLC"
    db.conexiones_por_deuda.oficina.readable = 0
    db.conexiones_por_deuda.servicio.readable = 0
    contenido = DIV(SQLFORM.grid(query))
    return response.render("default/index.html",
                           dict(titulo=titulo, contenido=contenido, link_activo="sop_comercial"))

def cargos_por_conexion_emp_mn():
    query = (db.cargos_diario.servicio == db.conexiones_por_deuda.servicio)
    query &= db.cargos_diario.moneda == "MN"
    query &= ((db.cargos_diario.oficina == 301) | (db.cargos_diario.oficina == 320))

    titulo = "Cargos por conexión Sector Empresarial en MN"
    db.conexiones_por_deuda.oficina.readable = 0
    db.conexiones_por_deuda.servicio.readable = 0
    contenido = DIV(SQLFORM.grid(query))
    return response.render("default/index.html",
                           dict(titulo=titulo, contenido=contenido, link_activo="sop_comercial"))

def cargos_por_conexion_res_mlc():
    query = (db.cargos_diario.servicio == db.conexiones_por_deuda.servicio)
    query &= db.cargos_diario.moneda == "MLC"
    query &= ((db.cargos_diario.oficina != 301) & (db.cargos_diario.oficina != 320))

    titulo = "Cargos por conexión Sector Residencial en MLC"
    db.conexiones_por_deuda.oficina.readable = 0
    db.conexiones_por_deuda.servicio.readable = 0
    contenido = DIV(SQLFORM.grid(query))
    return response.render("default/index.html",
                           dict(titulo=titulo, contenido=contenido, link_activo="sop_comercial"))

def cargos_por_conexion_res_mn():
    query = (db.cargos_diario.servicio == db.conexiones_por_deuda.servicio)
    query &= db.cargos_diario.moneda == "MN"
    query &= ((db.cargos_diario.oficina != 301) & (db.cargos_diario.oficina != 320))

    titulo = "Cargos por conexión Sector Residencial en MN"
    db.conexiones_por_deuda.oficina.readable = 0
    db.conexiones_por_deuda.servicio.readable = 0
    contenido = DIV(SQLFORM.grid(query))
    return response.render("default/index.html",
                           dict(titulo=titulo, contenido=contenido, link_activo="sop_comercial"))

def conexiones_sin_cargos():
    titulo = "Servicios conectados sin aplicar cargos miscelaneos"
    session.forget(response)
    query_db = db.cargos_diario.servicio==None
    query = db.cargos_diario.on(db.conexiones_por_deuda.servicio == db.cargos_diario.servicio)
    fields = [db.conexiones_por_deuda.servicio,db.conexiones_por_deuda.oficina,db.conexiones_por_deuda.fecha_conexion,
              db.conexiones_por_deuda.conectado_por]
    grid = SQLFORM.grid(query_db,left=query,fields=fields,orderby=db.conexiones_por_deuda.oficina)
    contenido = grid

    return response.render("default/index.html",
                           dict(titulo=titulo, contenido=contenido, link_activo="sop_comercial"))

def cargos_sin_conexiones():
    titulo = "Servicios con cargos miscelaneos que no fueron conectados"
    #session.forget(response)
    query_db = db.conexiones_por_deuda.servicio==None
    query_db &= db.cargos_diario.concepto <> "38"
    query = db.conexiones_por_deuda.on(db.cargos_diario.servicio == db.conexiones_por_deuda.servicio)
    fields = [db.cargos_diario.servicio,db.cargos_diario.nombreEmpleado,db.cargos_diario.oficina,
              db.cargos_diario.fecha]
#db.define_table("cargos_diario",fecha,	idAgrupacion,	moneda,	tipoMoneda,	unidad,	segmentacion,	numCuentaBancaria,	ciclo,	oficina,	concepto,	claveLocalidad,	servicio,	estado,	importe,	userName,	cierreDiario,	cierreMensual,	nombreEmpleado,	idUsuario,migrate=1)
    grid = SQLFORM.grid(query_db,left=query,fields=fields,orderby=db.cargos_diario.oficina)
    contenido = grid
    return response.render("default/index.html",
                           dict(titulo=titulo, contenido=contenido, link_activo="sop_comercial"))


@auth.requires(auth.has_membership("administrador") or auth.has_membership("editor_comercial"))
def importar():
    import os, sys

    sys.path.append(os.path.join("site-packages", "xlrd"))
    titulo = "Importar Cargos Diario desde SGC"
    uploadfolder = os.path.join(request.folder, 'uploads')

    form = SQLFORM.factory(Field("file", "upload", label="Archivo desde SGC", requires=IS_NOT_EMPTY(), uploadfolder=uploadfolder))
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

    tabla = "cargos_diario"
    book = open_workbook(archivo)
    sheet = book.sheet_by_index(0)
    campos = db[tabla]._fields[1:]
    db[tabla].truncate('RESTART IDENTITY CASCADE')
    numeros_oficinas = [n.numero for n in db(db.ofic_comercial).select()]
    for row in range(1, sheet.nrows):
        valores = sheet.row_values(row,0)

        dict_ = dict(zip(campos, valores))
        if dict_["servicio"]:
            if int(dict_["oficina"]) in numeros_oficinas:  # importar solo mtz
                db[tabla].insert(**dict_)