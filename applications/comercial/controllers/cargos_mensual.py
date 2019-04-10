# -*- coding: utf-8 -*-
def index():
    titulo = "Cargos Mensuales desde SGC"
    grid = SQLFORM.grid(db.cargos_mensual)
    return response.render("default/index.html",
                           dict(titulo=titulo, contenido=grid, link_activo="sop_comercial"))

def detalles():
    id = request.args(0,cast=int)
    titulo = "Detalles del Cargo Mensual"
    cargo = db.cargos_mensual(id)
    contenido = ""
    if cargo:
        contenido = SQLFORM(db.cargos_mensual,cargo,readonly=True)
    return response.render("default/index.html",
                           dict(titulo=titulo, contenido=contenido, link_activo="sop_comercial"))

def cargos_por_conexion_emp_mlc():
    query = (db.cargos_mensual.servicio == db.conexiones_por_deuda.servicio)
    query &= db.cargos_mensual.moneda == "MLC"
    query &= ((db.cargos_mensual.oficina == 301) | (db.cargos_mensual.oficina == 320))

    titulo = "Cargos por conexión Sector Empresarial en MLC"
    db.conexiones_por_deuda.oficina.readable = 0
    db.conexiones_por_deuda.servicio.readable = 0
    contenido = DIV(SQLFORM.grid(query))
    return response.render("default/index.html",
                           dict(titulo=titulo, contenido=contenido, link_activo="sop_comercial"))

def cargos_por_conexion_emp_mn():
    query = (db.cargos_mensual.servicio == db.conexiones_por_deuda.servicio)
    query &= db.cargos_mensual.moneda == "MN"
    query &= ((db.cargos_mensual.oficina == 301) | (db.cargos_mensual.oficina == 320))

    titulo = "Cargos por conexión Sector Empresarial en MN"
    db.conexiones_por_deuda.oficina.readable = 0
    db.conexiones_por_deuda.servicio.readable = 0
    contenido = DIV(SQLFORM.grid(query))
    return response.render("default/index.html",
                           dict(titulo=titulo, contenido=contenido, link_activo="sop_comercial"))

def cargos_por_conexion_res_mlc():
    query = (db.cargos_mensual.servicio == db.conexiones_por_deuda.servicio)
    query &= db.cargos_mensual.moneda == "MLC"
    query &= ((db.cargos_mensual.oficina != 301) & (db.cargos_mensual.oficina != 320))

    titulo = "Cargos por conexión Sector Residencial en MLC"
    db.conexiones_por_deuda.oficina.readable = 0
    db.conexiones_por_deuda.servicio.readable = 0
    contenido = DIV(SQLFORM.grid(query))
    return response.render("default/index.html",
                           dict(titulo=titulo, contenido=contenido, link_activo="sop_comercial"))

def cargos_por_conexion_res_mn():
    query = (db.cargos_mensual.servicio == db.conexiones_por_deuda.servicio)
    query &= db.cargos_mensual.moneda == "MN"
    query &= ((db.cargos_mensual.oficina != 301) & (db.cargos_mensual.oficina != 320))

    titulo = "Cargos por conexión Sector Residencial en MN"
    db.conexiones_por_deuda.oficina.readable = 0
    db.conexiones_por_deuda.servicio.readable = 0
    contenido = DIV(SQLFORM.grid(query))
    return response.render("default/index.html",
                           dict(titulo=titulo, contenido=contenido, link_activo="sop_comercial"))

def conexiones_sin_cargos():
    titulo = "Servicios conectados sin aplicar cargos miscelaneos"
    session.forget(response)
    query_db = db.cargos_mensual.servicio==None
    db.conexiones_por_deuda.id.readable = 1

    query = db.cargos_mensual.on(db.conexiones_por_deuda.servicio == db.cargos_mensual.servicio)
    fields = [db.conexiones_por_deuda.servicio,db.conexiones_por_deuda.oficina,db.conexiones_por_deuda.fecha_conexion,
              db.conexiones_por_deuda.conectado_por]
    grid = SQLFORM.grid(query_db,left=query,fields=fields,orderby=db.conexiones_por_deuda.oficina)
    contenido = grid
    return response.render("default/index.html",
                           dict(titulo=titulo, contenido=contenido, link_activo="sop_comercial"))

def cargos_sin_conexiones():
    titulo = "Servicios con cargos miscelaneos que no fueron conectados"
    session.forget(response)
    query_db = db.conexiones_por_deuda.servicio==None
    query_db &= db.cargos_mensual.concepto <> "38"
    query = db.conexiones_por_deuda.on(db.cargos_mensual.servicio == db.conexiones_por_deuda.servicio)
    fields = [db.cargos_mensual.servicio,db.cargos_mensual.fullUserName,db.cargos_mensual.nombreOficina,
              db.cargos_mensual.oficina,db.cargos_mensual.importe,db.cargos_mensual.moneda,db.cargos_mensual.fechaOperacion]

    db.conexiones_por_deuda.id.readable = 0
    db.conexiones_por_deuda.oficina.readable = 0
    db.conexiones_por_deuda.planta.readable = 0
    db.conexiones_por_deuda.servicio.readable = 0
    db.conexiones_por_deuda.motivo.readable = 0
    db.conexiones_por_deuda.conectado_por.readable = 0
    db.conexiones_por_deuda.fecha_conexion.readable = 0
    grid = SQLFORM.grid(query_db,left=query,fields=fields,orderby=db.cargos_mensual.oficina)
    contenido = grid
    return response.render("default/index.html",
                           dict(titulo=titulo, contenido=contenido, link_activo="sop_comercial"))

@auth.requires(auth.has_membership("administrador") or auth.has_membership("editor_comercial"))
def importar():
    import os, sys

    sys.path.append(os.path.join("site-packages", "xlrd"))
    titulo = "Importar Cargos Mensual desde SGC"
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

    tabla = "cargos_mensual"
    book = open_workbook(archivo)
    sheet = book.sheet_by_index(0)
    db[tabla].truncate('RESTART IDENTITY CASCADE')
    campos = sheet.row_values(0,0)
    numeros_oficinas = [n.numero for n in db(db.ofic_comercial).select()]  # myconf.get('provincia.numeros_oficinas')
    for row in range(1, sheet.nrows):
        valores = sheet.row_values(row,0)

        dict_ = dict(zip(campos, valores))
        if dict_["servicio"]:
                if int(dict_["oficina"]) in numeros_oficinas:  # importar solo mtz
                    v = dict(servicio=dict_["servicio"],fullUserName=dict_["fullUserName"],importe=float(dict_["importe"]),
                         oficina=dict_["oficina"],nombreOficina=dict_["nombreOficina"],concepto=dict_["concepto"],
                         fechaOperacion=dict_["fechaOperacion"],moneda=dict_["moneda"])
                    db[tabla].insert(**v)
