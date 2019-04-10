# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < "2.14.1":
    raise HTTP(500, "Requires web2py 2.13.3 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# app configuration made easy. Look inside private/appconfig.ini
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
myconf = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL(myconf.get('db_postgres.uri'),
             pool_size=myconf.get('db_postgres.pool_size'),
             migrate_enabled=myconf.get('db_postgres.migrate'),
             check_reserved=['all'])
else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = ['*'] if request.is_local else []
# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = myconf.get('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.get('forms.separator') or ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

from gluon.tools import Auth, Service, PluginManager, Crud

# host names must be a list of allowed host names (glob syntax allowed)
h=myconf.get('host.names')
auth = Auth(db, host_names=myconf.get('host.names'))
service = Service()
plugins = PluginManager()
crud = Crud(db)

# -------------------------------------------------------------------------
# create all tables needed by auth if not custom tables
# -------------------------------------------------------------------------
auth.define_tables(username=False,migrate=0)
from gluon.contrib.login_methods.email_auth import email_auth
auth.settings.login_methods.append(
    email_auth("mail.etecsa.cu:587", "@etecsa.cu"))



# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.get('smtp.server')
mail.settings.sender = myconf.get('smtp.sender')
mail.settings.login = myconf.get('smtp.login')
mail.settings.tls = myconf.get('smtp.tls') or False
mail.settings.ssl = myconf.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True
auth.settings.actions_disabled=['register','change_password','request_reset_password','retrieve_username','profile']
# -------------------------------------------------------------------------
# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
#
# More API examples for controllers:
#
# >>> db.mytable.insert(myfield='value')
# >>> rows = db(db.mytable.myfield == 'value').select(db.mytable.ALL)
# >>> for row in rows: print row.id, row.myfield
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# after defining tables, uncomment below to enable auditing
# -------------------------------------------------------------------------
# auth.enable_record_versioning(db)

dn = Field('dn',label="Usuario",requires=IS_NOT_EMPTY())
accountStatus = Field("accountStatus",label="Estado de la cuenta",default="Bueno",requires=IS_IN_SET(("active","noaccess","deleted","disabled")))
telephoneNumber = Field('telephoneNumber',label="Teléfono")
servicio = Field('servicio')
mail = Field('mail')
ipnavegacion = Field("ipnavegacion",label="IP de navegación",requires = IS_IPV4(),default="0.0.0.0")
cn = Field('cn',label="Nombre completo")
departmentnumber = Field('departmentnumber',label="Nombre completo")
title = Field('title',label="Cargo")
db.define_table("usuarios",cn,dn,title,departmentnumber,telephoneNumber,mail,servicio,ipnavegacion,accountStatus,format="%(dn)s")
#db.usuarios.drop()

tipo = Field("tipo",requires=IS_IN_SET(("HARDWARE","SOFTWARE")))
descripcion = Field("descripcion",'text',label="Descripción",requires=IS_NOT_EMPTY(error_message="Requerido"))
fecha_ocurrencia = Field("fecha_ocurrencia","datetime",label="Ocurrido en",default=request.now)
observaciones = Field("observaciones",'text')
db.define_table("eventos",tipo,descripcion,observaciones,fecha_ocurrencia,auth.signature)


equipo=Field("equipo")
fepuestser=Field("fepuestser")
no_serie=Field("no_serie")
marca=Field("marca_del_equipo")
modelo=Field("modelo_del_equipo")
emplaz=Field("emplaz")
local_=Field("local_")
are=Field("are_")
campo_clasificacion=Field("campo_de_clasificacion")
act_fijo=Field("actfijo")
cecoste=Field("cecoste")
sello=Field("selllo")
grau=Field("grau")
no_inventario=Field("no_inventario")
ce=Field("ce")
div=Field("div_")
cepl=Field("cepl")
gp=Field("gp")
ptotrbres=Field("ptotrbres")
denominacion_obj=Field("denominacion_obj")
db.define_table("equipo_sap",equipo,fepuestser,no_serie,marca,modelo,emplaz,local_,are,campo_clasificacion,act_fijo,cecoste,sello,grau,no_inventario,ce,div,cepl,gp,ptotrbres,denominacion_obj)
#db.equipo_sap.drop()
db.equipo_sap.truncate("RESTART IDENTITY CASCADE")

def autor(id):
    a = db.auth_user(id)
    return a and "{} {}".format(a.first_name,a.last_name) or "Desconocido"

def Responsable(id, cargo=True):
    r = db.responsable(id)
    out = '{} | {}'.format(r.nombre, r.cargo) if cargo else '{}'.format(r.nombre)
    return out

#**********************************activos_ti******************************************

cargo = Field('cargo')
nombre = Field('nombre')
db.define_table('responsable', nombre, cargo, format="%(nombre)s | %(cargo)s",migrate=1)

responsable = Field('responsable', 'reference responsable',
                    requires=IS_IN_DB(db, 'responsable.id', "%(nombre)s | %(cargo)s", error_message="Valor requerido"))

direccion = Field('direccion')
db.define_table('entidad', nombre, direccion, format='%(nombre)s')

entidad = Field('entidad', 'reference entidad')
local_ = Field('local_')
ce_coste = Field('ce_coste', label='Centro de costo')
db.define_table('uo', entidad, local_, ce_coste, responsable, format="%(entidad)s | %(direccion)s")

ce_coste = Field('cecoste', label='Centro de costo')
act_fijo = Field('actfijo', label='Activo fijo')
no_inventario = Field('n_inventario', label='No. Inventario')
fe_capit = Field('fecapit')
denominacion = Field('denominacin_del_activo_fijo', label='Denominación')
val_adq = Field('valadq')
amo_acum = Field('amo_acum')
valor_cont = Field('valcont')
mon = Field('mon', label="Moneda")
local = Field('local_')
crit_clas = Field('critclas5',requires=IS_IN_DB(db,'clasificacion_hardware.critclas5'))
sn = Field('sn')

db.define_table('activo', act_fijo, no_inventario, ce_coste, fe_capit, denominacion, val_adq, amo_acum, valor_cont, mon,
                local, crit_clas, sn, format='%(no_inventario)s')

ip = Field('ip',label="IP")
nombre = Field('nombre')
activo = Field('activo',requires=IS_IN_DB(db,'activo.n_inventario'))
tipos = ['Gestión','Nauta','Ejec. Comercial','Otras']
tipo = Field('tipo',requires=IS_IN_SET(tipos))
obs = "Motherboard: \nDisco duro: \nRAM: \nProcesador: \nFuente: \nTarjeta de red: \nMonitor: \nMouse: \nTeclado:"
observaciones = Field('observaciones','text',default=obs)
estado = Field("estado",default="Funcionando",requires=IS_IN_SET(("Funcionando","Dictaminado baja","Reparado","Pendiente de destino final","Pendiente por diagnóstico","Pendiente por pieza","Baja")))
db.define_table('activo_config',ip,nombre,activo,tipo,observaciones,estado)

#db.activo_config.truncate('RESTART IDENTITY CASCADE')


estado = Field("estado",default="Pendiente por diagnóstico",requires=IS_IN_SET(("Dictaminado baja","Reparado","Pendiente de destino final","Pendiente por diagnóstico","Pendiente por pieza","Baja")))
observaciones = Field("observaciones","text",default="Equipo SAP: \nTiquet IT: \nOrden SAP: ")
responsable = Field("responsable")
db.define_table("activo_taller",no_inventario,denominacion,responsable,local,estado,observaciones)
fecha_baja = Field("fecha_baja","date",default=request.now.date())
db.define_table("activo_taller_baja",no_inventario,denominacion,local,observaciones,fecha_baja,auth.signature)
#db.activo_taller_baja.truncate("RESTART IDENTITY CASCADE")

def update_taller(f):
    activo_taller = db(db.activo_taller.n_inventario==f['n_inventario']).select().first()
    activo_config = db(db.activo_config.activo == activo_taller['n_inventario']).select().first()
    if activo_config:    
        activo_config.update_record(estado = activo_taller.estado)#si tiene descripcion la PC se la modifico
    else:#d lo contrario creo una nueva con el estado especificado y lo otro defaults
        db.activo_config.insert(ip="127.0.0.1",nombre="",activo=f['n_inventario'],tipo="Otras",observaciones="",estado = activo_taller.estado)
    redirect(URL('activos_ti','activos_taller'))
    
db.activo_taller._after_insert.append(lambda f,id: update_taller(f))
db.activo_taller._after_update.append(lambda s,f: update_taller(f))
#db.activo_taller._after_delete.append(lambda s: asd(s))

ACTIVO_TI = myconf.get("db_postgres.critclas5")
ACTIVO_TI_MTTO = ("HW_COMPT","HW_LAPTP")

critclas5 = Field("critclas5")
db.define_table("clasificacion_hardware",critclas5)
db.clasificacion_hardware.id.readable = 0

dictamen = Field("dictamen","text",requires=IS_NOT_EMPTY())
jefe_dpto = Field("jefe_dpto")
orden_trabajo = Field("orden_trabajo",requires=IS_NOT_EMPTY())
db.define_table("dictemenes_tec",no_inventario,denominacion,no_serie,marca,modelo,local,dictamen,jefe_dpto,orden_trabajo,critclas5,auth.signature)

#db.dictemenes_tec._after_insert.append(lambda f,id: update_taller(f))
#db.dictemenes_tec._after_update.append(lambda s,f: update_taller(f))


#db.define_table("dictemenes_baja",no_inventario,denominacion,no_serie,marca,modelo,local,dictamen,jefe_dpto,orden_trabajo,critclas5)

#db.dictemenes_tec.truncate("RESTART IDENTITY CASCADE")


dictamen_tec = Field("dictamen_tec","reference dictemenes_tec")
descripcion_piezas = Field("descripcion_piezas",'list:string',label="Descripción de las partes y piezas que se entregarán al Área de Logística y Servicios")
db.define_table("destinos_finales",dictamen_tec,descripcion_piezas,denominacion,no_inventario,local,critclas5)
rows = db(db.destinos_finales.id>0).select()
for r in rows:
    x = db(db.activo.n_inventario==r.n_inventario).select().first()
    r.update_record(local_=x.local_)


#db.destinos_finales.truncate("RESTART IDENTITY CASCADE")

#db.eventos.truncate('RESTART IDENTITY CASCADE')
#db.eventos.drop()
