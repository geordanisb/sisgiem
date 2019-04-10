def usuarios_restringido():
    db.usuarios.ipnavegacion.readable = db.usuarios.servicio.readable = db.usuarios.accountStatus.readable = auth.has_membership(
        "administrador")

def index():
    titulo = "Usuarios"
    usuarios_restringido()
    db.usuarios.id.readable = 0
    fields = [db.usuarios.dn, db.usuarios.title, db.usuarios.departmentnumber, db.usuarios.telephoneNumber]
    create = editable = deletable = auth.has_membership("Administradores") or auth.has_membership("editor_ti")
    contenido = SQLFORM.grid(db.usuarios,create=create, editable=editable, deletable=deletable,user_signature=False)

    return response.render("default/index.html", dict(titulo=titulo, contenido=contenido))