# Analizador-Sint-ctico
Analizador sintáctico integrado al analizador léxico que habría realizado anteriormente.
Este proyecto implementa las dos primeras fases de un compilador:

Análisis Léxico: Convierte el código fuente en tokens usando Flex
Análisis Sintáctico: Valida la estructura del código y construye un árbol sintáctico usando descenso recursivo

El sistema puede analizar expresiones matemáticas, asignaciones de variables y detectar errores léxicos y sintácticos.

Características
Análisis Léxico (con Flex):
Reconoce números enteros y decimales
Identifica operadores matemáticos (+, -, *, /)
Detecta identificadores (nombres de variables)
Reconoce símbolos de asignación (=)
Maneja paréntesis para agrupación
Ignora espacios en blanco
Detecta caracteres no válidos

Análisis Sintáctico (Descenso Recursivo)
Valida la estructura del código según la gramática
Construye árbol sintáctico abstracto (AST)
Respeta precedencia de operadores (* y / antes que + y -)
Maneja expresiones con paréntesis
Detecta errores de sintaxis con mensajes descriptivos
Soporta múltiples sentencias

Interfaz Gráfica:
Visualización de tokens en tiempo real
Representación visual del árbol sintáctico
Dos paneles para análisis léxico y sintáctico
Mensajes de error claros y específicos
Botones para analizar y limpiar

Tecnologías Utilizadas:
Flex 2.6+ - Generador de analizadores léxicos
GCC - Compilador de C
Python 3.13.12 - Lenguaje para analizador sintáctico e interfaz
Tkinter - Biblioteca de interfaces gráficas (incluida con Python)
