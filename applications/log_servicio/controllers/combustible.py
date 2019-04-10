# -*- coding: utf-8 -*-
deletable = editable = create = auth.has_membership("jefe_grupo")

def index():
    titulo = "Demanda mensual de combustible"
    contenido = MENU(response.combustible)
    return response.render("default/index.html", dict(titulo=titulo, contenido=contenido))

def recorridos():
    titulo = "Recorridos"
    db.recorrido.id.readable = 0
    grid = SQLFORM.grid(db.recorrido,create=create,deletable=deletable,editable=editable)
    btn_import = A(I(_class="glyphicon glyphicon-import")," Importar",_href=URL("importar_recorridos"), _class="btn btn-primary",_title="Importar recorridos")
    grid[0].append(btn_import)
    return response.render("default/index.html", dict(titulo=titulo, contenido=grid))

def vehiculos():
    titulo = "Vehículos"
    db.vehiculo.id.readable = 0
    grid = SQLFORM.grid(db.vehiculo,create=create,deletable=deletable,editable=editable)
    return response.render("default/index.html", dict(titulo=titulo, contenido=grid))

def responsable_comb():
    titulo = "Responsables"
    db.responsable_comb.id.readable = 0
    grid = SQLFORM.grid(db.responsable_comb,create=create,deletable=deletable,editable=editable)
    return response.render("default/index.html", dict(titulo=titulo, contenido=grid))

@auth.requires_membership("jefe_grupo")
def demandas():
    titulo = "Demandas"
    db.demanda.id.readable = 0
    links = [lambda row: A(I(_class="glyphicon glyphicon-zoom-in")," Vista",_href=URL("demanda",args=row.id),_class="btn btn-default btn-success"),
             lambda row: A(I(_class="glyphicon glyphicon-print"), " Imprimir", _href=URL("imprimir_demanda", args=row.id),
                           _class="btn btn-default btn-success")]
    grid = SQLFORM.grid(db.demanda,create=create,deletable=deletable,details=0,editable=editable,links=links)
    return response.render("default/index.html", dict(titulo=titulo, contenido=grid))

def imprimir_demanda():
    id = request.args(0, cast=int)
    demanda = db.demanda(id)
    vehiculo = db.vehiculo(demanda.vehiculo)
    responsable = db.responsable_comb(vehiculo.responsable)
    dpto = responsable.area
    responsable_nombre = responsable.nombre
    cargo = responsable.cargo
    tipo_vehiculo = vehiculo.tipo
    marca = vehiculo.marca
    modelo_vehiculo = vehiculo.modelo
    ind_consumo = vehiculo.ind_consumo
    tipo_combustible = demanda.tipo_combustible
    fecha_demanda = demanda.fecha
    elabora = Autor(auth.user_id) 
    if elabora == "Desconocido": elabora = "" 

    tr_th = TR(TH("Actividades"),TH("Recorridos"),TH("Días/mes"),TH("Km"),TH("Total Km"),TH("Demanda"))
    thead = THEAD(tr_th)
    tbody = TBODY()

    table = TABLE(thead, tbody, _class="table table-bordered table-condensed")

    query = db.demandas_recorridos.demanda == id
    query &= db.demandas_recorridos.recorrido == db.recorrido.id
    recorridos = db(query).select()
    total_veces=total_distancia=total_kms=total_demanda=0

    for r in recorridos:
        origen = r["recorrido"].origen
        destino = r["recorrido"].destino
        veces = r["demandas_recorridos"].veces
        distancia = r["recorrido"].distancia
        kms = float(veces) * float(distancia)
        d = round(kms / ind_consumo,1)
        tr_td = TR(TD(),TD(origen + " - " + destino),TD(veces),TD(distancia),TD(kms),TD(d))
        tbody.append(tr_td)
        total_veces+=veces
        total_distancia+=distancia
        total_kms+=kms
        total_demanda+=d

    tr_footer = TR(TD(STRONG("TOTAL"),_colspan=2,_class="text-center"),TD(STRONG(total_veces)),TD(STRONG(total_distancia)),TD(STRONG(total_kms)),
                   TD(STRONG(round(total_demanda,1))))
    tbody.append(tr_footer)

    return locals()

@auth.requires_membership("jefe_grupo")
def demanda():
    titulo = "Datos de la demanda"
    id = request.args(0,cast=int)
    d = db.demanda(id)
    db.demanda.id.readable=0
    db.demandas_recorridos.id.readable = 0
    db.demandas_recorridos.demanda.readable = 0
    db.demandas_recorridos.recorrido.readable = 0
    db.recorrido.id.readable=0
    detalles = SQLFORM(db.demanda,d,readonly=1,user_signature=0)


    query = db.demandas_recorridos.demanda == id
    query &= db.demandas_recorridos.recorrido == db.recorrido.id
    links = [lambda row: A(I(_class="glyphicon glyphicon-pencil"), " Editar", _href=URL("demanda_recorridos", args=(row["demandas_recorridos"].id,
                                                                                                                    row["demandas_recorridos"].demanda)),
                           _class="btn btn-default")]

    grid_recorridos = SQLFORM.grid(query, searchable=0,user_signature=0,deletable=0,editable=0,details=0,create=0,csv=0,maxtextlength=200,links=links,
                                   orderby=db.demandas_recorridos.id)

    db.demandas_recorridos.demanda.default = id
    db.demandas_recorridos.demanda.writable = 0
    origenes = [o.origen for o in db().select(db.recorrido.origen,distinct=1)]
    destinos = [d.destino for d in db().select(db.recorrido.destino, distinct=1)]
    origen = Field("origen",requires=IS_IN_SET(origenes))
    destino = Field("destino",requires=IS_IN_SET(destinos))
    veces = Field("veces", requires=IS_INT_IN_RANGE())
    form_recorridos = SQLFORM.factory(origen,destino,veces)

    if form_recorridos.process().accepted:
        q = db.recorrido.origen == form_recorridos.vars.origen
        q &= db.recorrido.destino == form_recorridos.vars.destino
        recorrido = db(q).select().first()
        db.demandas_recorridos.insert(demanda=id,recorrido=recorrido.id,veces=form_recorridos.vars.veces)
        redirect(URL("demanda",args=id))
    grid_recorridos[0].append(form_recorridos)
    recorridos = DIV(
        DIV(H5("Recorridos"),_class="panel-heading"),
        DIV(grid_recorridos,_class="panel-body")
        ,_class="panel panel-info")
    contenido = DIV(detalles,recorridos)
    return response.render("default/index.html", dict(titulo=titulo, contenido=contenido, regresar=URL("demandas")))

def demanda_recorridos():
    titulo = "Editar recorrido de demanda"
    id = request.args(0,cast=int)
    demanda = request.args(1,cast=int)
    recorrido_d = db.demandas_recorridos(id)
    form = SQLFORM(db.demandas_recorridos,recorrido_d,deletable=1).process()
    if form.accepted:
        redirect(URL("demanda", args=demanda))
    return response.render("default/index.html", dict(titulo=titulo, contenido=form))

def importar_recorridos_(archivo):
    from xlrd import open_workbook

    tabla = "recorrido"
    book = open_workbook(archivo)
    sheet = book.sheet_by_index(0)

    db[tabla].truncate('RESTART IDENTITY CASCADE')

    destinos = sheet.row_values(1, 0)

    col = 1

    for row in range(2, sheet.nrows):
        valores = sheet.row_values(row, 0)
        origen = valores[0].replace("CENTRO DE TELECOMUNICACIONES ","")
        origen = origen.replace("CT ", "")
        origen = origen.replace("DIRECCION TERRITORIAL ETECSA","DT")
        for v in valores[1:]:
            destino = destinos[col].replace("CENTRO DE TELECOMUNICACIONES ","")
            destino = destino.replace("CT ", "")
            destino = destino.replace("DIRECCION TERRITORIAL ETECSA", "DT")
            distancia = v
            #if v != 0.0:
            db[tabla].insert(origen=origen,destino=destino,distancia=distancia)
            col += 1
        col = 1
    db[tabla].insert(origen="DT MATANZAS", destino="Recorrido de las FOTOS", distancia=363.4)

@auth.requires_membership("jefe_grupo")
def importar_recorridos():
    import os, sys

    sys.path.append(os.path.join("site-packages", "xlrd"))
    titulo = "Importar recorridos"
    uploadfolder = os.path.join(request.folder, 'uploads')
    valores = 0
    form = SQLFORM.factory(
        Field('tabla_distancias', 'upload', label="Tabla de distancias",
              requires=IS_NOT_EMPTY(error_message="Seleccione el archivo (csv)."), uploadfolder=uploadfolder),

    )
    if form.process().accepted:
        try:
            path = os.path.join(uploadfolder, form.vars.tabla_distancias)
            valores = importar_recorridos_(path)
            os.unlink(path)
        except Exception, e:
            redirect(URL('error', 'index', vars=dict(error=str(e))))
        #else:
        #    redirect(URL('importar'))

    return response.render("default/index.html", dict(titulo=titulo, contenido=form))
