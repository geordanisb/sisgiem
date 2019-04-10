create = deletable = editable = auth.has_membership('editor_economia') or auth.has_membership('administrador')
def index():
    args = lambda row:  row.id if ("view" in request.args or "edit" in request.args or "delete" in request.args)  else row["movimiento"].id
    links = [dict(header=' ', body=lambda row: A(I(_class='glyphicon glyphicon-print'), ' Imprimir',
                                                 _href=URL('movimientos', 'movimiento_activo_tpl', args=args(row)),
                                                 _class='btn btn-primary', _target='_blank'))]
    db.movimiento.id.readable = 0
    fields = [db.movimiento.id,db.activo.n_inventario,db.activo.denominacin_del_activo_fijo,db.activo.cecoste,db.activo.local_,db.movimiento.entidad_receptora]
    query = db.movimiento.activo == db.activo.id
    grid = SQLFORM.grid(query, create=create,deletable=deletable,editable=editable, links=links, fields=fields,orderby=~db.movimiento.id,maxtextlength=200)
    return dict(grid=grid)


def movimiento_activo():
    n_inventario = request.args(0)
    count = db(db.activo.n_inventario == n_inventario).count()
    activos = db(db.activo.n_inventario == n_inventario).select()

    if not activos: redirect(
        URL('error', 'index', vars=dict(error="No existe el activo con No. Inventario: {}".format(n_inventario))))

    activo_mn = activo_me = None
    db.movimiento.activo.readable = db.movimiento.activo.writable = False

    aux = db(db.entidad.id > 0).select(db.entidad.nombre, cache=(cache.ram, 3600))
    entidades = [e.nombre for e in aux]

    entidades.insert(0, "Traslado externo")
    entidades.insert(0, "Baja")
    entidades.insert(0, "Alta")
    db.movimiento.entidad_receptora.requires = IS_IN_SET(entidades, error_message="Valor requerido")

    if count == 2:
        activo_mn, activo_me = activos[0] if activos[0].mon == "CUP" else activos[1], activos[0] if activos[
                                                                                                        0].mon == "USD" else \
        activos[1]
        db.movimiento.activo.default = activo_me.id

    elif activos and activos[0].mon == "CUP":
        activo_mn = activos[0]
        db.movimiento.activo.default = activo_mn.id
    else:
        activo_me = activos[0]
        db.movimiento.activo.default = activo_me.id

    db.movimiento.act_fijo_mn.readable = db.movimiento.act_fijo_mn.writable = False
    db.movimiento.act_fijo_mn.default = activo_mn.actfijo if activo_mn else 0

    db.movimiento.act_fijo_me.readable = db.movimiento.act_fijo_me.writable = False
    db.movimiento.act_fijo_me.default = activo_me.actfijo if activo_me else 0

    db.movimiento.val_adq_mn.readable = db.movimiento.val_adq_mn.writable = False
    db.movimiento.val_adq_mn.default = activo_mn.valadq if activo_mn else 0

    db.movimiento.val_adq_me.readable = db.movimiento.val_adq_me.writable = False
    db.movimiento.val_adq_me.default = activo_me.valadq if activo_me else 0

    db.movimiento.amo_acum_mn.readable = db.movimiento.amo_acum_mn.writable = False
    db.movimiento.amo_acum_mn.default = activo_mn.amo_acum if activo_mn else 0

    db.movimiento.amo_acum_me.readable = db.movimiento.amo_acum_me.writable = False
    db.movimiento.amo_acum_me.default = activo_me.amo_acum if activo_me else 0

    uo = db(db.uo.local_ == activos[0].local_).select().first()
    responsable = uo.responsable if uo else redirect(
        URL('error', 'index', vars=dict(error="El activo pertenece a una UO que no se ha creado en el sistema.")))


    if responsable:
        db.movimiento.realiza.default = responsable
        db.movimiento.realiza.writable = db.movimiento.realiza.readable = False
    else:
        redirect(
            URL('error', 'index', vars=dict(error="El activo pertenece a una UO que no tiene responsable asignado.")))

    form = SQLFORM(db.movimiento)

    if form.process().accepted:        
        redirect(URL("movimiento_activo_tpl", args=form.vars.id))
        

    return locals()
def movimiento_activo_tpl_():
    return locals()
def movimiento_activo_tpl():
    session.forget(response)
    id = request.args(0, cast=int)
    movimiento = db.movimiento(id)

    no_consecutivo = ""
    hecho_en = request.now.date()
    if not movimiento:
        redirect(URL('activos', 'index'))

    activo = db.activo(movimiento.activo)

    no_inventario = activo.n_inventario
    uo = db(db.uo.local_ == activo.local_).select().first()

    local_receptor = ""
    receptor_responsable = Responsable(uo.responsable,cargo=False)
    ce_coste = activo.cecoste
    entidad = uo.entidad.nombre
    direccion = uo.entidad.direccion
    local_ = activo.local_

    entidad_receptora = ""
    direccion_receptora = ""
    if movimiento.entidad_receptora != "Baja" or movimiento.entidad_receptora != "Traslado externo":
        entidad_receptora = movimiento.entidad_receptora if movimiento.entidad_receptora != "Traslado externo" else ""
        e = db(db.entidad.nombre == movimiento.entidad_receptora).select().first()
        direccion_receptora = e.direccion if e else ""
        receptor_responsable = ""

    if movimiento.entidad_receptora == "Alta":
       entidad_receptora  =   entidad
       receptor_responsable = Responsable(uo.responsable,cargo=False)
       direccion_receptora = direccion
       local_receptor = "{} {}".format(ce_coste,activo.local_)
       local_ = "Almacén central"
       ce_coste = ""
    if movimiento.entidad_receptora == "Baja":
        entidad_receptora  =   ""

    denominacion = activo.denominacin_del_activo_fijo

    aux = activo.fecapit.split('.')
    fe_capit =  aux if len(aux) == 3 else ["","",""]

    val_adq_mn = movimiento.val_adq_mn
    val_adq_me = movimiento.val_adq_me

    act_fijo_mn = movimiento.act_fijo_mn
    act_fijo_me = movimiento.act_fijo_me

    amo_acum_mn = movimiento.amo_acum_mn
    amo_acum_me = movimiento.amo_acum_me

    fundamentacion = movimiento.fundamentacion

    anota_nombre = myconf.get('app.anota_nombre')
    anota_cargo = myconf.get('app.anota_cargo')
    
    

    realiza = db.responsable(movimiento.realiza)
    aprueba = realiza.autoridad_facultada.nombre if realiza.autoridad_facultada else ""
    cargo = realiza.autoridad_facultada.cargo if realiza.autoridad_facultada else ""
    realiza_nombre = realiza.nombre if (movimiento.entidad_receptora != "Baja") and (movimiento.entidad_receptora != "Alta") else anota_nombre
    realiza_cargo = realiza.cargo if (movimiento.entidad_receptora != "Baja") and (movimiento.entidad_receptora != "Alta") else anota_cargo
    db.movimiento.truncate()
    return locals()
