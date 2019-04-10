def index():
    #db.responsable.id.readable = False
    create = editable = deletable = auth.has_membership('editor_economia') or auth.has_membership('administrador')
    db.responsable.id.readable = 0
    grid = SQLFORM.grid(db.responsable, create=create, editable=editable, deletable=deletable)
    return locals()
