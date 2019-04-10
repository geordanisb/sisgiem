def index():
    error_msg = request.vars.error
    btn_back = A("Regresar",_href=request.env.HTTP_REFERER,_class="btn btn-info")
    return dict(error_msg=error_msg,btn_back=btn_back)