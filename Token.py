# --Tokens--
# formulario
# ~
# >
# <
# :
# ,
# [
# ]
# tipo
# valor
# fondo
# nombre
# valores
# evento
# entrada
# info
# "valores"
# 'valores'

class Token:
    def __init__(self,tipo,buffer,linea,columna):
        self.tipo = tipo
        self.buffer = buffer
        self.linea = linea
        self.columna = columna