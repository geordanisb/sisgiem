def importar():
    import os, sys

    sys.path.append(os.path.join("site-packages", "xlrd"))
    titulo = "Importar interrupciones desde SIPREC"
    uploadfolder = os.path.join(request.folder, 'uploads')

    form = SQLFORM.factory(
        Field('pendientes_inicio', 'upload', label="Interrupciones pendientes al inicio desde SIPREC",
              requires=IS_NOT_EMPTY(error_message="Seleccione el archivo (csv)."), uploadfolder=uploadfolder),
        Field('pendientes_cierre', 'upload', label="Interrupciones pendientes al cierre desde SIPREC",
              requires=IS_NOT_EMPTY(error_message="Seleccione el archivo (csv)."), uploadfolder=uploadfolder),
        Field('reparadas', 'upload', label="Interrupciones reparadas desde SIPREC",
              requires=IS_NOT_EMPTY(error_message="Seleccione el archivo (csv)."), uploadfolder=uploadfolder)
    )
    if form.process().accepted:
        try:
            path = os.path.join(uploadfolder, form.vars.pendientes_inicio)
            importar_pendientes(path, "siprec_pendientes_inicio")
            os.unlink(path)

            path = os.path.join(uploadfolder, form.vars.pendientes_cierre)
            importar_pendientes(path, "siprec_pendientes_cierre")
            os.unlink(path)

            path = os.path.join(uploadfolder, form.vars.reparadas)
            importar_reparadas(path)
            os.unlink(path)

        except Exception, e:
            redirect(URL('error', 'index', vars=dict(error=str(e))))
        else:
            redirect(URL('importar'))

    return response.render("default/index.html", dict(titulo=titulo, contenido=form))

def importar_reparadas(archivo):
    from xlrd import open_workbook
    from Excepciones import NotCentral

    tabla = "siprec_reparadas"
    book = open_workbook(archivo)
    sheet = book.sheet_by_index(0)
    campos = db[tabla]._fields[1:]
    db[tabla].truncate('RESTART IDENTITY CASCADE')
    folios = []

    for row in range(3, sheet.nrows):
        valores = sheet.row_values(row, 0)
        #valida = int_reparada_valida(valores,red)
        #if valida:
        #valores[7] = datetime.datetime.strptime(valores[7], "%d/%m/%Y %H:%M:%S %p")  # fecha_reporte
        #valores[11] = datetime.datetime.strptime(valores[11], "%d/%m/%Y %H:%M:%S %p")  # fecha_cierre
        dict_ = dict(zip(campos, valores))
        central = db.central_telefonica(nombre=dict_["central_tel"])
        if not central:
            raise NotCentral(dict_["central_tel"])
        else:
            dict_["centro_tel"] = central.ctlc.id
        if not valores[0] in folios:
            folios.append(valores[0])
            db[tabla].insert(**dict_)


def importar_pendientes(archivo,tabla):
    from xlrd import open_workbook
    from Excepciones import NotCentral
    import datetime

    book = open_workbook(archivo)
    sheet = book.sheet_by_index(0)
    campos = db[tabla]._fields[1:]
    folios = []

    db[tabla].truncate('RESTART IDENTITY CASCADE')
    for row in range(4, sheet.nrows):
        valores = sheet.row_values(row, 0)

        # valido = int_pendiente_valida(valores, tabla, red)  # filtros
        # if valido:
        valores[7] = datetime.datetime.strptime(valores[7], "%d/%m/%Y %H:%M:%S %p")  # fecha_reporte
        dict_ = dict(zip(campos, valores))

        central = db.central_telefonica(nombre=dict_["central_tel"])
        if not central:
            raise NotCentral(dict_["central_tel"])
        else:
            dict_["centro_tel"] = central.ctlc.id

        if not valores[10] in folios:
            folios.append(valores[10])
            db[tabla].insert(**dict_)