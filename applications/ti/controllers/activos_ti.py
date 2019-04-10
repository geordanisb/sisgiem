create = deletable = editable = auth.has_membership('editor_ti')
db.activo.mon.represent = lambda mon,row: SPAN(mon,_class="label label-info") if mon=="USD" else mon

def represent_local(local):
    uo = db.uo(local_==local)
    if uo:
        return SPAN(uo.entidad.nombre, " ", SPAN(local,_class="label label-info"))

def usa_ip(r):
    critclas5 = db.activo(r.id).critclas5
    return (critclas5 == "HW_COMPT") or (critclas5 == "HW_LAPTP") or (critclas5 == "HW_IMPRE")

def get_record_activo(row):
    if "activo" in row:
        return row["activo"]
    else: return row

db.activo.local_.represent = lambda local,row: represent_local(local)
fields = [db.activo.n_inventario,db.activo.mon,db.activo.denominacin_del_activo_fijo,db.activo.local_]



links = [dict(header=' ', body=lambda row: DIV(A(I(_class='glyphicon glyphicon-blackboard'), '', _title="Detalles del activo",_href=URL('activo_config', args=get_record_activo(row).n_inventario),_class='btn btn-primary'),A(I(_class='glyphicon glyphicon-wrench'), '', _title="Enviar al taller",_href=URL('enviar_al_taller', args=get_record_activo(row).n_inventario),_class='btn btn-primary'),A(I(_class='glyphicon glyphicon-list-alt'), '',_title="Dictamen Técnico",_href=URL('dictamen_tecnico_form',args=get_record_activo(row).n_inventario),_class='btn btn-primary'), \
                                               \
                                               _class="btn btn-group"))         ]


@cache(request.env.path_info, time_expire=5, cache_model=cache.ram)
def index():
    titulo = "Activos TI"
    query = False
    for a in ACTIVO_TI:
        query |= (db.activo.critclas5 == a)

    query &= (db.activo.mon=="USD")

    #db.activo.actfijo.readable=0
    #db.activo.cecoste.readable = 0
    
    grid = SQLFORM.grid(query, create=0, editable=0, deletable=0, fields=fields,links=links)
    
    #glyphicon glyphicon-erase
    grid[0].append(A(I(_class="glyphicon glyphicon-wrench"), _href=URL("activos_taller"), _title="Activos en el taller",
                     _class="btn btn-default"))

    grid[0].append(A(I(_class="glyphicon glyphicon-remove text-danger"), _href=URL("activos_de_baja"), _title="Activos dados de baja",
                     _class="btn btn-default"))

    grid[0].append(A(I(_class="glyphicon glyphicon-list-alt"), _href=URL("dictemenes_tec"),
                     _title="Dictamenes técnicos",
                     _class="btn btn-default"))

    grid[0].append(A(I(_class="glyphicon glyphicon-briefcase"), _href=URL("destinos_finales"),
                     _title="Destinos finales",
                     _class="btn btn-default"))

    criterios = P(H3("Criterios de clasificación de activos: "),P(*[A(c,_class="label label-info",_style="display:inline-block;margin-right:2px",_href=URL("index",vars=dict(keywords=c))) for c in ACTIVO_TI]),_class="well")
    contenido = P(criterios,grid)

    return response.render("default/index.html", dict(titulo=titulo, contenido=contenido))

@auth.requires(auth.has_membership("administrador") or auth.has_membership("editor_ti"))
def enviar_al_taller():
    titulo = "Activo en el taller"
    no_inv = request.args(0)

    if no_inv:
        activo = db(db.activo.n_inventario == no_inv).select().first()
        activo_taller = responsable = None

        if activo:
            activo_taller = db(db.activo_taller.n_inventario == no_inv).select().first()
            db.activo_taller.local_.default = activo.local_
            db.activo_taller.local_.writable = 0
            db.activo_taller.denominacin_del_activo_fijo.default = activo.denominacin_del_activo_fijo
            db.activo_taller.denominacin_del_activo_fijo.writable = 0
            uo = db(db.uo.local_ == activo.local_).select().first()
            if uo:
                responsable = uo.responsable
                if responsable:
                    db.activo_taller.responsable.default = Responsable(responsable)
                    db.activo_taller.responsable.writable = 0

        db.activo_taller.n_inventario.default = no_inv
        db.activo_taller.n_inventario.writable = False
        if activo_taller:
            form = SQLFORM(db.activo_taller,activo_taller)
        else:
            form = SQLFORM(db.activo_taller)
        if form.process().accepted:
            redirect(URL("index"))
    else: redirect(URL("index"))

    return response.render("default/index.html", dict(titulo=titulo, contenido=form))

def activos_taller():
    titulo = "Activos en el taller"
    db.activo_taller.id.readable = db.activo_taller.denominacin_del_activo_fijo.writable = db.activo_taller.n_inventario.writable = False
    db.activo_taller.responsable.writable = db.activo_taller.local_.writable = 0
    def Estado(estado):
        if estado == "Reparado": return SPAN(estado,_class="label label-success")
        if estado == "Dictaminado baja": return SPAN(estado, _class="label label-warning")
        if estado == "Baja": return SPAN(estado, _class="label label-danger")
        if estado == "Pendiente por diagnóstico": return SPAN(estado, _class="label label-info")
        return SPAN(estado,_class="label label-default")

    link_dictamen = ""
    db.activo_taller.estado.represent = lambda estado,row: Estado(estado)
    links = [lambda row: A(SPAN(I(_class="glyphicon glyphicon-ok")," Dar salida"), _href=URL("dar_salida",args=row.id), _title="Dar salida a activo del taller",
                     _class="btn btn-success"),lambda row:A(I(_class='glyphicon glyphicon-list-alt'), '',_title="Dictamen Técnico",_href=URL('dictamen_tecnico_form',args=get_record_activo(row).n_inventario),_class='btn btn-primary')]
    
    export_classes = dict(csv=True, json=False, html=False,tsv=True, xml=False, csv_with_hidden_cols=False,tsv_with_hidden_cols=False)
    grid = SQLFORM.grid(db.activo_taller,links=links,create=0,editable=editable)

    return response.render("default/index.html", dict(titulo=titulo, contenido=grid))

@auth.requires(auth.has_membership("administrador") or auth.has_membership("editor_ti"))
def dar_salida():
    id = request.args(0,cast=int)
    activo = db.activo_taller[id]
    estado = activo.estado
    if estado == "Reparado":
        estado = "Funcionando"
    if activo.estado == "Baja":
        db.activo_taller_baja.insert(n_inventario=activo.n_inventario,denominacin_del_activo_fijo=activo.denominacin_del_activo_fijo,
                                 responsable=activo.responsable,local_=activo.local_,estado=activo.estado,observaciones=activo.observaciones)

    activo_config = db(db.activo_config.activo == activo['n_inventario']).select().first()
    if activo_config:    activo_config.update_record(estado = estado)#si tiene descripcion la PC se la modifico
    del db.activo_taller[id]
    redirect(URL("activos_taller"))

def activos_de_baja():
    titulo = "Activos dados de baja"
    if not "view" in request.args:
        db.activo_taller_baja.id.readable = 0

    grid = SQLFORM.grid(db.activo_taller_baja,editable=0,deletable=0)
    return response.render("default/index.html", dict(titulo=titulo, contenido=grid))

def pc_por_entidad():
    f_entidades = Field("entidades",requires=IS_IN_DB(db,"entidad.id","%(nombre)s",multiple=True))
    form = SQLFORM.factory(f_entidades)
    grid = ""
    titulo = "Computadoras por entidad para dar mantenimiento"

    if form.process().accepted:
        entidades = form.vars.entidades

        query_entidad = [(db.uo.entidad == e) for e in entidades]
        query_entidad = reduce(lambda a, b: (a | b), query_entidad)

        query_moneda = (db.activo.mon == "USD")
        query_local = db.uo.local_ == db.activo.local_

        #query_criterio = [(db.activo.critclas5 == c) for c in ACTIVO_TI_MTTO]
        query_criterio = reduce(lambda a,b: (a | b), ((db.activo.critclas5 == c) for c in ACTIVO_TI_MTTO))

        query = query_entidad & query_criterio & query_moneda & query_local

        fields = [db.activo.n_inventario, db.activo.critclas5, db.uo.entidad, db.activo.local_,db.activo.denominacin_del_activo_fijo]
        grid = SQLFORM.grid(query, fields=fields,paginate=1000)
    contenido = DIV(form,grid)
    return response.render("default/index.html", dict(titulo=titulo, contenido=contenido))

def harware_por_entidad():
    f_local = Field("local",requires=IS_IN_DB(db,"uo.local_","%(local_)s"))
    f_clasif = Field("critclas5",label="Clasificación del hardware",
                     requires=IS_IN_SET(ACTIVO_TI))

    form = SQLFORM.factory(f_local,f_clasif)
    grid = ""
    titulo = "Hardware por entidad"
    db.activo.local_.represent = lambda local,row: local
    
    if form.process().accepted:
        query = (db.activo.local_ == form.vars.local)
        query &= (db.activo.mon == "USD")
        query &= (db.activo.critclas5 == form.vars.critclas5)

        fields = [db.activo.n_inventario, db.activo.critclas5, db.activo.local_,db.activo.denominacin_del_activo_fijo]
        grid = SQLFORM.grid(query, fields=fields,paginate=1000)
    contenido = DIV(form,grid)
    return response.render("default/index.html", dict(titulo=titulo, contenido=contenido))

def exportar_excel():
    query_local = (db.activo.local_ == local)
    query_moneda = (db.activo.mon == "USD") & (db.activo.critclas5 == "TX_SOTER")
    query = query_local & query_moneda
    rows = []
    fields = db
    [rows.append(i) for i in db(query).select().as_list()]
    write_xls("activos.xls","activos",["No. Inventario","Critclas5","Local",u"Denominación"],rows)
    return locals()

def activos_por_no_inv():
    import re

    f =Field("f","text",label="Texto con los números de inventarios",requires=IS_NOT_EMPTY(error_message="Datos requeridos"))
    form = SQLFORM.factory(f)
    grid = ""
    titulo = "Activos por no. de inventarios"
    if form.process().accepted:
        try:
            rule = re.compile(r"08_24\d_\d\d\d\d\d\d")
            no_inventarios = rule.findall(form.vars.f)
            if no_inventarios:
                db.activo.id.readable = False
                q = [(db.activo.n_inventario == i) for i in no_inventarios]
                queries = reduce(lambda a, b: (a | b), q)
                queries &= (db.activo.mon == "USD")
                grid = SQLFORM.grid(queries)
        except Exception, e:
            return response.render("default/index.html", dict(titulo=titulo, contenido=str(e)))
    return response.render("default/index.html", dict(titulo=titulo, contenido=DIV(form,grid)))



def clasificacion_hardware():
    titulo = "Clasificaciones del hardware según activos desde SAP"
    deletable = create = editable = auth.has_membership("administrador") or auth.has_membership("editor_ti")
    grid = SQLFORM.grid(db.clasificacion_hardware,create=create,deletable=deletable,editable=editable)
    return response.render("default/index.html", dict(titulo=titulo, contenido=grid))

def por_uo():
    titulo = "Activos informáticos por unidades organizativas"
    db.uo.local_.represent = lambda local, row: A(local,_class="btn btn-info",_href=URL("hardware_por_uo",vars=dict(local=local)))
    db.uo.id.readable = db.uo.entidad.readable = 0
    deletable = create = editable = auth.has_membership("administrador") or auth.has_membership("editor_ti")
    query = db.uo.entidad == db.entidad.id
    fields = [db.entidad.nombre,db.uo.local_,db.uo.responsable]
    grid = SQLFORM.grid(query, create=create, deletable=deletable, editable=editable,fields=fields)
    return response.render("default/index.html", dict(titulo=titulo, contenido=grid))

def hardware_por_uo():
    titulo = "Activos informáticos por unidades organizativas"
    local = request.vars["local"]

    query = db.activo.critclas5 == db.clasificacion_hardware.critclas5
    query &= local == db.activo.local_
    query &= db.activo.mon == "USD"

    def es_pc(row):
        return (row["critclas5"] == "HW_COMPT") or (row["critclas5"] == "HW_LAPTP") or (row["critclas5"] == "HW_IMPRE")
    
    activo_config_link = [lambda row: A(I(_class="glyphicon glyphicon-ok")," Config.",_href=URL("activo_config",args=row.id),_class="btn btn-info") if es_pc(row) else ""]
    
    db.activo.local_.represent = lambda local_,row: local_
    fields = [db.activo.actfijo, db.activo.n_inventario, db.activo.denominacin_del_activo_fijo, db.activo.local_,
              db.activo.critclas5,db.activo.id]
    grid = SQLFORM.grid(query, fields=fields, paginate=100,links=links)
    return response.render("default/index.html", dict(titulo=titulo, contenido=grid))

def por_entidades():
    titulo = "Activos informáticos por entidades"
    form = SQLFORM.factory(Field("entidad", requires=IS_IN_DB(db, 'entidad.nombre')))
    if form.process().accepted:
        redirect(URL("entidades_",vars=dict(entidad=form.vars.entidad)))
    return response.render("default/index.html", dict(titulo=titulo, contenido=form))

def entidades_():
    titulo = "Activos informáticos por entidades"
    entidad = request.vars["entidad"]
    
    query = db.activo.critclas5 == db.clasificacion_hardware.critclas5
    query &= db.entidad.nombre == entidad
    query &= db.uo.entidad == db.entidad.id
    query &= db.uo.local_ == db.activo.local_
    query &= db.activo.mon == "USD"
    #query &= db.clasificacion_hardware.critclas5 == db.activo.critclas5

    #db.activo.local_.represent = lambda local_,row: local_
    
    db.activo.local_.represent = lambda local, row: A(local,_class="btn btn-info",_href=URL("hardware_por_uo",vars=dict(local=local)))
    fields = [db.activo.id,db.activo.actfijo, db.activo.n_inventario, db.activo.denominacin_del_activo_fijo, db.activo.local_,
              db.activo.critclas5]
    grid = SQLFORM.grid(query, fields=fields, paginate=100,links=links)
    return response.render("default/index.html", dict(titulo=titulo, contenido=grid))

def activo_config():
    titulo = "Activos informáticos por entidades"
    n_inventario = request.args(0)
    db.activo_config.activo.default = n_inventario
    db.activo_config.activo.writable = 0
    record = db(db.activo_config.activo==n_inventario).select().first()
    form=""
    if record:
        form = SQLFORM(db.activo_config,record)
    else:
        form = SQLFORM(db.activo_config)
    if form.process().accepted:redirect(URL('index'))
       
    return response.render("default/index.html", dict(titulo=titulo, contenido=form))

@auth.requires_membership("editor_taller")
def dictamen_tecnico_form():
    n_inventario = request.args(0)
    #db.define_table("dictemenes_tec",no_inventario,denominacion,no_serie,marca,modelo,local,dictamen,jefe_dpto)
    activo = db(db.activo.n_inventario == n_inventario).select().first()
    dictemen_tec = db(db.dictemenes_tec.n_inventario==activo.n_inventario).select().first()
    if dictemen_tec:
        dictemen_tec.update_record(created_on=request.now,created_by=auth.user_id)
    titulo = "Realizar Dictamen Técnico"
    
    
    db.dictemenes_tec.critclas5.default = activo.critclas5
    db.dictemenes_tec.critclas5.writable = 0
    
    db.dictemenes_tec.n_inventario.default = n_inventario
    db.dictemenes_tec.n_inventario.readable = db.dictemenes_tec.n_inventario.writable = 0

    db.dictemenes_tec.denominacin_del_activo_fijo.default = activo.denominacin_del_activo_fijo
    db.dictemenes_tec.denominacin_del_activo_fijo.readable = db.dictemenes_tec.denominacin_del_activo_fijo.writable = 0

    db.dictemenes_tec.local_.default = activo.local_
    db.dictemenes_tec.local_.readable = db.dictemenes_tec.local_.writable = 0
    
    db.dictemenes_tec.created_on.default = request.now
    db.dictemenes_tec.created_by.default = auth.user_id
    
    db.dictemenes_tec.created_on.readable = 1
    db.dictemenes_tec.created_by.readable = 1

    form = SQLFORM(db.dictemenes_tec,dictemen_tec)
    if form.process().accepted:
        redirect(URL("dictamen_tecnico",args=form.vars.id))
    return response.render("default/index.html", dict(titulo=titulo, contenido=form))

def dictemenes_tec():
    titulo = "Dictamenes técnicos"
    db.dictemenes_tec.id.readable = 0
    deletable=auth.has_membership("editor_taller")
    editable=deletable
    links = [dict(header=' ',
                  body=lambda row: A(I(_class='glyphicon glyphicon-briefcase'), '', _title="Destino Final",
                                     _href=URL('destino_final_form', args=get_record_activo(row).id),
                                     _class='btn btn-primary')),
             dict(header=' ',
                  body=lambda row: A(I(_class='glyphicon glyphicon-print'), '', _title="Imprimir Dictamen Técnico",
                                     _href=URL('dictamen_tecnico', args=get_record_activo(row).id),
                                     _class='btn btn-primary'))
             ]
    db.dictemenes_tec.created_on.readable = 1
    db.dictemenes_tec.created_by.readable = 1    
    
    grid = SQLFORM.grid(db.dictemenes_tec,links=links,editable=editable,deletable=0)
    return response.render("default/index.html", dict(titulo=titulo, contenido=grid))

def dictamen_tecnico():
    dictemen_tec_id = request.args(0)
    dictemen_tec = db.dictemenes_tec(dictemen_tec_id)
    no_inventario = dictemen_tec.n_inventario
    denominacion = dictemen_tec.denominacin_del_activo_fijo
    no_serie = dictemen_tec.no_serie
    marca = dictemen_tec.marca_del_equipo
    modelo = dictemen_tec.modelo_del_equipo
    local = dictemen_tec.local_
    orden_trabajo = dictemen_tec.orden_trabajo
    dictamen = dictemen_tec.dictamen
    uo = db(db.uo.local_ == local).select().first()
    responsable = db.responsable(uo.responsable).nombre or ""
    entidad = db.entidad(uo.entidad).nombre
    jefe_dpto = dictemen_tec.jefe_dpto
    dict_ = dict(orden_trabajo=orden_trabajo,dictemen_tec_id=dictemen_tec_id,no_inventario=no_inventario,denominacion=denominacion,marca=marca,no_serie=no_serie,modelo=modelo,responsable=responsable,jefe_dpto=jefe_dpto,entidad=entidad,dictamen=dictamen)
    return response.render("default/dictamen_tecnico.html",dict_)

@auth.requires_membership("editor_taller")
def destino_final_form():
    dictemen_tec_id = request.args(0)

    destino_final = db(db.destinos_finales.dictamen_tec==dictemen_tec_id).select().first()
    titulo = "Realizar Destino Final"
    dictamen_tec = db(db.dictemenes_tec.id==dictemen_tec_id).select().first()
    
    db.destinos_finales.dictamen_tec.default = dictemen_tec_id
    db.destinos_finales.n_inventario.default = dictamen_tec.n_inventario
    db.destinos_finales.n_inventario.writable = 0
    db.destinos_finales.denominacin_del_activo_fijo.default = dictamen_tec.denominacin_del_activo_fijo
    db.destinos_finales.denominacin_del_activo_fijo.writable = 0
    
    db.destinos_finales.critclas5.default = dictamen_tec.critclas5
    db.destinos_finales.critclas5.writable = 0
    
    db.destinos_finales.local_.default = dictamen_tec.critclas5
    db.destinos_finales.local_.writable = 0
    
    #destino_final.update_record(n_inventario=dictamen_tec.n_inventario,denominacin_del_activo_fijo=dictamen_tec.denominacin_del_activo_fijo)
    
    db.destinos_finales.dictamen_tec.writable = 0
    db.destinos_finales.id.readable=0
    form = SQLFORM(db.destinos_finales, destino_final)
    if form.process().accepted:
        redirect(URL("destino_final", args=form.vars.id))
    return response.render("default/index.html", dict(titulo=titulo, contenido=form))

def destino_final():
    destino_final_id = request.args(0)
    destino_final = db.destinos_finales(destino_final_id)
    dictamen_tec = destino_final.dictamen_tec

    no_inventario = dictamen_tec.n_inventario
    denominacion = dictamen_tec.denominacin_del_activo_fijo
    no_serie = dictamen_tec.no_serie

    local = dictamen_tec.local_
    dictamen = dictamen_tec.dictamen
    uo = db(db.uo.local_ == local).select().first()
    responsable = db.responsable(uo.responsable).nombre or ""
    entidad = db.entidad(uo.entidad).nombre
    jefe_dpto = dictamen_tec.jefe_dpto
    orden_trabajo = dictamen_tec.orden_trabajo
    descripcion_piezas = OL(*[s for s in destino_final.descripcion_piezas])
    dict_ = dict(descripcion_piezas=descripcion_piezas,orden_trabajo=orden_trabajo,no_inventario=no_inventario,denominacion=denominacion,marca=marca,no_serie=no_serie,modelo=modelo,responsable=responsable,jefe_dpto=jefe_dpto,entidad=entidad,dictamen=dictamen)

    return response.render("default/destino_final.html",dict_)

def destinos_finales():
    deletable = auth.has_membership("editor_taller")
    editable = deletable
    titulo = "Destinos finales"
    links = [dict(header=' ',
                  body=lambda row: A(I(_class='glyphicon glyphicon-remove text-danger'), '', _title="Dar baja",
                                     _href=URL('dar_baja', args=get_record_activo(row).dictamen_tec.n_inventario),
                                     _class='btn btn-default')),
             dict(header=' ',
                  body=lambda row: A(I(_class='glyphicon glyphicon-print'), '', _title="Imprimir Destino Final",
                                     _href=URL('destino_final', args=get_record_activo(row).id),
                                     _class='btn btn-primary'))
             ]
    db.destinos_finales.id.readable = 0    
    grid = SQLFORM.grid(db.destinos_finales, links=links,deletable=0,editable=editable,maxtextlength=200)
    return response.render("default/index.html", dict(titulo=titulo, contenido=grid))

@auth.requires_membership("editor_taller")
def dar_baja():
    n_inventario = request.args(0)
    titulo = "Activos dados de baja"
    #db.define_table("activo_taller_baja",no_inventario,denominacion,local,observaciones,fecha_baja)
    activo = db(db.activo.n_inventario == n_inventario).select().first()
    activo_config = db(db.activo_config.activo == activo.n_inventario).select().first()

    activo_taller_baja = db(db.activo_taller_baja.n_inventario==n_inventario).select().first()

    db.activo_taller_baja.n_inventario.default = n_inventario
    db.activo_taller_baja.n_inventario.writable=0
    db.activo_taller_baja.denominacin_del_activo_fijo.default = activo.denominacin_del_activo_fijo
    db.activo_taller_baja.denominacin_del_activo_fijo.writable=0
    db.activo_taller_baja.local_.default = activo.local_
    db.activo_taller_baja.local_.writable=0


    form = SQLFORM(db.activo_taller_baja,activo_taller_baja)
    if form.process().accepted:
        if activo_config:
            activo_config.update_record(estado="Baja")
        else:
            #db.define_table('activo_config',ip,nombre,activo,tipo,observaciones,estado)
            db.activo_config.insert(ip="",nombre="",activo=activo.n_inventario,tipo="Otras",observaciones=db.activo_taller_baja.observaciones.default,estado="Baja")
        redirect(URL("activos_de_baja", args=form.vars.id))
    return response.render("default/index.html", dict(titulo=titulo, contenido=form))


    return locals()
