tiempo = ("Rápido", "Medio", "Lento")
calidad = ("Bueno","Regular","Malo")
conoce_psi_values = ("No","Parcialmente","Totalmente")
solucion_en_ma_values = ("Se soluciona en Mesa Ayuda la mayoría de las veces","Se pasa a otro especialista con frecuencia")

tiempo_atencion_llamada = Field("tiempo_atencion_llamada",label="Tiempo de atención a la llamada a los números de Mesa Ayuda",requires=IS_IN_SET(tiempo))
tiempo_atencion_queja = Field("tiempo_atencion_queja",label="Tiempo de atención a la queja hecha a través del correo ayuda.dtmt@etecsa.cu o de la aplicación Información TI",requires=IS_IN_SET(tiempo))

solucion_en_ma = Field("solucion_en_ma",label="Solución de la interrupción o solicitud",requires=IS_IN_SET(solucion_en_ma_values))

causas_no_ma = Field("causas_no_ma","text",label="Si conoce las causas que provoquen que su problema no pueda ser resuelto por la Mesa Ayuda, argumente")

trato = Field("trato",label="Trato recibido por el personal de Mesa Ayuda",requires=IS_IN_SET(calidad))
argumento_trato = Field("argumento_trato","text",label="Puede argumentar cualquiera de las respuestas dadas")

calidad_mtto_prev = Field("calidad_mtto_prev",label="Calidad percibida por Ud. en la realización de los mantenimientos preventivos",requires=IS_IN_SET(calidad))
calidad_sol_inter = Field("calidad_sol_inter",label="Calidad percibida por Ud. en la solución de las interrupciones",requires=IS_IN_SET(calidad))

tiempo_sol_por_piezas = Field("tiempo_sol_por_piezas",label="Tiempo de solución de la queja en el caso de interrupciones cuya solución depende de partes o piezas a sustituir",requires=IS_IN_SET(tiempo))

criterio_tiempo_sol_por_piezas = Field("criterio_tiempo_sol_por_piezas","text",label="Puede exponer su criterio sobre cómo mejorar este tiempo y si cree que tiene solución a nivel del Dpto. o territorio")

conoce_psi = Field("conoce_psi",label="¿Conoce el Plan de Seguridad Informática de su área?",requires=IS_IN_SET(conoce_psi_values))
conoce_psi_arg = Field("conoce_psi_arg","text",label="Argumente la respuesta anterior")

conoce_msi_values = ("Demasiado restrictivas","Necesarias","Débiles")
conoce_msi = Field("conoce_msi",label="¿Cómo considera las medidas de seguridad establecidas?",requires=IS_IN_SET(conoce_msi_values))


criterio_del_dpto = Field("criterio_del_dpto","text",label="Criterios generales sobre el funcionamiento del Dpto.")

db.define_table("encuesta_ti",tiempo_atencion_llamada,tiempo_atencion_queja,solucion_en_ma,causas_no_ma,
                trato,argumento_trato,calidad_mtto_prev,calidad_sol_inter,tiempo_sol_por_piezas,criterio_tiempo_sol_por_piezas,
                conoce_psi,conoce_psi_arg,conoce_msi,criterio_del_dpto,auth.signature)
