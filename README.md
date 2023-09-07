# CR Cabys procesar el XLSX servido por el BCCR con Python y Bash

```bash
    virtualenv venv
    source venv/bin/activate

    pip install -r requirements.txt
    python download_cabys.py # Downloads XLSX
    python cabys_xlsx_to_txt.py

    # Save cabys as a txt
    python cabys_xlsx_to_txt.py > cabys.txt
    bash search_cabys.sh <palabra_de_interés>

    bash search_cabys.sh pescado
```
