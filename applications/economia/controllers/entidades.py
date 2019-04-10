def index():
    db.entidad.id.readable = False
    create = editable = deletable = auth.has_membership('editor_economia')
    grid = SQLFORM.grid(db.entidad, create=create, editable=editable, deletable=deletable)
    return locals()