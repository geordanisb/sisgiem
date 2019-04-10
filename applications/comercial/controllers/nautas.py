def nautas():
    sala = TH("Salas",_width="20%")
    posiciones = TH("Posiciones", _width="10%")
    activas = TH("Activas", _width="10%")
    observaciones = TH("Observaciones", _width="60%")

    thead = THEAD(TR(sala,posiciones,activas,observaciones))
    tbody = TBODY()
    table = TABLE(thead,tbody,_class="table table-bordered table-condensed",_width="100%")
    nautas = db(db.pc_nauta.id>0).select()
    for n in nautas:
        tbody.append(TR(TD(SPAN(n.sala)),TD(SPAN(n.posiciones)),TD(SPAN(n.activas)),TD(SPAN(n.observaciones))))
    titulo = "PC Nautas"
    return response.render('default/index.html', dict(titulo=titulo,contenido=table))

def index():
    request.vars._export_filename = "nautas"

    db.pc_nauta.id.readable = False
    db.pc_nauta.activas.represent = lambda a, row: SPAN(a, _class="label label-info") if row.posiciones == row.activas  else SPAN(a, _class="label label-danger")

    create = deletable = editable = auth.has_membership('editor')
    grid = SQLFORM.grid(db.pc_nauta, create=create, editable=editable, deletable=deletable)
    titulo = "Computadoras Nautas"

    imprimir = A("Imprimir",_class="btn btn-primary",_href=URL('reporte_nauta'))
    grid[0].append(imprimir)
    return response.render('default/index.html', dict(titulo=titulo, contenido=grid))