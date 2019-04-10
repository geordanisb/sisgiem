def index():
    titulo = "Soporte comercial"
    contenido = MENU(response.sop_comercial)
    return response.render("default/index.html",dict(titulo=titulo,contenido=contenido))

def cargos():
    db.cargos.id.readable = False
    grid = SQLFORM.grid(db.cargos)
    return response.render("default/index.html", dict(titulo="Cargos", contenido=grid))

def importar_conexiones_(path):
    import os,csv,datetime
    if os.path.isfile(path):
        with open(path,"rb") as f:
            dialect = csv.Sniffer().sniff(f.read(), delimiters=';,')
            f.seek(0)
            reader = csv.DictReader(f, dialect=dialect)

            db.conexiones.truncate('RESTART IDENTITY CASCADE')
            for r in reader:
                if r["servicio"]:
                    r["servicio"] = r["servicio"].replace(" ","")
                if r["fecha_conexion"]:
                    _datetime = datetime.datetime.strptime(r["fecha_conexion"],"%m/%d/%Y %H:%M:%S %p")#fecha_reporte
                    r["fecha_conexion"] = _datetime
                if r["fecha_conexion"]!="": db.conexiones.insert(**r)
        os.unlink(path)

def importar_cargos_(path):
    import os,csv,datetime
    if os.path.isfile(path):
        with open(path,"rb") as f:
            dialect = csv.Sniffer().sniff(f.read(), delimiters=';,')
            f.seek(0)
            reader = csv.DictReader(f, dialect=dialect)

            db.cargos.truncate('RESTART IDENTITY CASCADE')
            for r in reader:
                if r["servicio"]:
                    r["servicio"] = r["servicio"].replace(" ","")
                db.cargos.insert(**r)
        os.unlink(path)

@auth.requires(auth.has_membership("administrador") or auth.has_membership("editor_comercial"))
def importar_cargos():
    import csv, os
    session.forget(response)
    uploadfolder = os.path.join(request.folder, "uploads")
    form = SQLFORM.factory(Field("file", "upload", requires=IS_NOT_EMPTY(), uploadfolder=uploadfolder))
    if form.process().accepted:
        path = os.path.join(uploadfolder, form.vars.file)
        importar_cargos_(path)

    aviso = DIV(
        "Para poder importar la tabla de cargos, exportela como archivo separado por coma (csv) y nombre las columnas de la siguiente forma: fecha, idAgrupacion, moneda, tipoMoneda, unidad, segmentacion, numCuentaBancaria, ciclo, oficina, concepto, claveLocalidad, servicio, estado, importe, userName, cierreDiario, cierreMensual, nombreEmpleado,	idUsuario.",
        _class="alert alert-warning")
    contenido = DIV(aviso, form)
    return response.render("default/index.html",
                               dict(titulo="Importar cargos", contenido=contenido, link_activo="sop_comercial"))

@auth.requires(auth.has_membership("administrador") or auth.has_membership("editor_comercial"))
def importar_conexiones():
    import csv, os
    #session.forget(response)
    uploadfolder = os.path.join(request.folder, "uploads")
    form = SQLFORM.factory(Field("file", "upload", requires=IS_NOT_EMPTY(), uploadfolder=uploadfolder))
    if form.process().accepted:
        path = os.path.join(uploadfolder, form.vars.file)
        importar_conexiones_(path)

    aviso = DIV("Para poder importar la tabla de conexiones, exportela como archivo separado por coma (csv) y nombre las columnas de la siguiente forma: planta, oficina, servicio, motivo, fecha_conexion, conectado_por",_class="alert alert-warning")
    contenido = DIV(aviso,form)
    return response.render("default/index.html", dict(titulo="Importar conexiones", contenido=contenido,link_activo="sop_comercial"))

def conexiones():
    db.conexiones.id.readable = False
    grid = SQLFORM.grid(db.conexiones)
    return response.render("default/index.html", dict(titulo="Conexiones", contenido=grid))

def conexiones_sin_cargos():
    titulo = "Conexiones sin cargos"
    con = db(db.conexiones.id>0).select(db.conexiones.ALL)
    th = TR(TH("Planta"),TH("Oficina"),TH("Servicio"),TH("Motivo"),TH("Fecha de conexión"),TH("Conectado por"),_class="info")
    thead = THEAD(th)
    tbody = TBODY()
    table = TABLE(thead,tbody,_class="table table-bordered")
    for c in con:
        cargos = db(db.cargos.servicio == c.servicio.strip()).select(cache=(cache.ram,300),cacheable=False)
        if not cargos:
            tr = TR(TD(c.planta),TD(c.oficina),TD(c.servicio),TD(c.motivo),TD(c.fecha_conexion),TD(c.conectado_por))
            tbody.append(tr)
    return response.render("default/index.html",dict(titulo=titulo,contenido=table))

def cargos_sin_conexiones():
    session.forget(response)
    titulo = "Cargos sin conexiones"

    th = TR(TH("Empleado"), TH("Oficina"), TH("Servicio"), TH("Moneda"), TH("Fecha"), TH("Importe"), _class="info")
    thead = THEAD(th)
    tbody = TBODY()
    table = TABLE(thead, tbody, _class="table table-bordered")
    total = 0
    conexiones = [c.servicio for c in db(db.conexiones).select(db.conexiones.servicio, distinct=1, cache=(cache.ram, 300), cacheable=1)]
    cargos = db(db.cargos).select(db.cargos.ALL,cacheable=1)

    for c in cargos.exclude(lambda c: not c.servicio in conexiones):
        tr = TR(TD(c.nombreEmpleado), TD(c.oficina), TD(c.servicio), TD(c.moneda), TD(c.fecha), TD(c.importe))
        tbody.append(tr)
        total += 1

    total = SPAN(B("Total: "),I("%s" % total,_class="text-danger"))
    contenido = DIV(total, table)
    return response.render("default/index.html", dict(titulo=titulo, contenido=contenido))

def cargos_repetidos():
    session.forget(response)
    titulo = "Cargos repetidos"
    con = db(db.cargos.id > 0).select(db.cargos.ALL)
    th = TR(TH("Empleado"), TH("Oficina"), TH("Servicio"), TH("Moneda"), TH("Fecha"), TH("Importe"),_class="info")
    thead = THEAD(th)
    tbody = TBODY()
    table = TABLE(thead, tbody, _class="table table-bordered")
    servicios = []
    total = 0
    for c in con:
        cargos = db(db.cargos.servicio == c.servicio).count()
        if cargos > 1:
            if c.servicio not in servicios:
                tr = TR(TD(c.nombreEmpleado), TD(c.oficina), TD(c.servicio), TD(c.moneda), TD(c.fecha), TD(c.importe))
                tbody.append(tr)
                servicios.append(c.servicio)
                total += 1
    total = SPAN(B("Total: "), I("%s" % total, _class="text-danger"))
    contenido = DIV(total, table)
    return response.render("default/index.html", dict(titulo=titulo, contenido=contenido))


#**********************para unir archivos edad de cuenta******************

def reporte_edad_cuenta():
    db.cuentas_edad.id.readable = False
    grid = SQLFORM.grid(db.cuentas_edad)
    return response.render("default/index.html", dict(titulo="Edad de la Cuenta N DIAS", contenido=grid))

def importar_desde_archivo(archivo,edad):
    from xlrd import open_workbook
    import datetime

    book = open_workbook(archivo)
    sheet = book.sheet_by_index(0)
    tabla = "cuentas_edad"
    #campos = db[tabla]._fields[1:]
    moneda = ""

    for i,row in enumerate(range(1,sheet.nrows)):
        valores = sheet.row_values(row, 0)

        if valores[0] == "Moneda MLC": moneda = "MLC"
        if valores[0] == "Moneda MN": moneda = "MN"

        if valores[0] == "Segmento PT":
            for r in (range(i+1,sheet.nrows)):
                v = sheet.row_values(r, 0)
                if not v[0].startswith("SubTotal Segmento") and not v[0].startswith("Segmento"):
                    dict_ = {}#{"treinta":0,"sesenta":0,"noventa":0,"mas_de_90":0}
                    dict_["no_agrupacion"] = v[0]
                    dict_["sg"] = v[4]
                    dict_["nomb_agrupacion"] = v[6]
                    dict_["moneda"] = moneda
                    dict_[edad] = v[19]
                    record = db(db[tabla].no_agrupacion == dict_["no_agrupacion"])(db[tabla].moneda == dict_["moneda"]).select().first()
                    if record:
                        record.update_record(**dict_)
                    else:
                        db[tabla].insert(**dict_)
                elif v[0].startswith("SubTotal Segmento"): break

@auth.requires(auth.has_membership("administrador") or auth.has_membership("editor_comercial"))
def importar_cuentas_edad():
    import os,sys

    sys.path.append(os.path.join("site-packages","xlrd"))
    titulo = "Importar Reporte Edad de la Cuenta N DIAS"
    uploadfolder = os.path.join(request.folder, 'uploads')

    form = SQLFORM.factory(
        Field('treinta', 'upload', label="ReporteEdadesCuenta30Dias",
              requires=IS_NOT_EMPTY(error_message="Seleccione el archivo (csv)."), uploadfolder=uploadfolder),
        Field('sesenta', 'upload', label="ReporteEdadesCuenta60Dias",
              requires=IS_NOT_EMPTY(error_message="Seleccione el archivo (csv)."), uploadfolder=uploadfolder),
        Field('noventa', 'upload', label="ReporteEdadesCuenta90Dias",
              requires=IS_NOT_EMPTY(error_message="Seleccione el archivo (csv)."), uploadfolder=uploadfolder),
        Field('mas_de_noventa', 'upload', label="ReporteEdadesCuentaMas90Dias",
              requires=IS_NOT_EMPTY(error_message="Seleccione el archivo (csv)."), uploadfolder=uploadfolder)
    )

    if form.process().accepted:
        try:
            db.cuentas_edad.truncate('RESTART IDENTITY CASCADE')
            path = os.path.join(uploadfolder,form.vars.treinta)
            importar_desde_archivo(path,"treinta")
            os.unlink(path)

            path = os.path.join(uploadfolder, form.vars.sesenta)
            importar_desde_archivo(path,"sesenta")
            os.unlink(path)

            path = os.path.join(uploadfolder, form.vars.noventa)
            importar_desde_archivo(path,"noventa")
            os.unlink(path)

            path = os.path.join(uploadfolder, form.vars.mas_de_noventa)
            importar_desde_archivo(path,"mas_de_90")
            os.unlink(path)

        except Exception, e:
            redirect(URL('error', 'index', vars=dict(error=str(e))))
        else:
           redirect(URL('index'))

    return response.render("default/index.html", dict(titulo=titulo, contenido=form))
