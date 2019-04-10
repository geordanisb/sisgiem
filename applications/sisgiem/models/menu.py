# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# ----------------------------------------------------------------------------------------------------------------------
# Customize your APP title, subtitle and menus here
# ----------------------------------------------------------------------------------------------------------------------

response.logo = A(B('Sis', SPAN("GIEM")),
                  _class="navbar-brand", _href=URL("sisgiem", "default", "index"),
                  _id="siem-logo")
response.title = request.application.replace('_', ' ').title()
response.subtitle = ''

# ----------------------------------------------------------------------------------------------------------------------
# read more at http://dev.w3.org/html5/markup/meta.name.html
# ----------------------------------------------------------------------------------------------------------------------
response.meta.author = myconf.get('app.author')
response.meta.description = myconf.get('app.description')
response.meta.keywords = myconf.get('app.keywords')
response.meta.generator = myconf.get('app.generator')

# ----------------------------------------------------------------------------------------------------------------------
# your http://google.com/analytics id
# ----------------------------------------------------------------------------------------------------------------------
response.google_analytics_id = None

# ----------------------------------------------------------------------------------------------------------------------
# this is the main application menu add/remove items as required
# ----------------------------------------------------------------------------------------------------------------------

response.menu = [
    (SPAN(I(_class="glyphicon glyphicon-home", _id="home")), False, URL("default", "index")),
    (SPAN("Centro de dirección", _id="centro_dir"), False, URL("centro_dir", "default", "index")),
    (SPAN("Comercial", _id="comercial"), False, URL("comercial", "default", "index")),
    (SPAN("Economía", _id="economia"), False, URL("economia", "default", "index")),
    #(SPAN("Planta Exterior", _id="planta_ext"), False, URL("planta_ext", "default", "index")),
    #(SPAN("Planta Interior", _id="planta_int"), False, URL("planta_int", "default", "index")),
(SPAN("Lóg. y Servicios", _id="log_servicio"), False, URL("log_servicio", "default", "index")),
    (SPAN("Operación y Desarrollo de la Red", _id="odr"), False, URL("odr", "default", "index")),
    (SPAN("TI", _id="ti"), False, URL("ti", "default", "index")),
    (SPAN("Notificador", _id="ti"), False, URL("notificador", "default", "index")),
    #(SPAN(I(_class="glyphicon glyphicon-cog"), _id="admin_panel"), False, URL("default", "admin_panel"))
]

if "auth" in locals():
    auth.wikimenu()
