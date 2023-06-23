from datetime import datetime
import pandas as pd

def descargar_xlsx(respuesta):
    """
    Descargar el archivo xlsx de un dataframe
    """
    actual = datetime.now()
    actual = f'{actual:%Y-%m-%d %H%M}'
    data_frame = pd.DataFrame(respuesta)
    data_frame.to_excel(f'./data/notas_{actual}.xlsx', index=False)
    return 'Descarga completa.'
