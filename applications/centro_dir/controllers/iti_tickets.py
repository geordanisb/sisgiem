# -*- coding: utf-8 -*-
def to_name(texto):
    texto = IS_SLUG()(texto)[0]
    texto = texto.replace("-", "_")
    return texto

def removeNonAscii(s): return "".join(
    i for i in s if ord(i) < 128)  # para remover los caracteres basuras del archivo CSV en los campos q haga falta

@auth.requires_membership("editor_ti")
def importar():
    import csv, os

    uploadfolder = os.path.join(request.folder, 'uploads')

    form = SQLFORM.factory(
        Field('file', 'upload', label="Archivo CSV",
              requires=IS_NOT_EMPTY(error_message="Seleccione el archivo (csv)."), uploadfolder=uploadfolder))

    if form.process().accepted:

        path_temp = os.path.join(request.folder, 'uploads', 'iti_tickets_temp.csv')
        path = os.path.join(request.folder, 'uploads', 'iti_tickets.csv')

        if os.path.isfile(path_temp):
            os.remove(path_temp)
        os.rename(os.path.join(uploadfolder, form.vars.file), os.path.join(uploadfolder, 'iti_tickets_temp.csv'))

        if os.path.isfile(path):
            os.remove(path)

        with open(path_temp, "rb") as fp_in, open(path, "wb") as fp_out:
            reader = csv.reader(fp_in, delimiter=";", quotechar='"')
            etiquetas = reader.next()
            etiquetas[0] = "ID"
            campos = map(lambda i: to_name(i), etiquetas)

            writer = csv.DictWriter(fp_out, fieldnames=campos, delimiter=";", quotechar='"')
            writer.writeheader()

            for i in reader:
                r = [removeNonAscii(x) for x in i]
                record = dict(zip(campos, r))
                writer.writerow(record)
            redirect(URL("parte", "index"))

    titulo = "Importar tickets pendientes e importantes desde Información TI (ITI)"
    info = DIV(P("Siga el siguiente procedimiento:"),
               OL(
                   LI("Mostrar listado de tickets en Información TI usando la siguiente URL:",
                      A("http://informacionti.etecsa.cu/front/ticket.php",
                        _href="http://informacionti.etecsa.cu/front/ticket.php?is_deleted=0&criteria%5B0%5D%5Bfield%5D=12&criteria%5B0%5D%5Bsearchtype%5D=equals&criteria%5B0%5D%5Bvalue%5D=all&criteria%5B1%5D%5Blink%5D=AND&criteria%5B1%5D%5Bfield%5D=3&criteria%5B1%5D%5Bsearchtype%5D=equals&criteria%5B1%5D%5Bvalue%5D=6&criteria%5B2%5D%5Blink%5D=AND&criteria%5B2%5D%5Bfield%5D=14&criteria%5B2%5D%5Bsearchtype%5D=equals&criteria%5B2%5D%5Bvalue%5D=1&search=Buscar&itemtype=Ticket&start=0&_glpi_csrf_token=cf3f10993ab091667429a824ad63cf49",
                        _target="_blank")),
                   LI("Exportar los tickets que se muestran como archivo CSV al disco local (según la imagen):",
                      IMG(_src=URL('static', '/images/exportar_ti.jpg'),
                          _style="border: solid 1px #dbe2e4; padding:4px")),
                   LI("Click en Examinar... para importar el archivo CSV desde el disco local")
               ))
    contenido = DIV(info, form)
    return response.render("default/index.html", dict(titulo=titulo, contenido=contenido))

