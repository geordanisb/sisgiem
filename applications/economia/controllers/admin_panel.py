@auth.requires_membership("Administradores")
def index():
    query = request.vars.query or "auth_user"
    grid = SQLFORM.grid(db[query],user_signature=False,editable=True,deletable=True,create=True)
    return locals()