def index():
    db.uo.id.readable = False
    create = editable = deletable = auth.has_membership('editor_economia') or auth.has_membership('administrador')
    grid = SQLFORM.grid(db.uo, create=create, editable=editable, deletable=deletable)
    return locals()
