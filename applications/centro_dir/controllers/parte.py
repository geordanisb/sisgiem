# -*- coding: utf-8 -*-

def es_hoy(fecha):
    import datetime
    hoy = datetime.date.today()
    return (fecha.year == hoy.year) and (fecha.month == hoy.month) and (fecha.day == hoy.day)

def to_name(texto):
    texto = IS_SLUG()(texto)[0]
    texto = texto.replace("-", "_")
    return texto

def index():
    import os, csv, datetime
    titulo = contenido = ""
    try:

        path = os.path.join(request.folder, 'uploads', 'iti_tickets.csv')
        if not os.path.isfile(path): redirect(URL("iti_tickets","importar"))
        btn_import = A("Importar tickets desde Información TI", _href=URL('iti_tickets', 'importar'),
                       _class="btn btn-success")

        tr_th = TR(*[v for v in VISIBLES], _class="info")
        thead = THEAD(tr_th)
        tbody = TBODY()
        tabla_ampliada = TABLE(thead, tbody, _class="table table-bordered table-striped")

        tr_th_r = TR(TH("Nuevas"), TH("Resueltas"), TH("Pendientes en el día"),TH("Pendientes acumuladas"), _class="info")
        thead_r = THEAD(tr_th_r)
        tr_td_r = TR()
        tbody_r = TBODY(tr_td_r)
        tabla_resumen = TABLE(thead_r, tbody_r, _class="table table-bordered table-striped")

        def to_date(fecha):  # establecer fecha con formato YYYY-MM-DD
            import re
            fecha_criterio = re.compile(
                "(\d?\d)[-|\s|/](\d?\d)[-|\s|/](\d{4})\s(\d?\d):(\d?\d)")  # regla para extraer fecha
            aux = fecha_criterio.search(fecha)
            return datetime.date(int(aux.group(3)), int(aux.group(2)), int(aux.group(1)))

        incidencias_hoy_nuevas = incidencias_hoy_resueltas = total = 0

        with open(path, 'rb') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=";", quotechar='"')
            campos = [to_name(campo) for campo in VISIBLES]

            for r in reader:  # Resuelto
                tr_td = TR()
                no_resuelto = (r["estado"] != "Cerrado") and (r["estado"] != "Resuelto")

                if no_resuelto:
                    tr_td = TR(*[TD(r[campo]) for campo in campos])
                    total += 1

                tbody.append(tr_td)
                if es_hoy(to_date(r["fecha_de_apertura"])):
                    incidencias_hoy_nuevas += 1
                    if r["estado"] == "Resuelto": incidencias_hoy_resueltas += 1

            tr_td_r.append(TD(incidencias_hoy_nuevas))
            tr_td_r.append(TD(incidencias_hoy_resueltas))
            tr_td_r.append(TD(incidencias_hoy_nuevas - incidencias_hoy_resueltas))
            tr_td_r.append(TD(total))
        titulo = SPAN("Parte diario"," ",A("Importar tickets desde Información TI", _href=URL('iti_tickets', 'importar'),
                       _class="btn btn-success"))
        contenido = DIV(tabla_resumen,tabla_ampliada)
    except Exception, e:
        session.contenido = btn_import
        redirect(URL('error', 'index', vars=dict(error=str(e))))
    return response.render("default/index.html",dict(titulo=titulo,contenido=contenido))