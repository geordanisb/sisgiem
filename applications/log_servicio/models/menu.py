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
    (SPAN("Demanda mensual de combustible"), False, URL("combustible", "index"),[
        (SPAN("Demandas"), False, URL("combustible", "demandas")),
        (SPAN("Vehículos"), False, URL("combustible", "vehiculos")),
        (SPAN("Responsables"), False, URL("combustible", "responsable_comb")),
        (SPAN("Recorridos"), False, URL("combustible", "recorridos")),
    ]),
    (SPAN(I(_class="glyphicon glyphicon-cog"), _id="admin_panel"), False, URL("default", "admin_panel",vars=dict(tablesname=("auth_user","auth_group"))))
]

response.combustible = [
(SPAN("Demandas"), False, URL("combustible", "demandas")),
(SPAN("Vehículos"), False, URL("combustible", "vehiculos")),
(SPAN("Responsables"), False, URL("combustible", "responsable_comb")),
(SPAN("Recorridos"), False, URL("combustible", "recorridos")),
]

if "auth" in locals():
    auth.wikimenu()
