# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------
mi = auth.user_id

def error(mensage="No autorizado"):
    session.flash = mensage
    redirect(URL("tareas"))

def index():
    titulo = "Notificador de tareas"
    contenido = MENU(response.menu[1:])
    if auth.user: redirect(URL("tareas"))
    return locals()

@auth.requires_login()
def tareas():
    query = db.tarea.asignada_a == mi
    query |= db.tarea.created_by == mi
#glyphicon glyphicon-zoom-in
    links = [lambda row: A(I(_class="glyphicon glyphicon-pencil")," Editar",\
                           _href=URL("editar_tarea",args=row.id),_class="btn btn-default"),
             lambda row: A(I(_class="glyphicon glyphicon-zoom-in"), " Ver", \
                           _href=URL("ver_tarea", args=row.id), _class="btn btn-default")
             ]
    deletable = lambda row: row.created_by == mi
    fields = [db.tarea.estado,db.tarea.titulo,db.tarea.created_on,db.tarea.created_by]
    grid = SQLFORM.grid(query,orderby=~db.tarea.created_on,links=links,details=0,editable=0,
                        deletable = deletable, create = 0,fields=fields)
    crear_btn = A("Crear tarea", _href=URL("crear_tarea"),_class="btn btn-primary")
    grid.insert(0,crear_btn)
    titulo = "Tareas asignadas y/o creadas por/para mí."
    contenido = grid
    return response.render("default/index.html",dict(titulo=titulo,contenido=contenido))

@auth.requires_login()
def crear_tarea():
    db.tarea.estado.writable=False
    form = SQLFORM(db.tarea).process()
    titulo = "Crear tarea"
    if form.accepted:
        email = db.auth_user(form.vars.asignada_a).email
        subject = "Nueva tarea asignada: %s" % form.vars.titulo
        message = form.vars.descripcion or "Sin descripción"

        enviar_correo(to=email, subject=subject, message=message)

        redirect(URL("tareas"))
    contenido = form    
    return response.render("default/index.html",dict(titulo=titulo,contenido=contenido))

@auth.requires_login()
def ver_tarea():
    from gluon.tools import prettydate
    tarea_id = request.args(0,cast=int)
    tarea = db.tarea(tarea_id) or error()
    if not tarea.created_by == mi and not tarea.asignada_a == mi: error()
    meta = "Creada {} por {}, asignada a {}".format(prettydate(tarea.created_on,T), autor(tarea.created_by), autor(tarea.asignada_a))
    titulo = SPAN(tarea.titulo," ", I(tarea.estado,_class="label label-default"))
    contenido = DIV(H6(meta,_class="text-muted"),P(tarea.descripcion))
    return response.render("default/index.html", dict(titulo=titulo, contenido=contenido))

@auth.requires_login()
def editar_tarea():
    #from gluon.tools import prettydate
    tarea_id = request.args(0,cast=int)
    tarea = db.tarea(tarea_id) or error()
    if not tarea.created_by == mi and not tarea.asignada_a == mi: error()
    deletable = tarea.created_by == mi

    db.tarea.titulo.writable = tarea.created_by == mi
    db.tarea.asignada_a.writable = tarea.created_by == mi

    if tarea.asignada_a == mi:
        db.tarea.estado.requires = IS_IN_SET(("aceptada","rechasada","completada"))

    form = SQLFORM(db.tarea,tarea,deletable=deletable).process()
    if form.accepted:
        email = tarea.created_by.email
        if tarea.created_by == mi:
            email = db.auth_user(form.vars.asignada_a).email


        subject = "Actualización de la tarea: %s" % form.vars.titulo
        message = form.vars.descripcion or "Sin descripción"

        enviar_correo(to=email, subject=subject, message=message)
        redirect(URL("ver_tarea",args=tarea_id))
    titulo = "Editar tarea: %s" % tarea.titulo
    contenido = form
    return response.render("default/index.html", dict(titulo=titulo, contenido=contenido))

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
