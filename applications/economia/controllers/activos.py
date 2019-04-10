create = deletable = editable = auth.has_membership('editor_economia')
db.activo.mon.represent = lambda mon,row: SPAN(mon,_class="label label-info") if mon=="USD" else mon
fields = [db.activo.actfijo,db.activo.n_inventario,db.activo.cecoste,db.activo.mon,db.activo.denominacin_del_activo_fijo]

def generate_link_movement(row):
    rows = db(db.activo.n_inventario == row.n_inventario).select()
    a = A(I(_class='glyphicon glyphicon-check'), ' Movimiento',_href=URL('movimientos','movimiento_activo', args=row.n_inventario),_class='btn btn-primary')
    if row.mon == "USD": return a
    if (len(rows) == 1): return a
    else: return ""
    

links = [dict(header=' ', body=lambda row: generate_link_movement(row))]

@cache(request.env.path_info, time_expire=5, cache_model=cache.ram)
def index():
    session.forget(response)
    titulo = "Activos"
    form = SQLFORM.grid(db.activo, create=create, editable=editable, deletable=deletable, links=links, fields=fields)
    form[0].append(A(I(_class="glyphicon glyphicon-blackboard"),_href=URL("computadoras"),_title="Computadoras",_class="btn btn-default"))
    return locals()

def c():
    rows = db((db.activo.local_ == db.uo.local_)).select()
    for r in rows:
        uo = db.uo[r["uo"].id]
        uo.update_record(ce_coste=r["activo"].ce_coste)
    return locals()

def computadoras():
    session.forget(response)
    query = (db.activo.critclas5 == "HW_COMPT") & (db.activo.mon == "USD")
    form = SQLFORM.grid(query, create=create, editable=editable, deletable=deletable, links=links, fields=fields)
    form[0].append(A(I(_class="glyphicon glyphicon-hand-left"), _href=URL("index"), _title="Activos - Todos",
                     _class="btn btn-default"))
    return response.render("activos/index.html",dict(form=form,titulo="Activos - Computadoras"))
