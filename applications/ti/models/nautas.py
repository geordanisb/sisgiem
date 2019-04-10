#						ram	disco
lugar = Field("lugar")
ip = Field("ip",requires = IS_IPV4(),default="0.0.0.0")
mascara_subred = Field("mascara_subred",requires = IS_IPV4(),default="0.0.0.0")
puerta_enlace = Field("puerta_enlace",requires = IS_IPV4(),default="0.0.0.0")
cod_seguridad = Field("cod_seguridad")
procesador = Field("procesador")
ram = Field("ram")
disco = Field("disco")
no_inventario = Field("no_inventario")
mac_address = Field("mac_address")
db.define_table("config_nautas",lugar,ip,mascara_subred,puerta_enlace,cod_seguridad,procesador,ram,disco,no_inventario,mac_address)
db.config_nautas.id.readable = 0
#Servicio		Tipo de servicio				Sector							No de Traza	Soporte		Ruta			Terminal	Dirección del Terminal	Circuito de Linea	Sitio	Central Digital
