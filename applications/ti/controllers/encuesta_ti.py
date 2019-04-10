mi = auth.user_id
db.encuesta_ti.id.readable = 0

def index():
    titulo = "ENCUESTA DE SATISFACCION AL CLIENTE DPTO. TECNOLOGIAS DE LA INFORMACION"
    #create = puede_hacer_encuesta()
    deletable = editable = lambda row: row.created_by == mi
    btn_fill = A(I(_class="glyphicon glyphicon-plus")," Llenar encuesta",_class="btn btn-primary",_href=URL("llenar_encuesta"))
    grid = SQLFORM.grid(db.encuesta_ti, create=0, deletable=0, editable=0, csv=1,user_signature=0)
    grid[0].append(btn_fill)
    return response.render("default/index.html", dict(titulo=titulo, contenido=grid))

def llenar_encuesta():
    titulo = "Llenar encuesta"
    contenido = SQLFORM(db.encuesta_ti).process()
    if contenido.accepted:
        redirect(URL("index"))

    return response.render("default/index.html", dict(titulo=titulo, contenido=contenido))


def puede_hacer_encuesta():
    hoy = request.now.date()
    query = db.encuesta_ti.created_by == mi
    rows = db(query).select()
    for r in rows:
        if (r.created_on.date().month == hoy.month) and (r.created_on.date().year == hoy.year):
            return False
    return True
