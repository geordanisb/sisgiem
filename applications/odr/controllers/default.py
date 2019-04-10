# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------
"""def preparar_datos_ctlc():    
    ctlc = db(db.ctlc.id>0).select()
    for c in ctlc:
        centrales = db(db.central_telefonica.ctlc == c.nombre).select()
        for i in centrales:
            i.update_record(ctlc=c.id)"""

def c():
    centrales= db(db.central_telefonica.ctlc==3).select()
    for c in centrales:
        central = db.central_telefonica(c.id)
        central.update_record(ctlc=2)
    return locals()

def index():
    redirect(URL(c="gpo_sporte_oper"))
    return dict(message=T('Welcome to web2py!'))

@auth.requires_membership("administrador")
def admin_panel():
    titulo = "Panel de administración"
    query = request.vars.query or "auth_user"
    others = ""
    others = UL(_class="nav navbar-nav")
    [others.append(LI(A(t,_href=URL("admin_panel",vars=dict(query=t)))))for t in db._tables]
    grid = SQLFORM.grid(db[query],user_signature=False,editable=True,deletable=True,create=True)
    contenido = DIV(others,grid)
    return response.render("default/index.html", dict(titulo=titulo, contenido=contenido))


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
