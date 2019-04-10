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
    (SPAN("Activos", _id="usuarios"), False, URL("activos_ti","index"),[
    (SPAN("Activos por No. Inventario", _id="usuarios"), False, URL("activos_ti","activos_por_no_inv")),
    (SPAN(I(_class="glyphicon glyphicon-wrench"), " Activos en el taller"), False, URL("activos_ti", "activos_taller")),

(SPAN(I(_class="glyphicon glyphicon-list-alt"), " Dictamenes técnicos"), False, URL("activos_ti", "dictemenes_tec")),

(SPAN(I(_class="glyphicon glyphicon-briefcase"), " Destinos finales"), False, URL("activos_ti", "destinos_finales")),


(SPAN(I(_class="glyphicon glyphicon-remove text-danger"), " Activos dados de baja"), False, URL("activos_ti", "activos_de_baja")),
    (SPAN(I(_class="glyphicon glyphicon-erase"), " PC por entidad para mtto"), False, URL("activos_ti", "pc_por_entidad")),
(SPAN("Hardware por entidad"), False, URL("activos_ti", "por_entidades")),
    (SPAN("Hardware por UO"), False, URL("activos_ti", "por_uo")),
        (SPAN("Config. de PC Nautas"),False,URL("nautas","index")),
(SPAN("Activos SAP PM", _id="equipos_sap"), False, URL("equipos_sap","index")),

    #(SPAN("Unidades organizativas", _id="uo"), False, URL("activos_ti","hardware_por_uo")),
    ]),
(SPAN("Parte TI", _id="parte_ti"), False, URL("parte_ti","index")),
(SPAN("Encuesta TI", _id="encuesta_ti"), False, URL("encuesta_ti","index")),
    (SPAN("Usuarios", _id="usuarios"), False, URL("usuarios","index")),

    (SPAN("Bitácora de eventos", _id="bitacora"), False, URL("bitacora", "eventos")),
    (SPAN("WIKI", _id="wiki"), False, URL("plugin_wiki", "index")),
    (SPAN(I(_class="glyphicon glyphicon-cog"), _id="admin_panel"), False, URL("ti","default", "admin_panel"))
]

DEVELOPMENT_MENU = True

# ----------------------------------------------------------------------------------------------------------------------
# provide shortcuts for development. remove in production
# ----------------------------------------------------------------------------------------------------------------------

def _():
    # ------------------------------------------------------------------------------------------------------------------
    # shortcuts
    # ------------------------------------------------------------------------------------------------------------------
    app = request.application
    ctr = request.controller
    # ------------------------------------------------------------------------------------------------------------------
    # useful links to internal and external resources
    # ------------------------------------------------------------------------------------------------------------------


if DEVELOPMENT_MENU:
    _()

if "auth" in locals():
    auth.wikimenu()
