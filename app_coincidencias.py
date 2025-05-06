import re
from difflib import SequenceMatcher
import pandas as pd
import streamlit as st
from io import BytesIO
from PIL import Image

# Configuración de la página
st.set_page_config(page_title="Coincidencias de Nombres", layout="wide")

# Logo (coloca un archivo 'logo.png' en el mismo directorio)
try:
    logo = Image.open("logo.png")
    st.image(logo, width=150)
except Exception:
    pass

st.title("App para detectar coincidencias de nombres entre dos archivos")

# Nota destacada sobre el orden de archivos
st.markdown(
    "<h4 style='color:#FF4B4B;'>⚠️ Primero sube el archivo de **Wise**, luego el archivo de **BackOffice**.</h4>",
    unsafe_allow_html=True
)

# Sidebar: configuración de columnas y umbral
st.sidebar.header("Configuración")
col1 = st.sidebar.text_input("Columna de nombres en archivo Wise", "Contacto Nombre").strip()
col1_id = st.sidebar.text_input("Columna extra (ID) en archivo Wise (opcional)", "Caso #").strip()
col2 = st.sidebar.text_input("Columna de nombres en archivo BackOffice", "Cli Nombre").strip()
col2_id = st.sidebar.text_input("Columna extra (ID) en archivo BackOffice (opcional)", "Fic Numero").strip()
threshold = st.sidebar.slider("Umbral de similitud", 0.5, 1.0, 0.8)

# Función de normalización
def normalize(name: str) -> str:
    if pd.isna(name):
        return ""
    name_clean = re.sub(r"[^\w\s]", "", str(name), flags=re.UNICODE)
    tokens = name_clean.lower().split()
    tokens.sort()
    return " ".join(tokens)

# Lógica de coincidencias
def find_matches(df1: pd.DataFrame, df2: pd.DataFrame, threshold: float) -> pd.DataFrame:
    df1 = df1.copy()
    df2 = df2.copy()
    # Normalizar nombres y eliminar vacíos
    df1['norm'] = df1[col1].apply(normalize)
    df2['norm'] = df2[col2].apply(normalize)
    df1 = df1[df1['norm'] != '']
    df2 = df2[df2['norm'] != '']

    # Bloqueo para optimizar
    df1['block'] = df1['norm'].str[:4]
    df2['block'] = df2['norm'].str[:4]
    common_blocks = set(df1['block']).intersection(df2['block'])
    common_blocks.discard('')

    matches = []
    for block in common_blocks:
        sub1 = df1[df1['block'] == block]
        sub2 = df2[df2['block'] == block]
        for _, r1 in sub1.iterrows():
            for _, r2 in sub2.iterrows():
                sim = SequenceMatcher(None, r1['norm'], r2['norm']).ratio()
                if sim >= threshold:
                    match = {
                        col1: r1[col1],
                        col2: r2[col2],
                        'Similitud': round(sim, 2)
                    }
                    if col1_id and col1_id in df1.columns:
                        match[col1_id] = r1[col1_id]
                    if col2_id and col2_id in df2.columns:
                        match[col2_id] = r2[col2_id]
                    matches.append(match)
    return pd.DataFrame(matches)

# Carga de archivos
st.subheader("Carga de archivos")
file1 = st.file_uploader("Sube primero el archivo de Wise", type=["xlsx", "xls"] )
file2 = st.file_uploader("Luego sube el archivo de BackOffice", type=["xlsx", "xls"] )

if file1 and file2:
    df1 = pd.read_excel(file1)
    df2 = pd.read_excel(file2)
    df1.columns = df1.columns.str.strip()
    df2.columns = df2.columns.str.strip()

    st.write(f"Archivo Wise: {df1.shape[0]} filas, {df1.shape[1]} columnas")
    st.write(f"Archivo BackOffice: {df2.shape[0]} filas, {df2.shape[1]} columnas")

    # Verificar columnas
    if col1 not in df1.columns or col2 not in df2.columns:
        st.error(
            f"Columnas no encontradas. Wise: {list(df1.columns)}, BackOffice: {list(df2.columns)}"
        )
    else:
        result = find_matches(df1, df2, threshold)
        st.subheader("Resultados de coincidencias")
        st.write(f"Se encontraron {len(result)} coincidencias.")
        st.dataframe(result)

        if not result.empty:
            towrite = BytesIO()
            with pd.ExcelWriter(towrite, engine="openpyxl") as writer:
                result.to_excel(writer, index=False)
            towrite.seek(0)
            st.download_button(
                label="Descargar resultados en Excel",
                data=towrite,
                file_name="coincidencias.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.info("No se encontraron coincidencias por encima del umbral especificado.")



