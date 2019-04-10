folio = Field("folio")
telefono = Field("telefono")
tipo_servicio = Field("tipo_servicio")
sector = Field("sector")
cable = Field("cable")
par = Field("par")
red = Field("red")
fecha_reporte = Field("fecha_reporte","datetime")
clave = Field("clave")
grupo = Field("grupo")
demora = Field("demora","double")
fecha_cierre = Field("fecha_cierre","datetime")
despachador = Field("despachador")
demora_en_hrs = Field("demora_en_hrs","double")
central_tel = Field("central_tel")
centro_tel = Field("centro_tel","reference ctlc",requires=IS_IN_DB(db,"ctlc.id","%(nombre)s"))
gerencia = Field("gerencia")
terminal = Field("terminal")
direccion = Field("direccion")
db.define_table("siprec_reparadas_ra",folio,telefono,tipo_servicio,sector,cable,par,red,fecha_reporte,clave,grupo,demora,fecha_cierre,despachador,demora_en_hrs,central_tel,centro_tel,gerencia,terminal,direccion,migrate=0)

servicio = Field("servicio")
demora_total = Field("demora_total","double")
problema = Field("problema")

db.define_table("siprec_pendientes_inicio_ra",servicio,tipo_servicio,sector,cable,par,fecha_reporte,grupo,demora,folio,demora_total,central_tel,centro_tel,gerencia,terminal,\
                direccion,problema,red,migrate=0)

servicio = Field("servicio")
demora_total = Field("demora_total","double")
problema = Field("problema")
db.define_table("siprec_pendientes_cierre_ra",servicio,tipo_servicio,sector,cable,par,fecha_reporte,grupo,demora,folio,demora_total,central_tel,centro_tel,gerencia,terminal,\
                direccion,problema,red,migrate=0)

#db.siprec_reparadas_ra.truncate('RESTART IDENTITY CASCADE')
#db.siprec_pendientes_inicio_ra.truncate('RESTART IDENTITY CASCADE')
#db.siprec_pendientes_cierre_ra.truncate('RESTART IDENTITY CASCADE')

tipo_servicio = Field("tipo_servicio")
db.define_table("servicios_ra",tipo_servicio,migrate=1)

db.define_table("senales",Field("nombre"),migrate=1)
