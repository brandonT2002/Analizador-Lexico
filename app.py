from AnalizadorLexico import AnalizadorLexico
archivo = open('entrada.form',encoding = 'utf-8').read()
lexico = AnalizadorLexico()
lexico.analizar(archivo)
lexico.verTokens()
#lexico.verErrores()
lexico.generarFormulario()