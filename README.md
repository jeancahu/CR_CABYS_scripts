# CR Cabys
Procesar el XLSX servido por el BCCR con Python y Bash

## Instalar

Instalar el ambiente virtual y las dependencias necesarias para procesar el cabys.xlsx

```bash
    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt
```


## Ejecutar

Ejecutar el script principal de Python

```bash
## Activar el ambiente virtual de python
source venv/bin/activate

## ver el texto de ayuda
python cabys.py -h

## Descargar el cabys.xlsx desde el BCCR
python cabys.py -D

# Convertir el cabys.xlsx a texto plano
python cabys.py -e cabys.xlsx -t cabys.txt

# Buscar en el cabys.txt
bash search_cabys.sh <palabra_de_interés>

## Ejemplo
bash search_cabys.sh pescado
```
