def index():
    titulo = "Información comercial"
    contenido = MENU(response.info_comercial)
    return response.render('default/index.html', dict(titulo=titulo, contenido=contenido))

def nautas():
    request.vars._export_filename = "nautas"

    db.pc_nauta.id.readable = False
    db.pc_nauta.activas.represent = lambda a, row: SPAN(a, _class="label label-info") if row.posiciones == row.activas  else SPAN(a, _class="label label-danger")

    create = deletable = editable = auth.has_membership('editor_comercial') or auth.has_membership('editor_ti')
    grid = SQLFORM.grid(db.pc_nauta, create=create, editable=editable, deletable=deletable)
    titulo = "PC Nautas"

    imprimir = A("Imprimir",_class="btn btn-primary",_href=URL('reporte_nautas'))
    grid[0].append(imprimir)
    return response.render('default/index.html', dict(titulo=titulo, contenido=grid))

def reporte_nautas():
    sala = TH("Salas",_width="20%")
    posiciones = TH("Posiciones", _width="10%")
    activas = TH("Activas", _width="10%")
    observaciones = TH("Observaciones", _width="60%")

    thead = THEAD(TR(sala,posiciones,activas,observaciones,_class="info"))
    tbody = TBODY()
    table = TABLE(thead,tbody,_class="table table-bordered table-condensed",_width="100%")
    nautas = db(db.pc_nauta.id>0).select()
    for n in nautas:
        tbody.append(TR(TD(SPAN(n.sala)),TD(SPAN(n.posiciones)),TD(SPAN(n.activas)),TD(SPAN(MARKMIN(n.observaciones)))))
    titulo = "PC Nautas"
    return response.render('default/index.html', dict(titulo=titulo,contenido=table))

def ejec_comercial():
    request.vars._export_filename = "ejecutivas_comercial"
    db.pc_ejec_comercial.no_.readable = db.pc_ejec_comercial.ctlc.readable = False

    titulo = "PC Ejec. Comercial"
    db.pc_ejec_comercial.id.readable = False
    db.pc_ejec_comercial.activas.represent = lambda a,row: SPAN(a,_class="label label-info") if row.posiciones == row.activas else SPAN(a,_class="label label-danger")
    create = deletable = editable = auth.has_membership('editor_comercial') or auth.has_membership('editor_ti')
    maxtextlengths = {'pc_ejec_comercial.unidad_comercial': 40,'pc_ejec_comercial.posiciones': 3,'pc_ejec_comercial.activas': 3}
    grid = SQLFORM.grid(db.pc_ejec_comercial, create=create, editable=editable, deletable=deletable,maxtextlengths=maxtextlengths)

    imprimir = A("Imprimir",_class="btn btn-primary",_href=URL('reporte_ejec_comercial'))
    grid[0].append(imprimir)
    return response.render('default/index.html', dict(titulo=titulo,contenido=grid))

def reporte_ejec_comercial():
    uc = TH("Unidades comerciales",_width="20%")
    posiciones = TH("Posiciones", _width="10%")
    activas = TH("Activas", _width="10%")
    observaciones = TH("Observaciones", _width="60%")

    titulo = "PC Ejec. Comercial"
    thead = THEAD(TR(uc,posiciones,activas,observaciones,_class="info"))
    tbody = TBODY()
    table = TABLE(thead,tbody,_class="table table-bordered table-condensed",_width="100%")
    ec = db(db.pc_ejec_comercial.id>0).select()
    for n in ec:
        tbody.append(TR(TD(SPAN(n.unidad_comercial)),TD(SPAN(n.posiciones)),TD(SPAN(n.activas)),TD(SPAN(MARKMIN(n.observaciones)))))
    return response.render('default/index.html', dict(titulo=titulo, contenido=table))
