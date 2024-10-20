import streamlit as st
from streamlit_folium import folium_static
import folium
from folium.plugins import MarkerCluster
import pandas as pd

st.title("팅이네 미동여지도!")

df = pd.read_csv("maps.csv", encoding='ansi')

st.dataframe(df, height=200)

df[["lat","lon"]] = df[["위도","경도"]]

#m = folium.Map(location=[36.350412, 127.384548], zoom_start=13)
#36.229796, 127.763104
m = folium.Map(location=[36.229796, 127.763104], zoom_start=7)

marker_cluster = MarkerCluster().add_to(m)

for idx, row in df.iterrows():
    folium.Marker(
        location=[row["lat"], row["lon"]],
        popup=row["업소명"],
    ).add_to(marker_cluster)

folium_static(m)