from Token import Token
from Error import Error


class AnalizadorLexico:
    def __init__(self):
        self.tokens = []
        self.errores = []
        self.linea = 1
        self.columna = 1
        self.estado = 0
        self.buffer = ''

    def agregarError(self,caracter):
        self.errores.append(Error(f'Caracter sin reconocer: {caracter}',self.linea,self.columna))

    def agregarToken(self,tipo,token):
        self.tokens.append(Token(tipo,token,self.linea,self.columna))
        self.i -= 1

    def verErrores(self):
        print('\nERRORES')
        for i in self.errores:
            print(i.caracter,i.linea,i.columna)

    def verTokens(self):
        print('\nTOKENS')
        for i in self.tokens:
            print(i.buffer,i.tipo,i.linea,i.columna)
    
    def s0(self,caracter):
        if caracter.isalpha():
            self.estado = 1
            self.columna += 1
            self.buffer += caracter
        elif caracter == '~':
            self.estado = 2
            self.columna += 1
            self.buffer += caracter
        elif caracter == '<':
            self.estado = 3
            self.columna += 1
            self.buffer += caracter
        elif caracter == '>':
            self.estado = 4
            self.columna += 1
            self.buffer += caracter
        elif caracter == '[':
            self.estado = 5
            self.columna += 1
            self.buffer += caracter
        elif caracter == ']':
            self.estado = 6
            self.columna += 1
            self.buffer += caracter
        elif caracter == ',':
            self.estado = 7
            self.columna += 1
            self.buffer += caracter
        elif caracter == ':':
            self.estado = 8
            self.columna += 1
            self.buffer += caracter
        elif caracter == '"':
            self.estado = 9
            self.columna += 1
            self.buffer += caracter
        elif caracter == '\'':
            self.estado = 12
            self.columna += 1
            self.buffer += caracter
        elif caracter in [' ']:
            self.columna += 1
        elif caracter in ['\n']:
            self.linea += 1
            self.columna += 1
        elif caracter == '#':
            pass
        else:
            self.agregarError(caracter)
            self.estado = 0
            self.columna += 1
            self.buffer += ''

    def s1(self,caracter):
        if caracter.isalpha():
            self.estado = 1
            self.columna += 1
            self.buffer += caracter
        else:
            if self.buffer in ['formulario','tipo','valor','fondo','nombre','valores','evento']:
                self.agregarToken(f'pr_{self.buffer}',self.buffer)
                self.buffer = ''
                self.estado = 0
            elif self.buffer in ['entrada','info']:
                self.agregarToken(f'evento_{self.buffer}',self.buffer)
                self.buffer = ''
                self.estado = 0
            else:
                self.agregarError(self.buffer)
                self.buffer = ''
                self.estado = 0

    def s2(self):
        self.agregarToken('virgulilla',self.buffer)
        self.buffer = ''
        self.estado = 0

    def s3(self):
        self.agregarToken('menor-que',self.buffer)
        self.buffer = ''
        self.estado = 0

    def s4(self):
        self.agregarToken('mayor-que',self.buffer)
        self.buffer = ''
        self.estado = 0

    def s5(self):
        self.agregarToken('corchete-abierto',self.buffer)
        self.buffer = ''
        self.estado = 0

    def s6(self):
        self.agregarToken('corchete-cerrado',self.buffer)
        self.buffer = ''
        self.estado = 0

    def s7(self):
        self.agregarToken('coma',self.buffer)
        self.buffer = ''
        self.estado = 0
    
    def s8(self):
        self.agregarToken('dos-puntos',self.buffer)
        self.buffer = ''
        self.estado = 0

    def s9(self,caracter):
        if caracter.isalpha() or caracter.isdigit() or caracter in ['-',':',' ']:
            self.estado = 10
            self.columna += 1
            self.buffer += caracter
        elif caracter == '"':
            self.estado = 11
            self.columna += 1
            self.buffer += caracter

    def s10(self,caracter):
        if caracter.isalpha() or caracter.isdigit() or caracter in ['-',':',' ']:
            self.estado = 10
            self.columna += 1
            self.buffer += caracter
        elif caracter == '"':
            self.estado = 11
            self.columna += 1
            self.buffer += caracter            
    
    def s11(self):
        self.agregarToken('param-cd',self.buffer)
        self.buffer = ''
        self.estado = 0

    def s12(self,caracter):
        if caracter.isalpha() or caracter.isdigit() or caracter in ['-',':',' ']:
            self.estado = 13
            self.columna += 1
            self.buffer += caracter
        elif caracter == '"':
            self.estado = 14
            self.columna += 1
            self.buffer += caracter

    def s13(self,caracter):
        if caracter.isalpha() or caracter.isdigit() or caracter in ['-',':',' ']:
            self.estado = 13
            self.columna += 1
            self.buffer += caracter
        elif caracter == '\'':
            self.estado = 14
            self.columna += 1
            self.buffer += caracter            
    
    def s14(self):
        self.agregarToken('param-cs',self.buffer)
        self.buffer = ''
        self.estado = 0

    def analizar(self,cadena):
        print('está analizando...')
        cadena += '#'
        self.i = 0
        while(self.i < len(cadena)):
            if self.estado == 0:
                self.s0(cadena[self.i])
            elif self.estado == 1:
                self.s1(cadena[self.i])
            elif self.estado == 2:
                self.s2()
            elif self.estado == 3:
                self.s3()
            elif self.estado == 4:
                self.s4()
            elif self.estado == 5:
                self.s5()
            elif self.estado == 6:
                self.s6()
            elif self.estado == 7:
                self.s7()
            elif self.estado == 8:
                self.s8()
            elif self.estado == 9:
                self.s9(cadena[self.i])
            elif self.estado == 10:
                self.s10(cadena[self.i])
            elif self.estado == 11:
                self.s11()
            elif self.estado == 12:
                self.s12(cadena[self.i])
            elif self.estado == 13:
                self.s13(cadena[self.i])
            elif self.estado == 14:
                self.s14()
            self.i += 1