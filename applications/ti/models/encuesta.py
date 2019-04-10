# -*- coding: utf-8 -*-
pregunta = Field("pregunta")
respuesta = Field("respuesta","list:string")
activa = Field("activa","boolean")
db.define_table("encuesta",pregunta,respuesta,activa)
