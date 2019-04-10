# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------
def x():
    uo = db(db.uo.id>0).select()
    for u in uo:
        activo = db(db.activo.local_ == u.local_).select()

        for a in activo:
            a.update_record(uo=u.id)

                #u.update_record(responsable = activo.responsable)

    return locals()

def index():
    redirect(URL('activos','index'))
    #enlaces = [A(i[0],_href=i[2],_class="btn btn-success") for i in response.menu]
    #enlaces = DIV(enlaces,_class="btn-group-lg")
    #return locals()

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
