# -*- coding: utf-8 -*-
# try something like
def removeNonAscii(s): return "".join(
    i for i in s if ord(i) < 128)  # para remover los caracteres basuras del archivo CSV en los campos q haga falta
def to_name(texto):
    texto = IS_SLUG()(texto)[0]
    texto = texto.replace("-", "_")
    return texto+"_"

@cache(request.env.path_info, time_expire=5, cache_model=cache.ram)
def index():
    db.equipo_sap.id.readable = 0
    grid = SQLFORM.grid(db.equipo_sap,csv=0)
    btn_importar = A(I(_class="glyphicon glyphicon-import"),_href=URL("importar_equipos_pm"),_class="btn btn-default",_title="Importar Équipos SAP")
    btn_migrar = A(I(_class="glyphicon glyphicon-transfer"), _href=URL("migrar"), _class="btn btn-default",_title="Migrar Équipos SAP")
    btn_exportar = A(I(_class="glyphicon glyphicon-save"), _href=URL("index",vars=dict(_export_type="tsv",keywords="",order="")), _class="btn btn-default",
                   _title="Exportar Équipos SAP para carga inicial")
    
    grid.elements("div.web2py_grid ")[0].insert(0, btn_exportar)
    grid.elements("div.web2py_grid ")[0].insert(0, btn_migrar)
    grid.elements("div.web2py_grid ")[0].insert(0, btn_importar)
    return locals()

@auth.requires(auth.has_membership("administrador") or auth.has_membership("editor_ti"))
def migrar():
    count = 0
    query = db.activo.n_inventario == db.equipo_sap.no_inventario
    query &= db.activo.mon == "USD"
    try:
        rows = db(query).select(db.equipo_sap.id,db.equipo_sap.equipo,db.activo.n_inventario,db.activo.denominacin_del_activo_fijo,
                                db.activo.actfijo,db.activo.cecoste,db.activo.local_,db.activo.fecapit,db.activo.id)
        for r in rows:
            uo = db(db.uo.local_ == r["activo"].local_).select().first()
            if uo:
                responsable = Responsable(uo.responsable,cargo=False)
                equipo_sap = db.equipo_sap(r["equipo_sap"].id)
                actfijo = r["activo"].actfijo
                local = uo.local_                
                cecoste = r["activo"].cecoste
                denominacion_obj = r["activo"].denominacin_del_activo_fijo
                equipo_sap.update_record(denominacion_obj = denominacion_obj,campo_de_clasificacion = responsable, actfijo = actfijo, local_ = local,cecoste=cecoste)
                count += 1
    except Exception, e:
                redirect(URL('error','index', vars=dict(error=str(e))))
    else: redirect(URL('index'))
    return locals()

@auth.requires(auth.has_membership("administrador") or auth.has_membership("editor_ti"))
def importar_equipos_pm():
    import os, sys

    sys.path.append(os.path.join("site-packages", "xlrd"))
    titulo = "Importar Equipos PM desde SAP PM"
    uploadfolder = os.path.join(request.folder, 'uploads')
    form = SQLFORM.factory(
        Field('equipos_pm', 'upload', label="Archivo .xlsx",
              requires=IS_NOT_EMPTY(error_message="Seleccione el archivo .xlsx"), uploadfolder=uploadfolder),

    )
    if form.process().accepted:
        try:
            path = os.path.join(uploadfolder, form.vars.equipos_pm)
            importar_equipos_pm_(path)
            os.unlink(path)
        except Exception, e:
            redirect(URL('error', 'index', vars=dict(error=str(e))))
        finally:
            if os.path.isfile(path):
                os.unlink(path)
            redirect(URL("index"))
    info = P("Exporte los equipos desde SAP PM al disco; abra el  archivo y guardelo como Excel 2010 o superior (.xlsx)",_class="alert alert-warning")
    return response.render("default/index.html", dict(titulo=titulo, contenido=DIV(info,form)))

def importar_equipos_pm_(archivo):
    from xlrd import open_workbook

    tabla = "equipo_sap"
    book = open_workbook(archivo)
    sheet = book.sheet_by_index(0)

    db[tabla].truncate('RESTART IDENTITY CASCADE')
    columnas = db[tabla]._fields[1:]

    for row in range(4, sheet.nrows):
        valores = sheet.row_values(row, 1)
        if valores[0] != u"":
            dict_ = dict(zip(columnas,valores))
            db[tabla].insert(**dict_)

def exportar():
    import csv, os
    try:
        rows = db(db.equipo_sap.id>0).select()
        path = os.path.join(request.folder,"uploads","equipos_sap_exported.csv")

        with open(path, "wb") as f:
            writer = csv.writer(f, delimiter=",")
            for r in rows:
                row = [r.equipo, r.fepuestser, r.no_serie, r.marca, r.modelo,
                       r.emplaz, r.local_,r.are, r.campo_clasificacion, r.act_fijo, r.cecoste, r.sello,
                       r.grau, r.no_inventario, r.ce, r.div, r.cepl, r.gp, r.ptotrbres, r.denominacion_obj]
                writer.writerow(row)

    except Exception, e:
        redirect(URL('error', 'index', vars=dict(error=str(e))))
    else:
        return response.stream(path, request=request,filename="equipos_sap_exported.csv", attachment=True)
