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
response.info_comercial = [
    (SPAN("PC Nautas"), False, URL("informacion_comercial", "nautas")),
    (SPAN("PC Ejec. comercial"), False, URL("informacion_comercial", "ejec_comercial")),
]
response.sop_comercial = [
(SPAN("Reporte Edad de la Cta N DIAS"), False, URL("soporte_comercial","reporte_edad_cuenta"),[
    (SPAN(I(_class="glyphicon glyphicon-import")," Importar cuentas"), False, URL("soporte_comercial","importar_cuentas_edad"))
]),
(SPAN("Conexiones por deuda ",I("SIPREC",_class="label label-info")), False, URL("conexiones_por_deuda", "index"),[
    (SPAN(I(_class="glyphicon glyphicon-import")," Importar conexiones"), False, URL("conexiones_por_deuda", "importar")),
]),
(SPAN("Cargos Mensuales ",I("SGC",_class="label label-info")), False, URL("cargos_mensual", "index"),[
    (SPAN(I(_class="glyphicon glyphicon-import")," Importar cargos"), False, URL("cargos_mensual", "importar")),

(SPAN("Cargos por conexión Sector Emp. en MN"), False, URL("cargos_mensual", "cargos_por_conexion_emp_mn")),
(SPAN("Cargos por conexión Sector Emp. en MLC"), False, URL("cargos_mensual", "cargos_por_conexion_emp_mlc")),

(SPAN("Cargos por conexión Sector Res. en MN"), False, URL("cargos_mensual", "cargos_por_conexion_res_mn")),
(SPAN("Cargos por conexión Sector Res. en MLC"), False, URL("cargos_mensual", "cargos_por_conexion_res_mlc")),

    (SPAN("Servicios conectados sin aplicar cargos miscelaneos"), False, URL("cargos_mensual", "conexiones_sin_cargos")),
    (SPAN("Servicios con cargos miscelaneos que no fueron conectados"), False, URL("cargos_mensual", "cargos_sin_conexiones")),
]),
(SPAN("Cargos Diarios ",I("SGC",_class="label label-info")), False, URL("cargos_diario", "index"),[
    (SPAN(I(_class="glyphicon glyphicon-import")," Importar cargos"), False, URL("cargos_diario", "importar")),

(SPAN("Cargos por conexión Sector Emp. en MN"), False, URL("cargos_diario", "cargos_por_conexion_emp_mn")),
(SPAN("Cargos por conexión Sector Emp. en MLC"), False, URL("cargos_diario", "cargos_por_conexion_emp_mlc")),

(SPAN("Cargos por conexión Sector Res. en MN"), False, URL("cargos_diario", "cargos_por_conexion_res_mn")),
(SPAN("Cargos por conexión Sector Res. en MLC"), False, URL("cargos_diario", "cargos_por_conexion_res_mlc")),

    (SPAN("Servicios conectados sin aplicar cargos miscelaneos"), False, URL("cargos_diario", "conexiones_sin_cargos")),
    (SPAN("Servicios con cargos miscelaneos que no fueron conectados"), False, URL("cargos_diario", "cargos_sin_conexiones")),

]),
]
response.menu = [
    (SPAN(I(_class="glyphicon glyphicon-home")), False, URL("default", "index")),
    (SPAN("Sop. comercial",_id="sop_comercial"), False, URL("soporte_comercial", "index"),[
    ]),
    (SPAN("Información comercial",_id="info_comercial"), False, URL("informacion_comercial", "index"),[
    ]),
    (SPAN("Oficinas comerciales", _id="ofic_comercial"), False, URL("ofic_comercial", "index"), []),
    (SPAN(I(_class="glyphicon glyphicon-cog"), _id="admin_panel"), False, URL("default", "admin_panel",vars=dict(tablesname=("auth_user","auth_group"))))
]

if "auth" in locals():
    auth.wikimenu()
