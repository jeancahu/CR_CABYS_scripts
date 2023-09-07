import requests, re
import hashlib
from sys import exit
from os.path import isfile

import argparse

parser = argparse.ArgumentParser()

parser.add_argument(
    '-e', '--excel-file',
    help='Nombre del Excel de cabys',
    default='cabys.xlsx',
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


def download_cabys():
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

    with open("cabys.xlsx","wb") as f:
        f.write(response.content)

def main():
    if args.download_cabys:
        print(f"Descargando el catálogo CABYS con el nombre {args.excel_file}")
        download_cabys()

## Execute main function
if __name__ == "__main__":
    main()
