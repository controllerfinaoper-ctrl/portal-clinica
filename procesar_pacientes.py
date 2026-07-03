import pandas as pd
import numpy as np
import os

def procesar_datos():
    ruta_input = "pacientes_100_registros.csv"
    
    if not os.path.exists(ruta_input):
        print(f"Error: No se encontró el archivo '{ruta_input}' en esta carpeta.")
        return

    # 1. Leer el archivo
    df = pd.read_csv(ruta_input)

    # Limpieza inicial de strings para evitar fallos por espacios vacíos
    df['Documento'] = df['Documento'].astype(str).str.strip()
    df['Telefono'] = df['Telefono'].astype(str).str.strip().replace('nan', np.nan)

    # 2. Detectar duplicados por Documento (Mantiene la primera aparición como potencial válido)
    es_duplicado = df.duplicated(subset=['Documento'], keep='first')

    # 3. Detectar teléfonos inválidos
    esta_vacio = df['Telefono'].isna() | (df['Telefono'] == '')
    contiene_letras = df['Telefono'].str.contains(r'[^0-9]', na=True, regex=True)
    menos_de_10_digitos = df['Telefono'].str.len() < 10

    es_telefono_invalido = esta_vacio | contiene_letras | menos_de_10_digitos

    # Filtrado: Es válido si NO es duplicado Y NO tiene teléfono inválido
    es_registro_valido = (~es_duplicado) & (~es_telefono_invalido)

    # 4. Genere confirmaciones.csv (Registros válidos)
    df_confirmaciones = df[es_registro_valido].copy()
    df_confirmaciones.to_csv("confirmaciones.csv", index=False)

    # 5. Genere errores.csv con registros inválidos y su motivo
    df_errores = df[~es_registro_valido].copy()
    
    motivos = []
    for idx, row in df_errores.iterrows():
        razon = []
        if es_duplicado.loc[idx]:
            razon.append("Documento Duplicado")
        if esta_vacio.loc[idx]:
            razon.append("Teléfono Vacío")
        elif contiene_letras.loc[idx]:
            razon.append("Teléfono contiene letras u otros caracteres")
        elif menos_de_10_digitos.loc[idx]:
            razon.append(f"Teléfono con menos de 10 dígitos ({len(str(row['Telefono']))})")
        
        motivos.append(" | ".join(razon))
        
    df_errores['Motivo_Error'] = motivos
    df_errores.to_csv("errores.csv", index=False)

    # 6. Muestre estadísticas
    print("\n=========================================")
    print("      ESTADÍSTICAS DE PROCESAMIENTO      ")
    print("=========================================")
    print(f"Registros Válidos (confirmaciones.csv): {len(df_confirmaciones)}")
    print(f"Registros Inválidos (errores.csv):     {len(df_errores)}")
    print("-----------------------------------------")
    
    print("\n[Cantidad por Especialidad (Solo Válidos)]")
    print(df_confirmaciones['Especialidad'].value_counts().to_string())
    
    print("\n[Cantidad por Estado (Solo Válidos)]")
    print(df_confirmaciones['Estado'].value_counts().to_string())
    print("=========================================\n")

if __name__ == "__main__":
    procesar_datos()