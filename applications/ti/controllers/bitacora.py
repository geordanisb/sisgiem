def index():
    redirect(URL("eventos"))

@auth.requires(auth.has_membership("administrador") or auth.has_membership("editor_ti"))
def eventos():
    titulo = "Eventos"
    db.eventos.created_on.readable = db.eventos.created_by.readable = auth.has_membership("administrador")
    db.eventos.created_on.writable = db.eventos.created_by.writable = auth.has_membership("administrador")
    db.eventos.id.readable = False
    deletable = editable = lambda row: row.created_by.id == auth.user_id
    grid = SQLFORM.grid(db.eventos,orderby=db.eventos.created_on,editable=editable,deletable=deletable)

    imp_btn = A("Imprimir",_href=URL('imprimir'),_class="btn btn-success")
    aux = grid[0].append(imp_btn)
    return response.render("default/index.html", dict(titulo=titulo, contenido=grid))

@auth.requires(auth.has_membership("administrador") or auth.has_membership("editor_ti"))
def imprimir():
    rows = db(db.eventos.id>0).select()

    thead = THEAD(TR(TH("Tipo"),TH("Descripción"),TH("Observaciones"),TH("Creado por"),TH("Ocurrido en"),TH("Creado en")))
    tbody = TBODY()
    table = TABLE(thead,tbody,_class="table table-condensed table-bordered table-striped")

    for r in rows:
        tbody.append(TR(TD(r.tipo),TD(r.descripcion),TD(r.observaciones),TD(autor(r.created_by)),TD(r.fecha_ocurrencia),TD(r.created_on)))
    return locals()
