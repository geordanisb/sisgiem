def cargar_csv():
    import os
    import csv

    uploadfolder=os.path.join(request.folder, 'uploads')
    form = SQLFORM.factory(
        Field('file', 'upload', label="Archivo CSV", requires=IS_NOT_EMPTY(error_message="Seleccione el archivo (csv)."), uploadfolder=uploadfolder))

    if form.process().accepted:
        path = os.path.join(request.folder, 'uploads', 'inventario.csv')

        if os.path.isfile(path):
            os.remove(path)
        os.rename(os.path.join(uploadfolder, form.vars.file),
            os.path.join(uploadfolder, 'inventario.csv'))
        rows = None
        with open(path, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"', )
            rows = [{'act_fijo': r[0], 'no_inventario': r[1], 'ce_coste': r[2], 'fe_capit': r[3],
                       'denominacion': r[4], 'val_adq': r[5].replace(',',''), 'amo_acum': r[6].replace(',',''), 'valor_cont': r[7].replace(',',''),
                       'mon': r[8], 'local_': r[9], 'crit_clas': r[10]} for r in reader if r[0]]
        with open(path, 'wb') as csvfile:
            writer = csvfile.writer(csvfile)
            
            #db.activo.truncate('RESTART IDENTITY CASCADE')
            #db.activo.bulk_insert(rows)

            
    return dict(form=form)

def cargar_datos():
    import os

    path = os.path.join(request.folder, 'uploads', 'inventario.csv')
    if not os.path.isfile(path): redirect(URL('preparar_csv'))

    db.activo.truncate('RESTART IDENTITY CASCADE')
    db.activo.import_from_csv_file(open(path, 'r'))
    redirect(URL('default','activos'))

    return locals()
