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
        self.agregarToken('cadena',self.buffer)
        self.buffer = ''
        self.estado = 0

    def s12(self,caracter):
        if caracter.isalpha() or caracter.isdigit() or caracter in ['-',':',' ','%']:
            self.estado = 13
            self.columna += 1
            self.buffer += caracter
        elif caracter == '"':
            self.estado = 14
            self.columna += 1
            self.buffer += caracter

    def s13(self,caracter):
        if caracter.isalpha() or caracter.isdigit() or caracter in ['-',':',' ','%']:
            self.estado = 13
            self.columna += 1
            self.buffer += caracter
        elif caracter == '\'':
            self.estado = 14
            self.columna += 1
            self.buffer += caracter            
    
    def s14(self):
        self.agregarToken('cadena',self.buffer)
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

    def generarFormulario(self):
        self.codigo = self.header()
        for i in range(len(self.tokens)):
            if self.tokens[i].tipo == 'pr_tipo' and self.tokens[i + 2].buffer == '"etiqueta"':
                self.codigo += self.etiqueta(self.tokens[i + 6].buffer)
            elif self.tokens[i].tipo == 'pr_tipo' and self.tokens[i + 2].buffer == '"texto"':
                self.codigo += self.campoTexto(self.tokens[i + 6].buffer,self.tokens[i + 10].buffer)
            elif self.tokens[i].tipo == 'pr_tipo' and self.tokens[i + 2].buffer == '"grupo-radio"':
                self.codigo += self.grupoRadio(i,self.tokens[i + 6].buffer)
            elif self.tokens[i].tipo == 'pr_tipo' and self.tokens[i + 2].buffer == '"grupo-option"':
                self.codigo += self.comboBox(i,self.tokens[i + 6].buffer)
            elif self.tokens[i].tipo == 'pr_tipo' and self.tokens[i + 2].buffer == '"boton"':
                self.codigo += self.boton(self.tokens[i + 6].buffer,self.tokens[i + 10].buffer)
                
                
        self.codigo += self.final()
        with open('Formularios/form.html','w') as form:
            form.write(self.codigo)

    def etiqueta(self,valor):
        return f"""        <label for="text" class="text1">{valor.replace('"','')}</label>
        """
    
    def campoTexto(self,valor,fondo):
        return f"""        <div class="container-fields">
                    <div class="field">
                        <input type="text" placeholder="{fondo.replace('"','')}" id="{valor.replace('"','')}">
                    </div>
                </div>
        """

    def grupoRadio(self,i,nombre) -> str:
        code = f"""        <div class="columns container-fields">
                    <label for="text" class="text1">{nombre.replace('"','')}</label>
                    <div class="radio-list">"""
        if self.tokens[i + 10].tipo == 'corchete-abierto':
            for j in range(i + 11,len(self.tokens)):
                if self.tokens[j].tipo == 'corchete-cerrado':
                    break
                if self.tokens[j].tipo == 'cadena':
                    #print(self.tokens[j].buffer)
                    code += self.radioButton(self.tokens[j].buffer)
        code += """            </div>
                </div>
        """
        #print(self.code)
        return code

    def radioButton(self,valor):
        return f"""
                        <label class="radio">
                            <input class="radio-input" type="radio" name="radio">
                            <span class="radio-checkmark-box">
                                <span class="radio-checkmark"></span>
                            </span>
                            <label for="" class="text">{valor.replace("'",'')}</label>
                        </label>
        """

    def comboBox(self,i,nombre):
        code = f"""        <div class="container-flieds">
                    <form action="" method="">
                        <label for="text" class="text1">{nombre.replace('"','')}</label>
                        <select id="action" class="selectForm field" name="status">
                            <option disabled="" selected="" cl="">Seleccione una opcion</option>
        """

        if self.tokens[i + 10].tipo == 'corchete-abierto':
            for j in range(i + 11,len(self.tokens)):
                if self.tokens[j].tipo == 'corchete-cerrado':
                    break
                if self.tokens[j].tipo == 'cadena':
                    code += self.opcion(self.tokens[j].buffer)

        
        code += """                </select>
                    </form>
                </div>
        """

        return code

    def opcion(self,valor):
        return f"""                    <option class="item">{valor.replace("'",'')}</option>
        """

    def boton(self,valor,evento):
        return f"""        <button id="{evento}" class="card__btn">{valor.replace('"','')} <span>&rarr;</span></button>
        """

    def header(self) -> str:
        return """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta http-equiv="x-ua-compatible" content="ie=edge">
    <meta name="description" content="An example pen showing how a basic CSS Grid container can create a nice, responsive card layout.">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <link rel="stylesheet" href="style.css">
    <title>Formulario</title>
</head>
<body>
    <form class="form">
        <div class="card">
            <img class="card__img" src="https://visme.co/blog/wp-content/uploads/2019/11/Header-9.jpg" alt="banner">
            <div class="card__content">
                <h1 class="card__header">Formulario</h1>
        """
    
    def final(self) -> str:
        return """    </div>
        </div>
    </form>
</body>
</html>
        """