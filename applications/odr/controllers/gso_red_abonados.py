# -*- coding: utf-8 -*-
#gso -> Grupo de Soporte a la Operación
from ParteGSO import SIPREC
siprec = SIPREC(red="ra")


if '_export_type' not in request.vars:
    db.partes_ra.porc_RI.represent = lambda porc_RI, row: SPAN(porc_RI,_class="label label-danger") if porc_RI > 5.8 else porc_RI
    db.partes_ra.porc_T3D.represent = lambda porc_T3D, row: SPAN(porc_T3D,_class="label label-danger") if porc_T3D < 94 else porc_T3D
    db.partes_ra.porc_T2D.represent = lambda porc_T2D, row: SPAN(porc_T2D,_class="label label-danger") if porc_T2D < 40 else porc_T2D

def index():
    titulo = "Red de abonados - Acciones"
    contenido = MENU(response.menu_ra)
    return response.render("default/index.html", dict(titulo=titulo, contenido=contenido))

def siprec_reparadas():
    session.forget(response)
    return siprec.siprec_reparadas()

def siprec_pendientes_inicio():
    session.forget(response)
    return  siprec.siprec_pendientes_inicio()

def siprec_pendientes_cierre():
    session.forget(response)
    return siprec.siprec_pendientes_cierre()

def parte():
    session.forget(response)
    return siprec.parte()

def parte_por_centros():
    session.forget(response)
    return siprec.parte_por_centros()

def total_lineas():
    total = 0
    for r in db(db.ctlc).select(db.ctlc.lineas_servicio_ra):
        total += int(r.lineas_servicio_ra)
    return total

def servicios():
    return siprec.servicios()

def parte_por_centros():
    #session.forget(response)
    table = ""
    titulo = "Parte por CTLC"

    try:
        centros  = [c  for c in db(db.ctlc).select(orderby=db.ctlc.no_asociado | ~db.ctlc.lineas_servicio_ra)]

        db.partes_ra.truncate('RESTART IDENTITY CASCADE')
        for c in centros:
            RE = siprec.RE(ctlc=c.id)
            RPI = siprec.RPI(ctlc=c.id)
            RPF = siprec.RPF(ctlc=c.id)
            RER = RE - RPI + RPF
            RI = siprec.RI(ctlc=c.id)
            porc_RI = round((float(RER) / float(c.lineas_servicio_ra))*100,3)

            RE_72 = siprec.RE(horas=72,ctlc=c.id)
            TIPCMAN_72 = siprec.TIPCMAN(horas=72,ctlc=c.id)
            TIPCMAC_72 = siprec.TIPCMAC(horas=72,ctlc=c.id)

            porc_T3D_denominador = float(RER + TIPCMAN_72 - TIPCMAC_72)
            porc_T3D = (float(RE_72) / porc_T3D_denominador) * 100 if porc_T3D_denominador > 0 else 0
            porc_T3D = round(porc_T3D, 2)
            #************* 24 hrs ********************
            RE_24 = siprec.RE(horas=24,ctlc=c.id)
            TIPCMAN_24 = siprec.TIPCMAN(horas=24,ctlc=c.id)
            TIPCMAC_24 = siprec.TIPCMAC(horas=24,ctlc=c.id)

            porc_T2D_denominador = float(RER + TIPCMAN_24 - TIPCMAC_24)
            porc_T2D = (float(RE_24) / porc_T2D_denominador) * 100 if porc_T2D_denominador > 0 else 0
            porc_T2D = round(porc_T2D,2)
            db.partes_ra.insert(ctlc=c.nombre, porc_RI=porc_RI, RI=RI, lineas_servicio_ra=c.lineas_servicio_ra, porc_T3D=porc_T3D, porc_T2D=porc_T2D, RPI=RPI, RPF=RPF, RE=RE, RE_72=RE_72, RE_24=RE_24, TIPCMAN_72=TIPCMAN_72,TIPCMAC_72=TIPCMAC_72, TIPCMAN_24=TIPCMAN_24, TIPCMAC_24=TIPCMAC_24)
            """tr_td = TR(TD(c.nombre),TD(porc_RI),
                       TD(RI),TD(c.lineas_servicio_ra),
                       TD(porc_T3D),TD(porc_T2D),
                       TD(RPI),TD(RPF),TD(RE),
                       TD(RE_72),TD(RE_24),
                       TD(TIPCMAN_72),TD(TIPCMAC_72),
                       TD(TIPCMAN_24),TD(TIPCMAC_24))

            tbody.append(tr_td)"""
        RE = siprec.RE()
        RPI = siprec.RPI()
        RPF = siprec.RPF()
        RER = RE - RPI + RPF
        RI = siprec.RI()
        total_l = total_lineas()
        RE_72 = siprec.RE(horas=72)
        TIPCMAN_72 = siprec.TIPCMAN(horas=72)
        TIPCMAC_72 = siprec.TIPCMAC(horas=72)
        porc_T3D_denominador = float(RER + TIPCMAN_72 - TIPCMAC_72)
        porc_T3D = (float(RE_72) / porc_T3D_denominador) * 100 if porc_T3D_denominador > 0 else 0
        RE_24 = siprec.RE(horas=24)
        TIPCMAN_24 = siprec.TIPCMAN(horas=24)
        TIPCMAC_24 = siprec.TIPCMAC(horas=24)
        porc_T3D = round(porc_T3D, 2)
        porc_RI = round((float(RER) / float(total_l)) * 100, 3)
        """tr = TR(TD("DT MTZ",_class="text-warning"), TD(porc_RI),
           TD(RI), TD(total_l),
           TD(porc_T3D), TD(porc_T2D),
           TD(RPI), TD(RPF), TD(RE),
           TD(RE_72), TD(RE_24),
           TD(TIPCMAN_72), TD(TIPCMAC_72),
           TD(TIPCMAN_24), TD(TIPCMAC_24))
tbody.append(tr)"""
        db.partes_ra.insert(ctlc="DT MTZ", porc_RI=porc_RI, RI=RI, lineas_servicio_ra=total_l, porc_T3D=porc_T3D, porc_T2D=porc_T2D, RPI=RPI,
                            RPF=RPF, RE=RE, RE_72=RE_72, RE_24=RE_24, TIPCMAN_72=TIPCMAN_72, TIPCMAC_72=TIPCMAC_72,
                            TIPCMAN_24=TIPCMAN_24, TIPCMAC_24=TIPCMAC_24)
    except Exception, e:
        redirect(URL('error', 'index', vars=dict(error=str(e))))
    else:
        redirect(URL("partes"))
    #return response.render("default/index.html", dict(titulo=titulo, contenido=table,menu_enabled=0))

def partes():
    titulo = "Partes"
    db.partes_ra.id.readable = 0
    grid = SQLFORM.grid(db.partes_ra)
    return response.render("default/index.html", dict(titulo=titulo, contenido=grid))


def int_pend_al_cierre_por_grupo():
    titulo = "Interrupciones pendientes al cierre por Grupo"
    query = db.siprec_pendientes_cierre_ra
    count = db.siprec_pendientes_cierre_ra.grupo.count()
    sum = db.siprec_pendientes_cierre_ra.demora.sum()
    rows = db(query).select(query.centro_tel,query.grupo,count,sum,groupby=db.siprec_pendientes_cierre_ra.centro_tel | db.siprec_pendientes_cierre_ra.grupo,orderby=db.siprec_pendientes_cierre_ra.centro_tel)
    
    db.int_pend_al_cierre_por_grupo_ra.truncate('RESTART IDENTITY CASCADE')
    db.int_pend_al_cierre_por_grupo_ra.id.readable = 0
    for row in rows:
        centro_tel = db.ctlc(row["siprec_pendientes_cierre_ra"].centro_tel)
        grupo = row["siprec_pendientes_cierre_ra"].grupo
        total = row["_extra"][count]
        demora = row["_extra"][sum]                
        db.int_pend_al_cierre_por_grupo_ra.insert(ctlc=centro_tel.nombre,grupo=grupo,total=total,demora=demora)
    grid = SQLFORM.grid(db.int_pend_al_cierre_por_grupo_ra,paginate=50)
    return response.render("default/index.html", dict(titulo=titulo, contenido=grid))

@auth.requires(auth.has_membership("administrador") or auth.has_membership("editor_odr"))
def importar_interrupciones_desde_siprec():
    return siprec.importar()
