# -*- coding: utf-8 -*-
def index():
    redirect(URL('cargar_archivos'))
    return locals()
@auth.requires_membership("editor_economia")
def cargar_archivos():
    import os, sys
    errores = []
    
    sys.path.append(os.path.join("site-packages", "xlrd"))
    titulo = "Importar archivo de direcciones de Capital Humano"
    uploadfolder = os.path.join(request.folder, 'uploads')
    downloadfolder = os.path.join(request.folder, 'static','economia')
    enlace = ""
    xs = ""
    form = SQLFORM.factory(
        Field('datos_capital_humano', 'upload', label="Archivo de datos en Capital Humano",requires=IS_NOT_EMPTY(error_message="Seleccione el archivo excel."), uploadfolder=uploadfolder),
        Field('dbf', 'upload', label="Archivo dbf de trabajadores sin tarjeta",
              requires=IS_NOT_EMPTY(error_message="Seleccione el archivo (dbf)."), uploadfolder=downloadfolder)
    )
    if form.process().accepted:
        try:
            path = os.path.join(request.folder,'uploads', form.vars.datos_capital_humano)
            path_dbf = os.path.join(downloadfolder, 'ban1.dbf')

            if os.path.isfile(path_dbf):
                os.remove(path_dbf)
            os.rename(os.path.join(downloadfolder, form.vars.dbf), os.path.join(downloadfolder, 'ban1.dbf'))

            xs = importar_archivos(path,errores)
            if os.path.isfile(path):
                os.remove(path)

            enlace = A(I(_class="glyphicon glyphicon-floppy-save")," Descargar archivo",_href=URL('static/economia','ban1.dbf'),_download="ban1.dbf",_class="btn btn-primary")
        except Exception, e:
            if os.path.isfile(path):
                os.remove(path)
            redirect(URL('error', 'index', vars=dict(error=str(e))))

    errores = errores if errores else ""
    not_founds = DIV(H2("Elementos no encontrados en el archivo de nómina:"),
                     *[P(i['value'][0], ": ", i['value'][1]) for i in errores if i['type'] == "not_found"],
                     _class="alert alert-warning") if errores else ""
    return response.render("default/index.html", dict(titulo=titulo, contenido=DIV(form,enlace,not_founds)))

def importar_archivos(path,errores):
    from xlrd import open_workbook
    from dbfpy import dbf
    import os
    path_dbf = os.path.join(request.folder, 'static', 'economia', 'ban1.dbf')
    db = dbf.Dbf(path_dbf)

    import os
    book = open_workbook(path)
    sheet = book.sheet_by_index(0)

    values = []
    d = {}

    for row in range(5, sheet.nrows):
        try:
            v = sheet.row_values(row, 0)
            def has_ntilde(s):
                if u'\xd1' in s:
                    return True
                return False

            NOMBRE = APELLIDO_1 = APELLIDO_2 =""
            DIR_PERSO1 = normalizar_dir(normalizar_dir(v[8])) if type(v[8])!=float else str(v[8])
            DIR_PERSO2 = normalizar_dir(normalizar_dir(v[9])) if type(v[9])!=float else str(v[9])
            NUM_IDEPER = str(v[6]).split('.')[0]

            if not has_ntilde(v[3]):
                APELLIDO_1 = elimina_tildes_nombre(v[3]).upper()
            if not has_ntilde(v[4]):
                APELLIDO_2 = elimina_tildes_nombre(v[4]).upper()
            if not has_ntilde(v[2]):
                NOMBRE = elimina_tildes_nombre(v[2]).upper()

            d = {'NOMBRE':NOMBRE.encode('utf-8'),'APELLIDO_1':APELLIDO_1.encode('utf-8'),'APELLIDO_2':APELLIDO_2.encode('utf-8'),'NUM_IDEPER':NUM_IDEPER,'DIR_PERSO1':DIR_PERSO1.encode('utf-8'),'DIR_PERSO2':DIR_PERSO2.encode('utf-8')}
            values.append(d)
        except Exception, e:
            errores.append({'type':'error','value':(e,v)})
    set_records(values, errores)



def copy_dbf():
    import os
    import shutil
    srcfile = os.path.join(request.folder,'databases','pago_tarjetas_dbf','ban1.dbf')
    dstroot = os.path.join(request.folder,'static','economia','ban1.dbf')
    shutil.copyfile(srcfile, dstroot)

def set_records(values,errores):
    from dbfpy import dbf
    import os
    path_dbf = os.path.join(request.folder, 'static', 'economia', 'ban1.dbf')
    db = dbf.Dbf(path_dbf)

    try:
        for rec in db:
            found = False
            for v in values:
                if rec['NUM_IDEPER'] == v['NUM_IDEPER']:
                    rec["DIR_PERSO1"] = v["DIR_PERSO1"].upper()
                    rec["DIR_PERSO2"] = v["DIR_PERSO2"].upper()
                    rec.store()
                    if v["APELLIDO_1"]:
                        rec["APELLIDO_1"] = v["APELLIDO_1"]
                        rec.store()
                    if v["APELLIDO_2"]:
                        rec["APELLIDO_2"] = v["APELLIDO_2"]
                        rec.store()
                    rec["NOMBRE"] = v["NOMBRE"]
                    rec["NOMB_APELL"] = rec["NOMBRE"] + ' ' + rec["APELLIDO_1"] + ' ' + rec["APELLIDO_2"]
                    rec.store()
                    found = True
                    break
            if not found:
                errores.append({'type':'not_found','value':(rec["NUM_IDEPER"],rec["NOMB_APELL"])})

    except Exception,e:
        errores.append((str(e),v))
    finally:
        db.close()

def new_record(values,db):
    rec = db.newRecord()
    rec["COD_TIPID"] = 'CI'
    rec["COD_PAEXID"] = '247'
    rec["NUM_IDEPER"] = values["NUM_IDEPER"]
    rec["APELLIDO_1"] = values["APELLIDO_1"].upper()
    rec["APELLIDO_2"] = values["APELLIDO_2"].upper()
    rec["NOMBRE"] = values["NOMBRE"].upper()
    rec["NOMB_APELL"] = rec["NOMBRE"] + ' ' + rec["APELLIDO_1"] + ' ' + rec["APELLIDO_2"]
    rec["DIR_PERSO1"] = values["DIR_PERSO1"].upper()
    rec["DIR_PERSO2"] = values["DIR_PERSO2"].upper()
    rec["EST_MLC"] = False
    rec["NOM_MNAC"] = True
    rec["NUM_IDEBEN"] = ""
    rec["AP1_BENEF"] = ""
    rec["AP2_BENEF"] = ""
    rec["NOMBRE_B"] = ""
    rec["CTA_MNAC"] = ""
    rec["CTA_MLC"] = ""
    rec.store()

def normalizar_dir(cadena):
    cadena = elimina_tildes_dir(cadena)
    cadena = cadena.replace("Calle", "C.")
    cadena = cadena.replace("calle", "C.")
    cadena = cadena.replace("CALLE","C.")
    cadena = cadena.replace("Call", "C.")
    cadena = cadena.replace("CALL", "C.")
    cadena = cadena.replace("Matanzas","MTZ")
    cadena = cadena.replace("MATANZAS","MTZ")
    cadena = cadena.replace(" MATAN","MTZ")
    cadena = cadena.replace("AVENIDA","AVE.")
    cadena = cadena.replace("PROVINCIA","PROV.")
    cadena = cadena.replace("REPARTO","RPTO.")
    cadena = cadena.replace("No. ",'#')
    cadena = cadena.replace("No.", '#')
    cadena = cadena.replace("NO ", '#')
    cadena = cadena.replace("NO. ","#")
    cadena = cadena.replace("NO.","#")
    cadena = cadena.replace("No ","#")
    cadena = cadena.replace("no ","#")
    cadena = cadena.replace("no. ","#")
    cadena = cadena.replace("NRO ","#")
    cadena = cadena.replace("Nro ","#")
    cadena = cadena.replace("nro ", "#")
    cadena = cadena.replace("# ","#")
    return cadena

def elimina_tildes_dir(s):
    import unicodedata
    if s:
        s = remove_unicode(s)
        return ''.join((c for c in unicodedata.normalize('NFD', s) if (unicodedata.category(c) != 'Mn')))

def elimina_tildes_nombre(s):
    import unicodedata
    if s:
        s = remove_unicode(s)
        return ''.join((c for c in unicodedata.normalize('NFD', s) if (unicodedata.category(c) != 'Mn')))

def remove_unicode(s):
    if type(s) == str:
        s = s.replace('\xe1','a')
        s = s.replace('\xe9', 'e')
        s = s.replace('\xa8', 'u')
        s = s.replace('\xf3', 'o')
        s = s.replace(u'・', '-')
        s = s.replace('\xd1', 'ñ')
        s = s.replace('0xd1', 'Ñ')
        s = s.replace('\xe1', 'a')
    return s
