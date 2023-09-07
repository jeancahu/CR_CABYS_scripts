import requests, re
import hashlib
from sys import exit
from os.path import isfile

import argparse
import pandas as pd

parser = argparse.ArgumentParser()

parser.add_argument(
    '-e', '--excel-file',
    help='Nombre del Excel de cabys',
    default='cabys.xlsx',
    required=False,
    type=str,
)

parser.add_argument(
    '-t', '--xlsx-to-plain',
    help='Leer Excel de cabys y convertirlo a texto plano.',
    default='',
    required=False,
    type=str,
)

parser.add_argument(
    '-D', '--download-cabys',
    default=False,
    action='store_true',
    help='Descargar el Excel de cabys.',
)

args = parser.parse_args()

base_url="https://www.bccr.fi.cr"
cabys_url="/indicadores-economicos/cat%C3%A1logo-de-bienes-y-servicios"

def verify_html(line):
    if 'type="hidden"' in line \
       or re.search('javascript', line, re.IGNORECASE) \
       or re.search('noscript', line, re.IGNORECASE) \
       or 'type="text/css"' in line:
        return False

    if len(line) < 8:
        return False

    ## The line is correct
    return True


def download_cabys(excel_file):
    session = requests.Session()
    response = session.get(base_url+cabys_url)

    #print(str(response.text).strip())
    clean_content = re.sub("[\n\r]", '', response.text, flags=re.DOTALL)
    clean_content = re.sub("\t", ' ', clean_content, flags=re.DOTALL)
    clean_content = re.sub('id="[^"]*"', ' ', clean_content, flags=re.DOTALL)
    clean_content = re.sub('class="[^"]*"', ' ', clean_content, flags=re.DOTALL)
    clean_content = re.sub('style="[^"]*"', ' ', clean_content, flags=re.DOTALL)
    clean_content = re.sub(" * ", ' ', clean_content, flags=re.DOTALL)

    ## Patter to remove script
    pattern = re.compile(r'<script\b[^>]*>.*?</script>', re.DOTALL)
    clean_content = re.sub(pattern, '', clean_content)

    result = []
    for line in clean_content.split('</'):
        if verify_html(line):
            result.append(line)

    result = "\n".join(result)
    md5sum = hashlib.md5(result.encode('utf-8')).hexdigest()
    cabys_xls_url = re.search('[^"]*xls[^"]*', result).group(0)


    print(base_url+cabys_xls_url)
    print("Current md5sum :{}".format(md5sum))

    try:
        ## Verifica si el cabys existe
        if not isfile("cabys.xlsx"):
            raise FileNotFoundError

        with open("last_request_md5sum.txt","r") as f:

            previous_md5sum = f.read()
            print("Previous md5sum :{}".format(previous_md5sum))
            if md5sum in previous_md5sum:
                print("Page shows the same information last request")
                exit(0)
            f.close()

    except FileNotFoundError as e:
        pass

    with open("last_request_md5sum.txt","w+") as f:
        f.write(md5sum)
        f.close()

    # Download the Cabys xlsx
    response = requests.get(base_url+cabys_xls_url, allow_redirects=False)

    with open(excel_file,"wb") as f:
        f.write(response.content)

def xlsx_to_plain (output_file):
    excel_data_df = pd.read_excel(
        args.excel_file,
        sheet_name='Cabys',
        header=1, # Second row is the header
    )

    result = ''
    for cat9, dcat9, iva in zip(
            excel_data_df['Categoría 9'],
            excel_data_df['Descripción (categoría 9)'],
            excel_data_df['Impuesto'],
    ):
        if type(iva) == str:
            iva = 0

        result += "IVA: {}%, Cat9: {}, DCat9: {}\n".format(iva*100, cat9, dcat9)

    with open(output_file, "wb") as f:
        f.write(result.encode('utf-8'))

def main():
    if args.download_cabys:
        print(f"Descargando el catálogo CABYS con el nombre {args.excel_file}")
        download_cabys(excel_file = args.excel_file)

    if args.xlsx_to_plain:
        print(f"Convirtiendo el catálogo CABYS con nombre {args.excel_file} a texto plano en el archivo {args.xlsx_to_plain}")
        xlsx_to_plain(output_file = args.xlsx_to_plain)

## Execute main function
if __name__ == "__main__":
    main()
