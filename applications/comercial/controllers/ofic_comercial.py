@auth.requires(auth.has_membership("administrador") or auth.has_membership("editor_comercial"))
def index():
    titulo = "Oficinas Comerciales"
    contenido = SQLFORM.grid(db.ofic_comercial)
    return response.render("default/index.html",
                           dict(titulo=titulo, contenido=contenido, link_activo="sop_comercial"))