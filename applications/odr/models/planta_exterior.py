# -*- coding: utf-8 -*-
servicio = Field("servicio")
tipo_servicio = Field("tipo_servicio",label="Tipo de servicio")
sector = Field("sector")
no_traza = Field("no_traza",label="No de Traza")
soporte = Field("soporte")

par_en_rack = Field("par_en_rack",label="Par en rack")
cable = Field("cable")
par = Field("par")
terminal = Field("terminal")

direccion = Field("direccion",label="Dirección")
circuito_de_linea = Field("circuito_de_linea",label="Circuito de Línea")
sitio = Field("sitio")
central = Field("central")
db.define_table("facilidades_pe",servicio,tipo_servicio,sector,no_traza,soporte,par_en_rack,cable,par,terminal,direccion,circuito_de_linea,sitio,central)

#,requires=IS_IN_DB(db,db.facilidades_pe.servicio)
servicio_pe = Field("servicio_pe")
db.define_table("servicios_nauta_hogar",servicio_pe)