# Importación de las bibliotecas necesarias
import pandas as pd
import plotly.express as px
import folium
import streamlit as st
from folium.plugins import HeatMap
from streamlit_folium import folium_static

# Configuración inicial de la página Streamlit
st.set_page_config(page_title="UFO Sightings Analysis", layout="wide")
# Título de la página Streamlit
st.title("UFO Sightings Analysis")
# Descripción en la página Streamlit
st.markdown("""Welcome to the UFO sightings analysis app.
Here you can explore data on UFO sightings around the world.
""")

# Definición de la clase UFOAnalysis
class UFOAnalysis:
    # Constructor de la clase
    def __init__(self):
        # Carga de datos desde un archivo CSV
        self.df = pd.read_csv("ufo-sightings-transformed.csv", encoding="latin-1")
        # Conversión de la duración de los encuentros de segundos a minutos
        self.df['length_of_encounter_seconds'] = pd.to_numeric(self.df['length_of_encounter_seconds'])
        self.df['length_of_encounter_seconds'] /= 60

    # Método principal para correr la aplicación
    def run(self):
        # Creación de un campo de entrada de texto para buscar por país
        pais_seleccionado = st.text_input("Enter a country to search for UFO sightings", "")
        # Análisis basado en el país seleccionado o análisis global
        if pais_seleccionado:
            self.analyze_country(pais_seleccionado)
        else:
            self.global_analysis()

    # Análisis específico por país
    def analyze_country(self, country):
        # Filtrado de los datos por país
        df_filtrado = self.df[self.df['Country'].str.contains(country, case=False, na=False)]
        # Llamadas a métodos para mostrar gráficos y mapas para el país seleccionado
        self.display_charts(df_filtrado, country)
        self.display_maps(df_filtrado)
        self.display_3d_scatter(df_filtrado)

    # Análisis a nivel global
    def global_analysis(self):
        # Llamadas a métodos para mostrar gráficos y mapas a nivel global
        self.display_charts(self.df, "Global")
        self.display_maps(self.df)
        self.display_3d_scatter(self.df)

    # Mostrar gráficos estadísticos
    def display_charts(self, df, title):
        # Creación y visualización de un histograma de formas de OVNIs
        fig = px.histogram(df, x='UFO_shape', title=f'Distribution of UFO Shapes in {title}')
        st.plotly_chart(fig)
        # Creación y visualización de un gráfico de líneas de tendencias de avistamientos a lo largo de los años
        fig = px.line(df.groupby('Year').size().reset_index(name='counts'), x='Year', y='counts', title=f'UFO Sightings Trends over Years in {title}')
        st.plotly_chart(fig)
        # Gráfico de barras para la duración promedio de encuentros por forma de OVNI (si no es un análisis global)
        if title != "Global":
            duracion_promedio = df.groupby('UFO_shape')['length_of_encounter_seconds'].mean().reset_index(name='average_duration')
            fig = px.bar(duracion_promedio, x='UFO_shape', y='average_duration', title=f'Average Encounter Duration by UFO Shape in {title}')
            st.plotly_chart(fig)

    # Mostrar mapas con marcadores y mapas de calor
    def display_maps(self, df):
        # Creación y visualización de un mapa con marcadores de avistamientos
        st.write("Map of UFO Sightings")
        mapa = self.create_map(df)
        folium_static(mapa)
        # Creación y visualización de un mapa de calor de avistamientos
        st.write("Heatmap of UFO Sightings")
        heatmap = self.create_heatmap(df)
        folium_static(heatmap)

    # Creación de un mapa de Folium con marcadores
    def create_map(self, df):
        mapa = folium.Map(location=[20, 0], zoom_start=2)
        # Tomar una muestra de los datos si el conjunto es muy grande
        sample_size = min(100, len(df))
        df_sample = df.sample(sample_size)
        # Agregar marcadores al mapa
        for lat, lon, description in zip(df_sample['latitude'], df_sample['longitude'], df_sample['Description']):
            if pd.notnull(lat) and pd.notnull(lon):
                folium.Marker(location=[lat, lon], popup=f"{description}").add_to(mapa)
        return mapa

    # Creación de un mapa de calor de Folium
    def create_heatmap(self, df):
        mapa_calor = folium.Map(location=[20, 0], zoom_start=2)
        # Preparación de datos para el mapa de calor
        heat_data = [[row['latitude'], row['longitude']] for index, row in df.iterrows() if pd.notnull(row['latitude']) and pd.notnull(row['longitude'])]
        HeatMap(heat_data).add_to(mapa_calor)
        return mapa_calor
    
    # Creación de un gráfico de dispersión 3D
    def display_3d_scatter(self, df):
        # Creación y visualización de un gráfico de dispersión 3D
        fig = px.scatter_3d(df, x='latitude', y='longitude', z='Year', color='UFO_shape', title='3D Scatter Plot of UFO Sightings')
        st.plotly_chart(fig)

# Ejecución de la aplicación
if __name__ == "__main__":2
    ufo_analysis = UFOAnalysis()
    ufo_analysis.run()
