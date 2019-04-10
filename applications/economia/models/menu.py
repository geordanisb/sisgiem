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
(SPAN(I(_class='glyphicon glyphicon-font'),"ctivos",_id="activos"),False,URL("activos","index")),
(SPAN(I(_class='glyphicon glyphicon-user')," Responsables",_id="responsables"),False,URL("responsables","index")),
    (SPAN(I(_class='glyphicon glyphicon-user text-info')," Autoridades Facultadas",_id="aut_facultada"),False,URL("autoridad_facultada","index")),
(SPAN("UO",_id="uo"),False,URL("uo","index")),
(SPAN("Entidades",_id="uo"),False,URL("entidades","index")),
(SPAN(I(_class="glyphicon glyphicon-import")," Importar activos",_id="importar_activos"),False,URL("csv","importar_activos")),
#(SPAN("Movimientos",_id="movimientos"),False,URL("movimientos","index")),
(SPAN(I(_class="glyphicon glyphicon-usd", _id="pago_tarjetas"), " Pago por tarjetas",_class="text-info"), False, URL("pago_tarjetas", "index")),

(SPAN(I(_class="glyphicon glyphicon-cog"), _id="admin_panel"), False, URL("default", "admin_panel"))
]

# ----------------------------------------------------------------------------------------------------------------------
# provide shortcuts for development. remove in production
# ----------------------------------------------------------------------------------------------------------------------



if "auth" in locals():
    auth.wikimenu()
