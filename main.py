import streamlit as st
import pandas as pd
from st_aggrid import AgGrid
import plotly.express as px
import folium
from streamlit_folium import st_folium
import time
import warnings
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

def main():
    st.set_page_config(page_title="Big Data", page_icon="🏠", layout="wide")
    warnings.filterwarnings("ignore")
    hide_streamlit_style = """
           <style>
            div.block-container{padding-top:2rem;}
               div[data-testid="stToolbar"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
           </style>
           """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    st.header("🏡 Vorhersage der Mietpreise in Deutschland")
    st.subheader("📊 Business Analytics: Big Data")
    df_data = pd.read_csv(r"https://streamlitbigdata.s3.us-west-1.amazonaws.com/tabelle.csv", dtype={"Postleitzahl": "string"})
    durchschnittsmieten = pd.read_csv(r"https://streamlitbigdata.s3.us-west-1.amazonaws.com/Durchschnittsmieten.csv")
    df_hist = pd.read_csv(r"https://streamlitbigdata.s3.us-west-1.amazonaws.com/Histogram.csv")
    st.write("""
                  - Die folgende Anwendung liefert eine **Prognose des Mietpreises** (warm) für ein Wohnobjekt anhand der Eingaben des Nutzers.
                  - Unsere Datenbank entält über **178.000 Wohnobjekte** und wird stetig erweitert.
                  - Neben der Prognose können auch verschiedene **Diagramme** und eine **interaktive Karte** aus dem Datensatz betrachtet werden
                   """)
    st.info("Für Premiumuser wird exakt aufgezeigt, wie Sie den Wert Ihres Wohnobjektes verbessern können. Für Mehr Informationen kontaktieren Sie uns unter: bigdataaalen@gmail.com\n\n"\
            '✅ Zum Starten der Prognose bitte Parameter an der Sidebar auswählen und den "Parameter bestätigen" Button drücken.')
    st.write("⚠️ bei Zugriff mit mobilen Geräten ist der Filter für die Prognose standardmäßig ausgeblendet und lässt sich mit dem Pfeil oben links wieder einblenden")
    try:
        st.write("Auszug aus unserer Datenbank:")
        AgGrid(df_data,height=400)
        st.markdown("""----""")
    except:
        st.write("Bitte Seite neu laden oder einen Slider an der Sidebar nocheinmal betätigen, um Datentabelle neu zu laden.")
    #st.markdown("""----""")
    st.markdown("##### Die Prognostizierte monatliche Miete für das Wohnobjekt beträgt: ")
    #with st.form(key='Form1'):
    with st.sidebar.form(key='Form1'):
         wohnraum = st.sidebar.slider("Wohnfläche in m²:", 8, 500, 80, 1)
         raeume = st.sidebar.slider("Anzahl Räume:", 1.0, 12.0, 4.0, 0.5)
         baujahr = st.sidebar.slider("Baujahr angeben:", 1500, 2020, 1980, 1)
         bundesland = st.sidebar.selectbox("Bundesland auswählen:",
                                          options=["Baden-Württemberg","Bayern","Berlin","Brandenburg","Bremen","Hamburg",
                                                   "Hessen","Mecklenburg-Vorpommern","Niedersachsen","Nordrhein-Westfalen",
                                                   "Rheinland-Pfalz","Saarland","Sachsen","Sachsen-Anhalt","Schleswig-Holstein","Thüringen"]
                                              , index=0)
        kueche = st.radio("Küche vorhanden", ("Ja", "Nein"), index=0)
        karte = st.radio("Karte anzeigen",("Ja", "Nein"),index=1)
        submitted1 = st.form_submit_button(label="Parameter bestätigen")
    if submitted1:
        try:
            with st.spinner("Bitte warten Prognose wird erstellt"):
                machine_learning = pd.read_feather(r"https://streamlitbigdata.s3.us-west-1.amazonaws.com/ml_streamlit.feather")
                x = machine_learning[["livingSpaceRange", "livingSpace", "noRoomsRange", "noRooms","yearConstructedRange", "yearConstructed","hasKitchen", "regio1_numeric"]]
                y = machine_learning["totalRent"]
                X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)
                ml_model = RandomForestRegressor(random_state = 42,n_estimators=50,max_depth=10)
                ml_model.fit(X_train, y_train)
                livingSpace=wohnraum
                if wohnraum >=machine_learning["livingSpace"].quantile((1/7)):
                    livingSpaceRange =1
                elif wohnraum >= machine_learning["livingSpace"].quantile((2/7)):
                    livingSpaceRange = 2
                elif wohnraum >= machine_learning["livingSpace"].quantile((3/7)):
                    livingSpaceRange = 3
                elif wohnraum >= machine_learning["livingSpace"].quantile((4/7)):
                    livingSpaceRange = 4
                elif wohnraum >= machine_learning["livingSpace"].quantile((5/7)):
                    livingSpaceRange = 5
                elif wohnraum >= machine_learning["livingSpace"].quantile((6/7)):
                    livingSpaceRange = 6
                else:
                    livingSpaceRange = 7
                noRooms=raeume
                if raeume >=machine_learning["noRooms"].quantile((1/5)):
                    noRoomsRange=1
                elif raeume >=machine_learning["noRooms"].quantile((2/5)):
                    noRoomsRange=2
                elif raeume >=machine_learning["noRooms"].quantile((3/5)):
                    noRoomsRange=3
                elif raeume >=machine_learning["noRooms"].quantile((4/5)):
                    noRoomsRange=4
                else:
                    noRoomsRange = 5
                yearConstructed=baujahr
                if baujahr >= machine_learning["yearConstructed"].quantile((1/9)):
                    yearConstructedRange = 1
                elif baujahr >= machine_learning["yearConstructed"].quantile((2/9)):
                    yearConstructedRange = 2
                elif baujahr >= machine_learning["yearConstructed"].quantile((3/9)):
                    yearConstructedRange = 3
                elif baujahr >= machine_learning["yearConstructed"].quantile((4/9)):
                    yearConstructedRange = 4
                elif baujahr >= machine_learning["yearConstructed"].quantile((5/9)):
                    yearConstructedRange = 5
                elif baujahr >= machine_learning["yearConstructed"].quantile((6/9)):
                    yearConstructedRange = 6
                elif baujahr >= machine_learning["yearConstructed"].quantile((7/9)):
                    yearConstructedRange = 7
                elif baujahr >= machine_learning["yearConstructed"].quantile((8/9)):
                    yearConstructedRange = 8
                else:
                    yearConstructedRange = 9
                if kueche=="Ja":
                    hasKitchen=True
                else:
                    hasKitchen = False
                if bundesland=="Baden-Württemberg":
                    regio1_numeric = 12
                elif bundesland=="Bayern":
                    regio1_numeric = 14
                elif bundesland=="Berlin":
                    regio1_numeric = 15
                elif bundesland=="Brandenburg":
                    regio1_numeric = 5
                elif bundesland=="Bremen":
                    regio1_numeric = 9
                elif bundesland=="Hamburg":
                    regio1_numeric = 16
                elif bundesland=="Hessen":
                    regio1_numeric = 13
                elif bundesland=="Mecklenburg-Vorpommern":
                    regio1_numeric = 3
                elif bundesland=="Niedersachsen":
                    regio1_numeric = 7
                elif bundesland=="Nordrhein-Westfalen":
                    regio1_numeric = 8
                elif bundesland=="Rheinland-Pfalz":
                    regio1_numeric = 11
                elif bundesland=="Saarland":
                    regio1_numeric = 6
                elif bundesland=="Sachsen":
                    regio1_numeric = 4
                elif bundesland=="Sachsen-Anhalt":
                    regio1_numeric = 1
                elif bundesland=="Schleswig-Holstein":
                    regio1_numeric = 10
                elif bundesland=="Thüringen":
                    regio1_numeric = 2
                price_prediction =ml_model.predict([[livingSpaceRange,livingSpace,noRoomsRange,noRooms,yearConstructedRange,yearConstructed,hasKitchen,regio1_numeric]])
                x = int(price_prediction)
                x_unter = int(x * 0.98)
                x_ober = int(x * 1.02)
                st.success("#### 📈 zwischen " + str(x_unter) + " und " + str(x_ober) + " €/Monat")
        except:
            st.write("Berechnung nicht möglich, bitte Seite neu laden und andere Parameter wählen.")
    st.markdown("""----""")
    try:
        config = {"displayModeBar": False}
        fig1 = px.bar(durchschnittsmieten, x="Bundesland", y="Durchschnittsmiete")
        fig1.update_layout(title={"text":"Durchschnittsmieten (warm) je Bundesland","y":0.92})
        st.plotly_chart(fig1, use_container_width=True, config=config)
        fig2 = px.bar(durchschnittsmieten, x="Bundesland", y="Durchschnittsmiete pro qm",color="Durchschnittsmiete pro qm")
        fig2.update_layout(title={"text":"Durchschnittsmieten (kalt) je qm","y":0.92},barmode="stack", xaxis={"categoryorder": "total ascending"},coloraxis_colorbar=dict(title="Miete/qm"))
        st.plotly_chart(fig2, use_container_width=True, config=config)
        bundesland=[]
        option = st.selectbox("Bundesland auswählen für Boxplot bzw. Histogramm", (
        "Baden-Württemberg", "Bayern", "Berlin", "Brandenburg", "Bremen", "Hamburg", "Hessen", "Mecklenburg-Vorpommern",
        "Niedersachsen", "Nordrhein-Westfalen", "Rheinland-Pfalz", "Saarland", "Sachsen", "Sachsen-Anhalt",
        "Schleswig-Holstein", "Thüringen"))
        bundesland.append(option)
        #st.write(bundesland)
        df_hist = df_hist[df_hist["regio1"].isin(bundesland)]
        fig_col1, fig_col2 = st.columns(2)
        with fig_col1:
            fig3 = px.box(df_hist, x="totalRent", title="Boxplot der Miete (warm)",labels={"totalRent":"Miete (warm)"})
            fig3.update_layout(title={"y": 0.83, "x": 0.5},xaxis_tickformat=".")
            st.plotly_chart(fig3, use_container_width=True, config=config)
        with fig_col2:
            fig4 = px.histogram(df_hist, x="totalRent", nbins=50, title="Histogramm der Miete (warm)",
                     labels={"totalRent":"Miete (warm)"}).update_layout(yaxis_title="Anzahl")
            fig4.update_layout(title={"y": 0.83, "x": 0.5},xaxis_tickformat=".")
            st.plotly_chart(fig4, use_container_width=True, config=config)
    except:
        st.write("Diagramme konnten nicht vollständig geladen werden, bitte Seite neu laden.")
    st.write(" ⚠️ **Beim Anzeigen der Deutschlandkarte und einer erneuten Prognose bitte Seite mit der Taste F5 neu laden. Das Generieren der Karte erfordert zudem etwas Zeit.**")
    if submitted1:
        if karte == "Ja":
            try:
                with st.spinner("Bitte warten Karte wird geladen"):
                    map_folium = pd.read_csv(r"https://streamlitbigdata.s3.us-west-1.amazonaws.com/geo_immo.csv")
                    map_all = folium.Map(location=[map_folium.lat.mean(), map_folium.long.mean()], zoom_start=6)
                    for index, location_info in map_folium.iterrows():
                        folium.Marker([location_info["lat"], location_info["long"]], popup=location_info["popup"]).add_to(map_all)
                    st.write("Zum zoomen Scrollrad der Maus benutzen oder Plus/Minus Button auf der Karte")
                    st_folium(map_all, width=700, height=700)
                    st.success("Karte geladen!")
                time.sleep(99999)
            except:
                st.write("Karte konnte nicht geladen werden")

if __name__ == "__main__":
  main()
