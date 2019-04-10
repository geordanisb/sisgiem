# -*- coding: utf-8 -*-
#gso -> Grupo de Soporte a la Operación
from gluon import *

class SIPREC(object):

    def __init__(self,red="ra"):
        self.db = current.db
        self.auth = current.auth
        self.response = current.response
        self.request = current.request
        self.red = red
        self.reparadas = "siprec_reparadas_%s" % red
        self.pendientes_inicio = "siprec_pendientes_inicio_%s" % red
        self.pendientes_cierre = "siprec_pendientes_cierre_%s" % red
        self.servicios_ = "servicios_%s" % red

    def grid(self,tabla):
        self.db[tabla].id.readable = False
        create = editable = deletable = self.auth.has_membership("administrador") or self.auth.has_membership("editor_odr")

        g = SQLFORM.grid(self.db[tabla],create = create, editable = editable, deletable = deletable)

        #btn_importar = A(I(_class="glyphicon glyphicon-import"), _href=URL("importar"), _class="btn btn-default",
        #                 _title="Importar interrupciones desde SIPREC")
        #g.elements("div.web2py_grid ")[0].insert(0, btn_importar)
        ri = SPAN(B(" Reportes iniciales: "),self.RI(),_class="text text-success")
        g.elements("div.web2py_grid ")[0].insert(1, ri)
        return g

    def siprec_reparadas(self):
        titulo = "Interrupciones reparadas desde SIPREC"
        contenido = self.grid(self.reparadas)
        return self.response.render("default/index.html", dict(titulo=titulo, contenido=contenido))

    def siprec_pendientes_inicio(self):
        titulo = "Interrupciones pendientes al inicio desde SIPREC"
        contenido = self.grid(self.pendientes_inicio)
        return self.response.render("default/index.html", dict(titulo=titulo, contenido=contenido))

    def siprec_pendientes_cierre(self):
        titulo = "Interrupciones pendientes al cierre desde SIPREC"
        contenido = self.grid(self.pendientes_cierre)
        return self.response.render("default/index.html", dict(titulo=titulo, contenido=contenido))

    def parte(self):
        titulo = "Parte %s" % self.red.upper()
        contenido = opt = ""

        form = SQLFORM.factory(
            Field("lineas_en_servicio", "integer", label="Líneas en servicio",
                  requires=IS_INT_IN_RANGE(1, 99999, error_message="Entre un # entre 1 y 99999")),
            Field("fecha_inicio", "datetime")
        )
        if form.process().accepted:
            lineas_en_servicio = form.vars.lineas_en_servicio
            fecha_inicio = form.vars.fecha_inicio

            demora_promedio_ = SPAN(self.demora_promedio(), "hrs", _class="label label-success")
            porc_report_inic = SPAN(self.porcentaje_reportes_iniciales(lineas_en_servicio), "%",
                                    _class="label label-success")
            porc_telf_rep_3dias = SPAN(self.porciento_telf_rep_3_dias(), "%",
                                       _class="label label-success")
            porc_telf_rep_2dias = SPAN(self.porciento_telf_rep_2_dias(), "%", _class="label label-success")
            int_pedtes_diarias = SPAN(self.int_pendientes_diarias(fecha_inicio, lineas_en_servicio),
                                      _class="label label-success")
            opt = DIV(
                P(XML("Porcentaje de reportes iniciales: {}".format(porc_report_inic))),
                P(XML("Porcentaje de teléfonos reparados en los primeros tres días: {}".format(porc_telf_rep_3dias))),
                P(XML("Porcentaje de teléfonos reparados dentro de las primeras veinticuatro horas: {}".format(
                    porc_telf_rep_2dias))),
                P(XML("Interrupciones pentientes diarias: {}".format(int_pedtes_diarias))),
                P(XML("Demora promedio: {}".format(demora_promedio_))),
            )
        contenido = DIV(form, opt)
        return self.response.render("default/index.html", dict(titulo=titulo, contenido=contenido))

    def parte_por_centros(self):
        titulo = "Parte %s por CTLC" % self.red.upper()
        contenido = opt = ""

        form = SQLFORM.factory(
            Field("lineas_en_servicio", "integer", label="Líneas en servicio",
                  requires=IS_INT_IN_RANGE(1, 99999, error_message="Entre un # entre 1 y 99999")),
            Field("ctlc", "reference ctlc", requires=IS_IN_DB(self.db, self.db.ctlc.id, "%(nombre)s"), label="CTLC"),
            Field("fecha_inicio", "datetime")
        )
        if form.process().accepted:
            lineas_en_servicio = form.vars.lineas_en_servicio
            ctlc = form.vars.ctlc
            fecha_inicio = form.vars.fecha_inicio

            demora_promedio_ = SPAN(self.demora_promedio(ctlc=ctlc), "hrs", _class="label label-success")
            porc_report_inic = SPAN(self.porcentaje_reportes_iniciales(lineas_en_servicio, ctlc=ctlc), "%",
                                    _class="label label-success")
            porc_telf_rep_3dias = SPAN(self.porciento_telf_rep_3_dias(ctlc=ctlc), "%",
                                       _class="label label-success")
            porc_telf_rep_2dias = SPAN(self.porciento_telf_rep_2_dias(ctlc=ctlc), "%", _class="label label-success")
            int_pedtes_diarias = SPAN(self.int_pendientes_diarias(fecha_inicio, lineas_en_servicio, ctlc=ctlc),
                                      _class="label label-success")
            opt = DIV(
                P(XML("Porcentaje de reportes iniciales: {}".format(porc_report_inic))),
                P(XML("Porcentaje de teléfonos reparados en los primeros tres días: {}".format(porc_telf_rep_3dias))),
                P(XML("Porcentaje de teléfonos reparados dentro de las primeras veinticuatro horas: {}".format(
                    porc_telf_rep_2dias))),
                P(XML("Interrupciones pentientes diarias: {}".format(int_pedtes_diarias))),
                P(XML("Demora promedio: {}".format(demora_promedio_))),
            )
        contenido = DIV(form, opt)
        return self.response.render("default/index.html", dict(titulo=titulo, contenido=contenido))

    # Total de inter reparadas todas y/o por centro y/o por X hrs
    def RE(self,horas=None, ctlc=None):
        query = self.db[self.reparadas].id > 0
        if ctlc:
            query = self.db[self.reparadas].centro_tel == ctlc
        if horas:
            query &= self.db[self.reparadas].demora_en_hrs <= horas
        return self.db(query).count()

    # Total de Int. pendientes al cierre del mes anterior < X hrs
    def TIPCMAN(self,horas, ctlc=None):
        query = self.db[self.pendientes_inicio].demora_total <= horas
        if ctlc:
            query &= self.db[self.pendientes_inicio].centro_tel == ctlc
        return self.db(query).count()

    # Total de Int. pendientes al cierre del mes actual < X hrs
    def TIPCMAC(self,horas, ctlc=None):
        query = self.db[self.pendientes_cierre].demora_total <= horas
        if ctlc:
            query &= self.db[self.pendientes_cierre].centro_tel == ctlc
        return self.db(query).count()

    # Cant. Int. pendientes al inicio del periodo
    def RPI(self,ctlc=None):
        query = self.db[self.pendientes_inicio].id > 0
        if ctlc:
            query = self.db[self.pendientes_inicio].centro_tel == ctlc
        return self.db(query).count()

    # Cant. Int. pendientes al cierre del periodo
    def RPF(self,ctlc=None):
        query = self.db[self.pendientes_cierre].id > 0
        if ctlc:
            query = self.db[self.pendientes_cierre].centro_tel == ctlc
        return self.db(query).count()

    # Reportes iniciales
    def RI(self,ctlc=None):
        try:
            RER = self.RE(ctlc=ctlc) - self.RPI(ctlc=ctlc) + self.RPF(ctlc=ctlc)
            return RER
        except Exception, e:
            redirect(URL('error', 'index', vars=dict(error=str(e))))

    def porciento_telf_rep_2_dias(self,ctlc=None):
        try:
            re = float(self.RE(horas=24, ctlc=ctlc))
            ri = float(self.RI(ctlc=ctlc))
            tipcman = float(self.TIPCMAN(horas=24, ctlc=ctlc))
            tipcmac = float(self.TIPCMAC(horas=24, ctlc=ctlc))
            aux = round((re / (ri + tipcman - tipcmac)) * 100,3)
            return aux
        except Exception, e:
            redirect(URL('error', 'index', vars=dict(error=str(e))))

    def porciento_telf_rep_3_dias(self,ctlc=None):
        try:
            re = float(self.RE(horas=72, ctlc=ctlc))
            ri = float(self.RI(ctlc=ctlc))
            tipcman = float(self.TIPCMAN(horas=72, ctlc=ctlc))
            tipcmac = float(self.TIPCMAC(horas=72, ctlc=ctlc))
            T3D = round((re / (ri + tipcman - tipcmac) * 100),3)
            return round(T3D, 3)
        except Exception, e:
            redirect(URL('error', 'index', vars=dict(error=str(e))))

    def porcentaje_reportes_iniciales(self,lineas_en_servicio, ctlc=None):
        try:
            RER = self.RI(ctlc=ctlc)
            PORC_RI = round((float(RER) / float(lineas_en_servicio)) * 100,3)
            return PORC_RI
        except Exception, e:
            redirect(URL('error', 'index', vars=dict(error=str(e))))

    def demora_promedio(self,ctlc=None):
        try:
            query = self.db[self.reparadas].id > 0
            if ctlc:
                query = self.db[self.reparadas].centro_tel == ctlc

            promedio = self.db[self.reparadas].demora_en_hrs.avg()
            promedio = self.db(query).select(promedio).first()[promedio]
            promedio = round(promedio, 2) if promedio else 0
            return promedio
        except Exception, e:
            redirect(URL('error', 'index', vars=dict(error=str(e))))

    # Int. pendientes diarias
    def int_pendientes_diarias(self,fecha_inicio, lineas_en_servicio, ctlc=None):
        import datetime

        query = self.db[self.pendientes_inicio].fecha_reporte >= fecha_inicio
        if ctlc: query &= self.db[self.pendientes_inicio].centro_tel == ctlc
        pendientes_inicio = self.db(query).count()

        query = self.db[self.pendientes_cierre].fecha_reporte >= fecha_inicio
        if ctlc: query &= self.db[self.pendientes_cierre].centro_tel == ctlc
        pendientes_cierre = self.db(query).count()

        total_int = pendientes_inicio + pendientes_cierre

        hoy = datetime.datetime.now()
        dias = hoy - fecha_inicio  # dias -> datetime.timedelta
        return round(float(total_int) / float(dias.days) / float(lineas_en_servicio) * 100,3)

    def int_reparada_valida(self,record,red):
        servicios_ = "servicios_%s" % self.red
        SERVICIOS = [ts.tipo_servicio for ts in self.db(self.db[servicios_]).select(self.db[servicios_].tipo_servicio)]
        tabla = "siprec_reparadas_%s" % self.red
        if self.red == "ra":
            if "Z" in record["clave"]: return False #OK
            if record["central_tel"] == "CAYO LARGO": return False#OK
            if record["tipo_servicio"] not in SERVICIOS: return False #OK
            if "LD" in record["telefono"]: return False #ok
        #if record["tipo_servicio"] == "SISTEMA DE CONDUCCION DE SENALES":#ok
        #    if "LD" in record["telefono"]: return False #ok
        elif self.red == "rd":
            if record["tipo_servicio"] not in SERVICIOS: return False  # OK
        record = self.db(self.db[self.reparadas].folio == record["folio"]).select().first()#ok
        if record: return False#ok
        return True

    def importar_reparadas(self,archivo,red):
        from xlrd import open_workbook
        from Excepciones import NotCentral
        import datetime
        tabla = "siprec_reparadas_%s" % red
        book = open_workbook(archivo)
        sheet = book.sheet_by_index(0)
        campos = self.db[tabla]._fields[1:]
        self.db[tabla].truncate('RESTART IDENTITY CASCADE')
        folios = []

        for row in range(3, sheet.nrows):
            valores = sheet.row_values(row, 0)
            dict_ = dict(zip(campos, valores))
            dict_["fecha_reporte"] = datetime.datetime.strptime(valores[7], "%d/%m/%Y %H:%M:%S %p")
            dict_["fecha_cierre"] = datetime.datetime.strptime(valores[11], "%d/%m/%Y %H:%M:%S %p")
            if float(dict_["demora_en_hrs"]) < 0:
                dict_["demora_en_hrs"] = 0
            valida = self.int_reparada_valida(dict_,red)
            if valida:
                central = self.db.central_telefonica(nombre=dict_["central_tel"])
                if not central:
                    raise NotCentral(dict_["central_tel"])
                else:
                    dict_["centro_tel"] = central.ctlc.id
                if not dict_["folio"] in folios:
                    folios.append(dict_["folio"])
                self.db[tabla].insert(**dict_)

    def int_pendiente_valida(self, record, tabla,red):
        if not isinstance(record,dict):raise Exception("Se necesito un diccionario con los valores.")
        servicios_ = "servicios_%s" % red
        SERVICIOS = [ts.tipo_servicio for ts in self.db(self.db[servicios_]).select(self.db[servicios_].tipo_servicio)]
        #if record["central_tel"] == "CAYO LARGO": return False
        if record["grupo"] == "PZ": return False
        if record["tipo_servicio"] not in SERVICIOS: return False
        if "LD" in record["servicio"]: return False
        #if record["tipo_servicio"] == "SISTEMA DE CONDUCCION DE SENALES":
        #    if "LD" in record["servicio"]: return False
        if record["demora_total"] < 0: return False
        return True

#servicios => hosteados en la red y servicios de transmicion de datos;

    def importar_pendientes(self, archivo, tabla,red):
        from xlrd import open_workbook
        from Excepciones import NotCentral
        import datetime

        book = open_workbook(archivo)
        sheet = book.sheet_by_index(0)
        tabla = tabla+"_%s" % red
        campos = self.db[tabla]._fields[1:]
        folios = []
        red_ = "Primaria"
        self.db[tabla].truncate('RESTART IDENTITY CASCADE')
        for row in range(4, sheet.nrows):
            valores = sheet.row_values(row, 0)
            if not valores[3] and not valores[4]:
                red_ = "Secundaria"
                del valores[3]
                del valores[3]
            else:
                del valores[5]
                del valores[5]
            dict_ = dict(zip(campos, valores))
            dict_["fecha_reporte"] = datetime.datetime.strptime(valores[5], "%d/%m/%Y %H:%M:%S %p")  # fecha_reporte
            dict_["red"] = red_
            valido = self.int_pendiente_valida(dict_, tabla, red)  # filtros
            if valido:
                central = self.db.central_telefonica(nombre=dict_["central_tel"])
                if not central:
                    raise NotCentral(dict_["central_tel"])
                else:
                    dict_["centro_tel"] = central.ctlc.id
                if not dict_["folio"] in folios:
                    folios.append(dict_["folio"])
                    self.db[tabla].insert(**dict_)

    def importar(self):
        import os, sys

        sys.path.append(os.path.join("site-packages", "xlrd"))
        titulo = "Importar interrupciones desde SIPREC"
        uploadfolder = os.path.join(self.request.folder, 'uploads')

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
                self.importar_pendientes(path, "siprec_pendientes_inicio",self.red)
                os.unlink(path)

                path = os.path.join(uploadfolder, form.vars.pendientes_cierre)
                self.importar_pendientes(path, "siprec_pendientes_cierre",self.red)
                os.unlink(path)

                path = os.path.join(uploadfolder, form.vars.reparadas)
                self.importar_reparadas(path,self.red)
                #self.importar_reparadas(path,"rd")
                os.unlink(path)

            except Exception, e:
                redirect(URL('error', 'index', vars=dict(error=str(e))))
            else:
                redirect(URL('index'))

        return self.response.render("default/index.html", dict(titulo=titulo, contenido=form))

    # Interfaz para los tipos de servicios
    def servicios(self):
        titulo = "Servicios"
        g = self.grid(self.servicios_)
        return self.response.render("default/index.html", dict(titulo=titulo, contenido=g))

def exportar(self):
    from xlrd import open_workbook
    from Excepciones import NotCentral
    import datetime

    book = open_workbook(archivo)
    sheet = book.sheet_by_index(0)
    tabla = tabla + "_%s" % red
    campos = self.db[tabla]._fields[1:]
    folios = []
    red_ = "Primaria"
    self.db[tabla].truncate('RESTART IDENTITY CASCADE')
    for row in range(4, sheet.nrows):
        valores = sheet.row_values(row, 0)
        if not valores[3] and not valores[4]:
            red_ = "Secundaria"
            del valores[3]
            del valores[3]
        else:
            del valores[5]
            del valores[5]
        dict_ = dict(zip(campos, valores))
        dict_["fecha_reporte"] = datetime.datetime.strptime(valores[5], "%d/%m/%Y %H:%M:%S %p")  # fecha_reporte
        dict_["red"] = red_
        valido = self.int_pendiente_valida(dict_, tabla, red)  # filtros
        if valido:
            central = self.db.central_telefonica(nombre=dict_["central_tel"])
            if not central:
                raise NotCentral(dict_["central_tel"])
            else:
                dict_["centro_tel"] = central.ctlc.id
            if not dict_["folio"] in folios:
                folios.append(dict_["folio"])
                self.db[tabla].insert(**dict_)
