def removeNonAscii(s): return "".join(
    i for i in s if ord(i) < 128)  # para remover los caracteres basuras del archivo CSV en los campos q haga falta


def to_name(texto):
    texto = IS_SLUG()(texto)[0]
    texto = texto.replace("-", "_")
    return texto


@auth.requires_membership("editor_economia")
def importar():
    import os
    import csv
    session.forget(response)
    uploadfolder = os.path.join(request.folder, 'uploads')
    form = SQLFORM.factory(Field('file', 'upload', label="Archivo CSV",
                                 requires=IS_NOT_EMPTY(error_message="Seleccione el archivo (csv)."),
                                 uploadfolder=uploadfolder))

    if form.process().accepted:
        path = os.path.join(request.folder, 'uploads', 'inventario.csv')

        if os.path.isfile(path):
            os.remove(path)
        os.rename(os.path.join(uploadfolder, form.vars.file),
                  os.path.join(uploadfolder, 'inventario.csv'))

        with open(path, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"', )
            db.activo.truncate('RESTART IDENTITY CASCADE')
            try:
                [db.activo.insert(**{'act_fijo': r[0], 'no_inventario': r[1], 'ce_coste': r[2], 'fe_capit': r[3],
                                     'denominacion': r[4], 'val_adq': r[5].replace(',', ''),
                                     'amo_acum': r[6].replace(',', ''), 'valor_cont': r[7].replace(',', ''),
                                     'mon': r[8], 'local_': r[9], 'crit_clas': r[10]}) for r in reader if
                 (r[0] != 'Act.fijo' and r[0] != '')]
            except Exception, e:
                redirect(URL('error', vars=dict(error=str(e))))

    return dict(form=form)


@auth.requires_membership("editor_economia")
def importar_activos():
    import csv, os

    uploadfolder = os.path.join(request.folder, 'uploads')
    form = SQLFORM.factory(Field('file', 'upload', label="Archivo CSV",
                                 requires=IS_NOT_EMPTY(error_message="Seleccione el archivo (csv)."),
                                 uploadfolder=uploadfolder))
    record_out = ""
    if form.process().accepted:
        path_temp = os.path.join(request.folder, 'uploads', 'activos_temp.csv')

        try:
            if os.path.isfile(path_temp):
                os.remove(path_temp)
            os.rename(os.path.join(uploadfolder, form.vars.file), os.path.join(uploadfolder, 'activos_temp.csv'))

            with open(path_temp, "rb") as fp_in:
                reader = csv.reader(fp_in, delimiter=",", quotechar='"')
                cabecera = False
                db.activo.truncate('RESTART IDENTITY CASCADE')
                for record in reader:
                    if "Act.fijo" in record:
                        if not cabecera:
                            cabecera = [to_name(removeNonAscii(c)) for c in record if c != ""]
                            cabecera[cabecera.index("local")] = "local_"
                    elif cabecera:
                        aux = [a for a in record if a != ""]
                        record_out = dict(zip(cabecera, aux))
                        if record_out:
                            db.activo.insert(**record_out)
        except Exception, e:
            redirect(URL("error", "index", vars=dict(error=str(e))))
    return locals()
