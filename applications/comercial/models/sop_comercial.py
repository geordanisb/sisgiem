# -*- coding: utf-8 -*-

planta = Field("planta")
oficina = Field("oficina")
servicio = Field("servicio")
motivo = Field("motivo")
fecha_conexion = Field("fecha_conexion","datetime",label="Conectado el")
conectado_por = Field("conectado_por",label="Conectado por")
db.define_table("conexiones_por_deuda",planta,oficina,servicio,motivo,fecha_conexion,conectado_por,migrate=1)
db.conexiones_por_deuda.id.readable = 0

servicio = Field("servicio")
fullUserName = Field("fullUserName",label="Nombre usuario")
importe = Field("importe","double")
oficina = Field("oficina","integer")
nombreOficina = Field("nombreOficina",label="Nombre de oficina")
concepto = Field("concepto")
fechaOperacion = Field("fechaOperacion","datetime",label="Cargado el")
moneda = Field("moneda")
db.define_table("cargos_mensual",servicio,fullUserName,importe,oficina,nombreOficina,concepto,fechaOperacion,moneda,migrate=1)
db.cargos_mensual.id.readable = 0

fecha = Field("fecha","datetime",label="Cargado el")
idAgrupacion = Field("idAgrupacion",label="Agrupación")
tipoMoneda = Field("tipoMoneda",label="Tipo de moneda")
unidad = Field("unidad")
segmentacion = Field("segmentacion",label="Segmentación")
numCuentaBancaria = Field("numCuentaBancaria",label="No. cta. bancaria")
ciclo = Field("ciclo")
oficina = Field("oficina")
concepto = Field("concepto")
claveLocalidad = Field("claveLocalidad",label="Clave localidad")
servicio = Field("servicio")
estado = Field("estado")
importe = Field("importe","double")
userName = Field("userName",label="Nombre usuario")
cierreDiario = Field("cierreDiario",label="Cierre diario")
cierreMensual = Field("cierreMensual",label="Cierre mensual")
nombreEmpleado = Field("nombreEmpleado",label="Nombre empleado")
idUsuario = Field("idUsuario")
db.define_table("cargos_diario",fecha,	idAgrupacion,	moneda,	tipoMoneda,	unidad,	segmentacion,	numCuentaBancaria,	ciclo,	oficina,	concepto,	claveLocalidad,	servicio,	estado,	importe,	userName,	cierreDiario,	cierreMensual,	nombreEmpleado,	idUsuario,migrate=1)
db.cargos_diario.id.readable = 0
db.cargos_diario.moneda.readable = 0
db.cargos_diario.numCuentaBancaria.readable = 0
db.cargos_diario.userName.readable = 0
db.cargos_diario.idUsuario.readable = 0
db.cargos_diario.cierreDiario.readable = 0


no_agrupacion = Field("no_agrupacion")
sg = Field("sg")
nomb_agrupacion = Field("nomb_agrupacion")
treinta = Field("treinta","double",label="30",default=0.0)
sesenta = Field("sesenta","double",label="60",default=0.0)
noventa = Field("noventa","double",label="90",default=0.0)
mas_de_90 = Field("mas_de_90","double",label="+90",default=0.0)
moneda = Field("moneda",requires=IS_IN_SET(["MN","MLC"]))
db.define_table("cuentas_edad",no_agrupacion,sg,nomb_agrupacion,treinta,sesenta,noventa,mas_de_90,moneda,migrate=1)
#db.cuentas_edad.drop()


"""fecha = Field("fecha","datetime")
idAgrupacion = Field("idAgrupacion")
moneda = Field("moneda")
tipoMoneda = Field("tipoMoneda")
unidad = Field("unidad")
segmentacion = Field("segmentacion")
numCuentaBancaria = Field("numCuentaBancaria")
ciclo = Field("ciclo")
oficina = Field("oficina")
concepto = Field("concepto")
claveLocalidad = Field("claveLocalidad")
servicio = Field("servicio")
estado = Field("estado")
importe = Field("importe","double")
userName = Field("userName")
cierreDiario = Field("cierreDiario")
cierreMensual = Field("cierreMensual")
nombreEmpleado = Field("nombreEmpleado")
idUsuario = Field("idUsuario")
db.define_table("cargos_mensual",fecha,	idAgrupacion,	moneda,	tipoMoneda,	unidad,	segmentacion,	numCuentaBancaria,	ciclo,	oficina,	concepto,	claveLocalidad,	servicio,	estado,	importe,	userName,	cierreDiario,	cierreMensual,	nombreEmpleado,	idUsuario,migrate=1)
db.cargos_mensual.id.readable = 0
db.cargos_mensual.moneda.readable = 0
db.cargos_mensual.numCuentaBancaria.readable = 0
db.cargos_mensual.userName.readable = 0
db.cargos_mensual.idUsuario.readable = 0
db.cargos_mensual.cierreDiario.readable = 0"""


"""mesCobro = Field("mesCobro")
idOperacion = Field("idOperacion")
fechaOperacion = Field("fechaOperacion","datetime")
fechaOperacionOficina = Field("fechaOperacionOficina","date")
oficinaOperacion = Field("oficinaOperacion","number")
nombreOficinaOperacion = Field("nombreOficinaOperacion")
idAgrupacion = Field("idAgrupacion")
moneda = Field("moneda")
tipoMoneda = Field("tipoMoneda")
tipoPago = Field("tipoPago")
nombreAgrupacion = Field("nombreAgrupacion")
unidad = Field("unidad")
oficina = Field("oficina","number")
nombreOficina = Field("nombreOficina")
ciclo = Field("ciclo")
tipoCuenta = Field("tipoCuenta")
segmentacion = Field("segmentacion")
concepto = Field("concepto")
nombreCargoMiscelaneo = Field("nombreCargoMiscelaneo")
claveLocalidad = Field("claveLocalidad")
servicio = Field("servicio")
estado = Field("estado","boolean")
importe = Field("importe","double")"""
