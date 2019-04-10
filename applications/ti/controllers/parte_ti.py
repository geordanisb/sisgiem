db.parte_ti.cumplimiento_fact.represent = db.parte_ti.indicadores_acum.represent = db.parte_ti.indicadores_mes.represent = db.parte_ti.cumplimiento_cronogramas.represent = lambda dato, row: MARKMIN(dato)

def index():
    titulo = "Partes del Dpto. TI"
    p = P(XML('<a href="/ti/plugin_wiki/ayuda-wiki" target="_blank" class="btn btn-sm btn-primary"><i class="glyphicon glyphicon-question-sign"></i> Ayuda para editar el texto</a>'))
    db.parte_ti.indicadores_acum.represent = db.parte_ti.indicadores_mes.represent = lambda dato, row: MARKMIN(dato)
    db.parte_ti.created_by.readable = 1
    db.parte_ti.indicadores_acum.default =("-Incidencias abiertas:     , Resueltas:     , Resolución:    \n-Solicitudes:     , Resueltas:     , Resolución:")
    db.parte_ti.indicadores_mes.default = ("-Incidencias abiertas:     , Resueltas:     , Resolución:     \n-Solicitudes:     , Resueltas:     , Resolución:")
    links = [
        lambda row: A(SPAN(I(_class="glyphicon glyphicon-ok"), " Imprimir"), _href=URL("imprimir", args=row.id),
                      _title="Dar salida a activo del taller",
                      _class="btn btn-success")]
    fields = [db.parte_ti.id,db.parte_ti.created_by,db.parte_ti.created_on]
    contenido = DIV(p,SQLFORM.grid(db.parte_ti,details=1,csv=0,searchable=0,fields=fields,links=links))
    return response.render("default/index.html", dict(titulo=titulo, contenido=contenido))


def imprimir():
    id = request.args(0,cast=int)
    parte = db.parte_ti(id)
    #titulo = "Detalles del parte del {}".format(parte.created_on.date())
    equipos_taller = ""

    if parte:
        db.parte_ti.id.readable = 0
        form = SQLFORM(db.parte_ti,parte,readonly=1)
        query = (db.activo_taller.estado != "Baja") & (db.activo_taller.estado != "Dictaminado baja")
        fields = [db.activo_taller.n_inventario,db.activo_taller.denominacin_del_activo_fijo,db.activo_taller.responsable,db.activo_taller.estado]
        equipos = db(query).select(*fields)
        indicadores_acum = SPAN(MARKMIN(parte.indicadores_acum))
        indicadores = DIV(P(B("Indicadores (GLPI-Acumulado): "),indicadores_acum),
                          P("Indicadores (GLPI-Mes): %s" % parte.indicadores_mes),
                          P("Disponibilidad de la red (Acumulado): %s" % parte.disp_red_acum),
                          P("Disponibilidad de la red (Mes): %s" % parte.disp_red_mes),
                          P("Cumplimiento del plan de mtto. preventivo.: %s" % parte.cumplimiento_mtto),
                          P("Cumplimiento de los cronogramas: %s" % parte.cumplimiento_cronogramas),
                          P("Cumplimiento de Facturación: %s" % parte.cumplimiento_fact))

        tbody = TBODY()
        equipos_taller = TABLE(tbody,_class="table table-condenced")
        for e in equipos:
            tr = TR(TD(e.n_inventario),TD(e.denominacin_del_activo_fijo),TD(e.responsable),TD(e.estado))
            tbody.append(tr)
        equipos_taller = DIV(B("Equipos en el taller"), equipos_taller)

        nautas = db(db.pc_nauta).select()
        tbody = TBODY()
        pc_nautas = TABLE(tbody, _class="table table-condenced")
        for n in nautas:
            if n.posiciones > n.activas:
                tbody.append(TR(TD(SPAN(n.sala)), TD(SPAN(n.posiciones)), TD(SPAN(n.activas)), TD(SPAN(MARKMIN(n.observaciones)))))
                pc_nautas = DIV(B("PC Nautas fuera de servicio"), pc_nautas)

        tbody = TBODY()
        pc_ejec_comercial = TABLE(tbody, _class="table table-condenced")
        ec = db(db.pc_ejec_comercial.id > 0).select()
        for n in ec:
            hay = 0
            if n.posiciones > n.activas:
                hay = 1
                tbody.append(TR(TD(SPAN(n.unidad_comercial)), TD(SPAN(n.posiciones)), TD(SPAN(n.activas)),
                            TD(SPAN(MARKMIN(n.observaciones)))))
        pc_ejec_comercial = DIV(B("PC Ejec. Comerciales fuera de servicio"),pc_ejec_comercial)
        titulo = H5("Parte del Dpto. TI {}/{}/{}".format(parte.created_on.date().day,parte.created_on.date().month,parte.created_on.date().year),_class="titulo")

    return dict(contenido=DIV(titulo,form,equipos_taller,pc_nautas,pc_ejec_comercial))