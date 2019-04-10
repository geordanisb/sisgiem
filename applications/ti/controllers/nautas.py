@auth.requires(auth.has_membership("editor_ti"))
def index():
    titulo = "Configuraciones de PC Nautas"
    form = SQLFORM.grid(db.config_nautas)
    return response.render("default/index.html", dict(titulo=titulo, contenido=form))
