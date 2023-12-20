# Simulación autobus 210

proyecto que simula el recorrido de autobus 210 desde Puente alto a Estación central usando python mesa

## Autores
- Bastían Díaz
- Otro Colaborador 
- Esteban Cruces
- Matias Osses
- Francisco Riquelme

## Instalación
2. Instalar python y tenerlo en las variables de entorno
3. Instalar mesa usando el comando `pip install mesa`


## Ejecución
1. Ingresa al directorio donde esta los archivos `Lab_SBA.py` y `variables_generales.py`
2. Ejecutar el proyecto usando `python Lab_SBA.py`
3. Abrir el puerto 8529 y ejecutar simulación

## Cambiar frecuencia de salida de buses
1. en la linea 106 de `variables_generales.py` modificar el parametro FRECUENCIA_LANZAR_BUS

## Cambiar algoritmo de aceleración
1. en la linea 102 de `Lab_SBA.py` usar linea `distancia_por_recorrer = self.calcularDistancia()` para algoritmo tradicional
2. en la linea 102 de `Lab_SBA.py` usar linea `distancia_por_recorrer = self.calcularDistanciaAlgoritmoInteligente()` para algoritmo inteligente