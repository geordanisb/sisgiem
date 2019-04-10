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
    (SPAN("Grupo Soporte a la Operación"), False, URL('gpo_sporte_oper', 'index'), [
        (SPAN("Red de abonados"), False, URL('gso_red_abonados', 'index')),
        (SPAN("Red de datos"), False, URL('gso_red_datos', 'index')),
    ]),
    (SPAN("Centros telefónicos"), False, URL('gpo_sporte_oper', 'centros_telefonicos'), []),
    (SPAN("Centrales telefónicas"), False, URL('gpo_sporte_oper', 'centrales_telefonicas'), []),
    (SPAN(I(_class="glyphicon glyphicon-cog"), _id="admin_panel"), False, URL("odr","default", "admin_panel"))
]
response.menu_ra = [
    (SPAN("Int. pendientes al inicio"), False, URL('gso_red_abonados', 'siprec_pendientes_inicio'), []),
    (SPAN("Int. pendientes al cierre"), False, URL('gso_red_abonados', 'siprec_pendientes_cierre'), []),
    (SPAN("Int. reparadas"), False, URL('gso_red_abonados', 'siprec_reparadas'), []),
    (SPAN("Servicios"), False, URL('gso_red_abonados', 'servicios'), []),    
    (SPAN("Parte por CTLC"), False, URL('gso_red_abonados', 'parte_por_centros'), []),
    (SPAN("Int. pendientes al cierre por grupo"), False, URL('gso_red_abonados', 'int_pend_al_cierre_por_grupo'), []),
(SPAN(I(_class="glyphicon glyphicon-import"), "Importar interrupciones ", B("SIPREC", _class="badge badge-info lable-xs")), False, URL('gso_red_abonados', 'importar_interrupciones_desde_siprec')),
    #(SPAN(I(_class="glyphicon glyphicon-import"), " Importar interrupciones ", B("SIPREC", _class="badge badge-info lable-xs")), False, URL('gso_red_abonados', 'importar')),
]

response.menu_rd = [
    (SPAN("Int. pendientes al inicio"), False, URL('gso_red_datos', 'siprec_pendientes_inicio'), []),
    (SPAN("Int. pendientes al cierre"), False, URL('gso_red_datos', 'siprec_pendientes_cierre'), []),
    (SPAN("Int. reparadas"), False, URL('gso_red_datos', 'siprec_reparadas'), []),
    (SPAN("Servicios"), False, URL('gso_red_datos', 'servicios'), []),
    (SPAN("Parte por CTLC"), False, URL('gso_red_datos', 'parte_por_centros'), []),
    (SPAN("Int. pendientes al cierre por grupo"), False, URL('gso_red_datos', 'int_pend_al_cierre_por_grupo'), []),
(SPAN(I(_class="glyphicon glyphicon-import"), "Importar interrupciones ", B("SIPREC", _class="badge badge-info lable-xs")), False, URL('gso_red_datos', 'importar_interrupciones_desde_siprec')),
    #(SPAN(I(_class="glyphicon glyphicon-import")," Importar interrupciones ", B("SIPREC", _class="badge badge-info lable-xs")), False, URL('gso_red_datos', 'importar')),
]

response.menu_pe = [

(SPAN("Servicios Nauta Hogar"), False, URL('planta_exterior', 'servicios_nauta_hogar'), []),
(SPAN("Facilidades P. Ext."), False, URL('planta_exterior', 'facilidades_pe'), []),
(SPAN(I(_class="glyphicon glyphicon-import"), "Importar Servicios Nauta Hogar"), False, URL('planta_exterior', 'importar_servicios_comercializables')),
    (SPAN(I(_class="glyphicon glyphicon-import"), "Importar Facilidades P. Ext. ",
          B("SIPREC", _class="badge badge-info lable-xs")), False, URL('planta_exterior', 'importar_facilidades')),
]

if "auth" in locals():
    auth.wikimenu()
