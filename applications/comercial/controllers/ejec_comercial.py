def reporte():
    uc = TH("Unidades comerciales",_width="20%")
    posiciones = TH("Posiciones", _width="10%")
    activas = TH("Activas", _width="10%")
    observaciones = TH("Observaciones", _width="60%")

    titulo = "PC Ejec. Comercial"
    thead = THEAD(TR(uc,posiciones,activas,observaciones))
    tbody = TBODY()
    table = TABLE(thead,tbody,_class="table table-bordered table-condensed",_width="100%")
    ec = db(db.pc_ejec_comercial.id>0).select()
    for n in ec:
        tbody.append(TR(TD(SPAN(n.unidad_comercial)),TD(SPAN(n.posiciones)),TD(SPAN(n.activas)),TD(SPAN(n.observaciones))))
    return response.render('default/index.html', dict(titulo=titulo, contenido=table))

def index():
    request.vars._export_filename = "ejecutivas_comercial"
    db.pc_ejec_comercial.no_.readable = db.pc_ejec_comercial.ctlc.readable = False

    titulo = "PC Ejec. Comercial"
    db.pc_ejec_comercial.id.readable = False
    db.pc_ejec_comercial.activas.represent = lambda a,row: SPAN(a,_class="label label-info") if row.posiciones == row.activas else SPAN(a,_class="label label-danger")
    create = deletable = editable = auth.has_membership('editor')
    maxtextlengths = {'pc_ejec_comercial.unidad_comercial': 40,'pc_ejec_comercial.posiciones': 3,'pc_ejec_comercial.activas': 3}
    grid = SQLFORM.grid(db.pc_ejec_comercial, create=create, editable=editable, deletable=deletable,maxtextlengths=maxtextlengths)

    imprimir = A("Imprimir",_class="btn btn-primary",_href=URL('reporte_ejec_comercial'))
    grid[0].append(imprimir)
    return response.render('default/index.html', dict(titulo=titulo,contenido=grid))