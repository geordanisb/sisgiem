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
             migrate_enabled=True,
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

from gluon.tools import Auth, Service, PluginManager, current

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=myconf.get('host.names'))
service = Service()
plugins = PluginManager()
current.db = db
current.auth = auth
current.response = response
current.request = request

# -------------------------------------------------------------------------
# create all tables needed by auth if not custom tables
# -------------------------------------------------------------------------
auth.define_tables(username=False, signature=False,migrate=0)
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
auth.settings.actions_disabled=['register','request_reset_password','retrieve_username']
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

nombre = Field("nombre")
lineas_servicio = Field("lineas_servicio")
lineas_servicio_rd = Field("lineas_servicio_rd","integer")
lineas_servicio_ra = Field("lineas_servicio_ra","integer")
no_asociado = Field("no_asociado","integer")
db.define_table("ctlc",lineas_servicio,nombre,lineas_servicio_rd,lineas_servicio_ra,no_asociado,format="%(nombre)s",migrate=0)

ctlc = Field("ctlc","reference ctlc",requires=IS_IN_DB(db,db.ctlc.id,"%(nombre)s"),label="CTLC")
#ctlc = Field("ctlc")
#db.ctlc.truncate('RESTART IDENTITY CASCADE')

nombre = Field("nombre")
db.define_table("central_telefonica",nombre,ctlc,label="Central Telefónica")
#db.central_telefonica.truncate('RESTART IDENTITY CASCADE')

ctlc = Field("ctlc")
porc_RI = Field("porc_RI","double")
RI = Field("RI","double")
porc_T3D = Field("porc_T3D","double")
porc_T2D = Field("porc_T2D","double")
RPI = Field("RPI","double")
RPF = Field("RPF","double")
RE = Field("RE","double")
RE_72 = Field("RE_72","double")
RE_24 = Field("RE_24","double")
TIPCMAN_72 = Field("TIPCMAN_72","double")
TIPCMAC_72 = Field("TIPCMAC_72","double")
TIPCMAN_24 = Field("TIPCMAN_24","double")
TIPCMAC_24 = Field("TIPCMAC_24","double")
db.define_table("partes_ra",ctlc,porc_RI,RI,lineas_servicio_ra,porc_T3D,porc_T2D,RPI,RPF,RE,RE_72,RE_24,TIPCMAN_72,TIPCMAC_72,TIPCMAN_24,TIPCMAC_24,auth.signature,migrate=1)

db.define_table("partes_rd",ctlc,porc_RI,RI,lineas_servicio_rd,porc_T3D,porc_T2D,RPI,RPF,RE,RE_72,RE_24,TIPCMAN_72,TIPCMAC_72,TIPCMAN_24,TIPCMAC_24,auth.signature,migrate=1)

grupo=Field("grupo")
total=Field("total","integer")
demora=Field("demora","double")
db.define_table("int_pend_al_cierre_por_grupo_ra",ctlc,grupo,total,demora)
db.define_table("int_pend_al_cierre_por_grupo_rd",ctlc,grupo,total,demora)

auth.enable_record_versioning(db)
