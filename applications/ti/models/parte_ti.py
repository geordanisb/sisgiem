#interrupciones_nauta = Field("interrupciones_nauta","text",label="Interrupciones Nauta")
#interrupciones_ejec = Field("interrupciones_ejec","text",label="Interrupciones Ejec. Comercial")
indicadores_acum = Field("indicadores_acum","text",label="Indicadores (GLPI-Acumulado)")
indicadores_mes = Field("indicadores_mes","text",label="Indicadores (GLPI-Mes)")
disp_red_acum = Field("disp_red_acum","double",label="Disponibilidad de la red (Acumulado)")
disp_red_mes = Field("disp_red_mes","double",label="Disponibilidad de la red (Mes)")
cumplimiento_cronogramas = Field("cumplimiento_cronogramas","text",label="Cumplimiento de los cronogramas")
cumplimiento_mtto = Field("cumplimiento_mtto","double",label="Cumplimiento del plan de mtto. preventivo")
estado_si = Field("estado_si","text",label="Estado de la Seguridad Informática")
cumplimiento_fact = Field("cumplimiento_fact","text",label="Cumplimiento de Facturación")
db.define_table("parte_ti",indicadores_acum,indicadores_mes,disp_red_acum,disp_red_mes,cumplimiento_mtto,cumplimiento_cronogramas,estado_si,cumplimiento_fact,auth.signature)

db.parte_ti.disp_red_acum.represent = lambda disp_red_acum,row: "{}%".format(disp_red_acum) 
db.parte_ti.disp_red_mes.represent = lambda disp_red_mes,row: "{}%".format(disp_red_mes) 
db.parte_ti.cumplimiento_mtto.represent = lambda cumplimiento_mtto,row: "{}%".format(cumplimiento_mtto) 

db.parte_ti.id.represent = lambda id,row: SPAN("{}/{}/{}".format(row.created_on.date().day,row.created_on.date().month,row.created_on.date().year),_class="badge badge-primary")

ubicacion = Field("sala",label='Salas')
posiciones = Field("posiciones",'integer')
activas = Field("activas",'integer')
observaciones = Field("observaciones",'text')
telefono = Field("telefono",label="Teléfono")
db.define_table("pc_nauta",ubicacion,posiciones,activas,observaciones,telefono,migrate=0)
db.pc_nauta.observaciones.represent = lambda dato, row: MARKMIN(dato)

no_ = Field("no_",'integer')
ctlc = Field("ctlc",label='Centro Telféfonico')
unidad_comercial = Field("unidad_comercial")
db.define_table('pc_ejec_comercial',no_,ctlc,unidad_comercial,posiciones,activas,observaciones,telefono,migrate=0)
db.pc_ejec_comercial.observaciones.represent = lambda dato, row: MARKMIN(dato)
