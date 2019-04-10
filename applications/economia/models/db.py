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
    db = DAL(myconf.get('db.uri_postgres'),
             pool_size=myconf.get('db.pool_size'),
             migrate_enabled=myconf.get('db.migrate'),
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

from gluon.tools import Auth, Service, PluginManager

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=myconf.get('host.names'))
service = Service()
plugins = PluginManager()

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


def Responsable(id,cargo=True):
        r = db.responsable(id)
        out = '{} | {}'.format(r.nombre,r.cargo) if cargo else '{}'.format(r.nombre)
        return out

cargo = Field('cargo')
nombre = Field('nombre')
db.define_table('autoridad_facultada',nombre,cargo,format="%(nombre)s | %(cargo)s")
autoridad_facultada = Field('autoridad_facultada','reference autoridad_facultada',requires=IS_IN_DB(db,'autoridad_facultada.id',"%(nombre)s | %(cargo)s",error_message="Valor requerido"))
db.define_table('responsable',nombre,cargo,autoridad_facultada,format="%(nombre)s | %(cargo)s")

responsable = Field('responsable','reference responsable',requires=IS_IN_DB(db,'responsable.id',"%(nombre)s | %(cargo)s",error_message="Valor requerido"))


direccion = Field('direccion')
db.define_table('entidad',nombre,direccion,format='%(nombre)s')

entidad = Field('entidad','reference entidad')
local_ = Field('local_')
ce_coste = Field('ce_coste',label='Centro de costo')
db.define_table('uo',entidad,local_,ce_coste,responsable,format="%(entidad)s | %(direccion)s")

REQUERIDOS=("actfijo","n_inventario","mon","local","cecoste","denominacin_del_activo_fijo","critclas5","valadq","amo_acum","valcont","fecapit")

ce_coste = Field('cecoste',label='Centro de costo')
act_fijo = Field('actfijo',label='Activo fijo')
no_inventario = Field('n_inventario',label='No. Inventario')
fe_capit = Field('fecapit')
denominacion = Field('denominacin_del_activo_fijo',label='Denominación')
val_adq = Field('valadq')#,'double')
amo_acum = Field('amo_acum')#,'double')
valor_cont = Field('valcont')#,'double')
mon = Field('mon',label="Moneda")
local = Field('local_')
crit_clas = Field('critclas5')
sn =  Field('sn')
db.define_table('activo',act_fijo,no_inventario,ce_coste,fe_capit,denominacion,val_adq,amo_acum,valor_cont,mon,local,crit_clas,sn,format='%(n_inventario)s')

entidad_receptora = Field('entidad_receptora',label='Entidad receptora')
activo = Field('activo')
fundamentacion = Field('fundamentacion','text',label='Fundamentación')
realiza = Field('realiza')#responsable

act_fijo_mn = Field('act_fijo_mn')
act_fijo_me = Field('act_fijo_me')
val_adq_mn = Field('val_adq_mn')#,'double')
val_adq_me = Field('val_adq_me')#,'double')
amo_acum_mn = Field('amo_acum_mn')#,'double')
amo_acum_me = Field('amo_acum_me')#,'double')
db.define_table("movimiento",activo,entidad_receptora,fundamentacion,act_fijo_mn,act_fijo_me,val_adq_mn,val_adq_me,amo_acum_mn,amo_acum_me,realiza,auth.signature,migrate=1)

equipo=Field("equipo_")
fepuestser=Field("fepuestser_")
no_piezfabr=Field("npiezfabr_")
marca=Field("marca_del_equipo_")
modelo=Field("modelo_del_equipo_")
emplaz=Field("emplaz_")
local_=Field("local_")
are=Field("are_")
campo_clasificacion=Field("campo_de_clasificacin_")
act_fijo=Field("actfijo_")
cecoste=Field("cecoste_")
sello=Field("selllo_")
grau=Field("grau_")
n_inventario=Field("n_inventario_")
ce=Field("ce_")
div=Field("div_")
cepl=Field("cepl_")
gp=Field("gp_")
ptotrbres=Field("ptotrbres_")
denominacion_obj=Field("denominacin_de_objeto_tcnico_")

db.define_table("equipo_sap",equipo,fepuestser,no_piezfabr,marca,modelo,emplaz,local_,are,campo_clasificacion,act_fijo,cecoste,sello,grau,n_inventario,ce,div,cepl,gp,ptotrbres,denominacion_obj)



#auth.enable_record_versioning(db)
