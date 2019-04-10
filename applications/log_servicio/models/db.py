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

def Autor(id):
    a = db.auth_user(id)
    return a and "{} {}".format(a.first_name,a.last_name) or "Desconocido"

def Responsable(id, cargo=True):
    r = db.responsable(id)
    out = '{} | {}'.format(r.nombre, r.cargo) if cargo else '{}'.format(r.nombre)
    return out

#**********************************demanda de combustible******************************************

cargo = Field('cargo')
nombre = Field('nombre')
area = Field('area')
db.define_table('responsable_comb', nombre, cargo, area,format="%(nombre)s | %(cargo)s",migrate=1)

chapa = Field("chapa")
marca = Field("marca")
modelo = Field("modelo")
ind_consumo = Field("ind_consumo","double")
tipo = Field("tipo",default="Auto",requires=IS_IN_SET(("Auto","Moto")))
responsable = Field('responsable', 'reference responsable_comb',
                    requires=IS_IN_DB(db, 'responsable_comb.id', "%(nombre)s | %(cargo)s", error_message="Valor requerido"))
db.define_table("vehiculo",chapa,marca,modelo,ind_consumo,tipo,responsable,format="%(modelo)s | %(chapa)s")

fecha = Field("fecha","date",default=request.now.date(),requires=IS_DATE())
tipo_combustible = Field("tipo_combustible",requires=IS_IN_SET(myconf.get("db_postgres.tipo_combustible")))
vehiculo = Field('vehiculo', 'reference vehiculo',
                    requires=IS_IN_DB(db, 'vehiculo.id', "%(marca)s %(modelo)s | %(chapa)s"))
db.define_table("demanda",fecha,tipo_combustible,vehiculo,auth.signature)


origen = Field("origen")
destino = Field("destino")
distancia = Field("distancia","double")
db.define_table("recorrido",origen,destino,distancia,auth.signature)

recorrido = Field('recorrido', 'reference recorrido',
                    requires=IS_IN_DB(db,'recorrido.id', "%(origen)s | %(destino)s", error_message="Valor requerido"))
demanda = Field('demanda', 'reference demanda',
                    requires=IS_IN_DB(db,'demanda.id', "%(fecha)s | %(vehiculo)s", error_message="Valor requerido"))
veces = Field("veces","integer",requires=IS_NOT_EMPTY(error_message="Campo requerido"))
db.define_table("demandas_recorridos",recorrido,demanda,veces)

