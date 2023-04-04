import pandas as pd

excel_data_df = pd.read_excel('cabys.xlsx',
                              sheet_name='Cabys',
                              header=1, # Second row is the header
                              )

for cat9, dcat9, iva in zip(
        excel_data_df['Categoría 9'],
        excel_data_df['Descripción (categoría 9)'],
        excel_data_df['Impuesto'],
):
    if type(iva) == str:
        iva = 0

    print("IVA: {}%, Cat9: {}, DCat9: {}".format(iva*100, cat9, dcat9))
