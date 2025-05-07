# 🧠 App de Coincidencias de Nombres entre Wise y BackOffice

Esta aplicación desarrollada en Streamlit permite identificar coincidencias entre nombres de personas que aparecen en dos fuentes diferentes: **Wise** y **BackOffice**. Utiliza un algoritmo de similitud para detectar coincidencias aunque los nombres estén escritos con variaciones o en distinto orden.

---

## 🚀 ¿Cómo funciona?

1. **Carga de archivos**  
   - El usuario debe subir primero el archivo generado por **Wise**.
   - Luego, el archivo de **BackOffice**.
   
2. **Selección de columnas**  
   Se pueden configurar las columnas que contienen los nombres y los identificadores únicos de cada archivo.

3. **Algoritmo de comparación**  
   - Los nombres son limpiados y normalizados (se eliminan tildes, puntuaciones y se ordenan las palabras).
   - Se aplica un algoritmo de similitud (`SequenceMatcher`) con un umbral configurable (por defecto 0.80).

4. **Visualización y descarga**  
   Se muestran los resultados en pantalla y se puede descargar un archivo Excel con todas las coincidencias encontradas.

---

## 🛠 Tecnologías utilizadas

- [Python](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [pandas](https://pandas.pydata.org/)
- [openpyxl](https://openpyxl.readthedocs.io/)
- [Pillow](https://pillow.readthedocs.io/)

---

## 📦 Instalación local

```bash
git clone https://github.com/tu_usuario/streamlit-coincidencias.git
cd streamlit-coincidencias
pip install -r requirements.txt
streamlit run app_coincidencias.py