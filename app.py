import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
import time
from dotenv import load_dotenv
import os

# -------------------------------
# Load environment variables
# -------------------------------
load_dotenv()
API_KEY = os.getenv("OPENCAGE_API_KEY", "a3ba867cf14f49019607a169b604a98f")
BASE_URL = "https://api.opencagedata.com/geocode/v1/json"

# -------------------------------
# Streamlit Page Setup
# -------------------------------
st.set_page_config(page_title="OpenCage Geocoder", page_icon="🗺️", layout="wide")
st.title("🗺️ OpenCage Geocoder Web App")

# -------------------------------
# Geocoding Function
# -------------------------------
@st.cache_data(ttl=3600)
def geocode(query):
    """Unified geocoding function (forward or reverse)."""
    start_time = time.time()
    params = {"q": query, "key": API_KEY, "limit": 1, "no_annotations": 1}
    response = requests.get(BASE_URL, params=params)
    elapsed = round(time.time() - start_time, 3)
    data = response.json()

    if response.status_code == 200 and data.get("results"):
        res = data["results"][0]
        return {
            "lat": res["geometry"]["lat"],
            "lng": res["geometry"]["lng"],
            "formatted": res["formatted"],
            "time": elapsed
        }
    return None

# -------------------------------
# Initialize session state
# -------------------------------
if "result" not in st.session_state:
    st.session_state.result = None
if "mode" not in st.session_state:
    st.session_state.mode = "Forward (Address → Coordinates)"

# -------------------------------
# Basemap Definitions
# -------------------------------
BASEMAPS = {
    "OpenStreetMap": {
        "tiles": "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        "attr": "© OpenStreetMap contributors",
    },
    "CartoDB Positron": {
        "tiles": "https://cartodb-basemaps-a.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png",
        "attr": "© OpenStreetMap © CartoDB",
    },
    "CartoDB DarkMatter": {
        "tiles": "https://cartodb-basemaps-a.global.ssl.fastly.net/dark_all/{z}/{x}/{y}.png",
        "attr": "© OpenStreetMap © CartoDB",
    },
    "Stamen Terrain": {
        "tiles": "https://stamen-tiles.a.ssl.fastly.net/terrain/{z}/{x}/{y}.jpg",
        "attr": "Map tiles by Stamen Design, under CC BY 3.0 — Data © OpenStreetMap contributors",
    },
    "Stamen Toner": {
        "tiles": "https://stamen-tiles.a.ssl.fastly.net/toner/{z}/{x}/{y}.png",
        "attr": "Map tiles by Stamen Design, under CC BY 3.0 — Data © OpenStreetMap contributors",
    },
    "Stamen Watercolor": {
        "tiles": "https://stamen-tiles.a.ssl.fastly.net/watercolor/{z}/{x}/{y}.jpg",
        "attr": "Map tiles by Stamen Design, under CC BY 3.0 — Data © OpenStreetMap contributors",
    },
    "OpenTopoMap": {
        "tiles": "https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png",
        "attr": "© OpenTopoMap contributors under CC BY-SA",
    },
    "Esri Satellite (Hybrid)": {
        "tiles": "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        "attr": "Tiles © Esri — Source: Esri, Maxar, Earthstar Geographics, and the GIS User Community",
    },
}

# -------------------------------
# Sidebar
# -------------------------------
st.sidebar.header("🧭 Geocoding Options")

mode = st.sidebar.radio(
    "Select Geocoding Type:",
    ["Forward (Address → Coordinates)", "Reverse (Coordinates → Address)"],
    key="mode",
)

basemap_option = st.sidebar.selectbox(
    "🗺️ Choose basemap style:", list(BASEMAPS.keys()), index=0
)

st.sidebar.markdown("---")
st.sidebar.write("💡 Powered by [OpenCage Data](https://opencagedata.com/)")

# -------------------------------
# Helper Function: Map Generator
# -------------------------------
def create_map(lat, lng, popup_text, marker_color="blue"):
    """Create a Folium map based on basemap selection."""
    m = folium.Map(
        location=[lat, lng],
        zoom_start=13,
        tiles=None,  # we’ll add tiles manually for better control
    )

    # Handle Esri Hybrid separately (imagery + labels)
    if basemap_option == "Esri Satellite (Hybrid)":
        # Base Imagery
        folium.TileLayer(
            tiles=BASEMAPS["Esri Satellite (Hybrid)"]["tiles"],
            attr=BASEMAPS["Esri Satellite (Hybrid)"]["attr"],
            name="Esri Imagery",
        ).add_to(m)

        # Transparent Labels Overlay
        folium.TileLayer(
            tiles="https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}",
            attr="© Esri — Boundaries & Places",
            name="Labels",
            overlay=True,
            control=True,
        ).add_to(m)
    else:
        # Regular basemap
        tiles = BASEMAPS[basemap_option]
        folium.TileLayer(tiles=tiles["tiles"], attr=tiles["attr"], name=basemap_option).add_to(m)

    # Marker
    icon = folium.Icon(color=marker_color, icon="map-marker", prefix="fa")
    folium.Marker(
        [lat, lng],
        popup=popup_text,
        tooltip="📍 " + popup_text,
        icon=icon,
    ).add_to(m)

    # Layer control if multiple tile layers (like hybrid)
    folium.LayerControl().add_to(m)
    return m

# -------------------------------
# Forward Geocoding
# -------------------------------
if mode.startswith("Forward"):
    address = st.text_input("Enter Address or Place Name:")

    if st.button("🔍 Geocode"):
        if address.strip():
            with st.spinner("Fetching coordinates..."):
                st.session_state.result = geocode(address.strip())
        else:
            st.warning("Please enter a valid address.")

    if st.session_state.result:
        result = st.session_state.result
        st.success(f"✅ {result['formatted']}")
        st.info(f"📍 Latitude: {result['lat']} | Longitude: {result['lng']}")
        st.write(f"⏱️ Response Time: {result['time']} seconds")

        m = create_map(result["lat"], result["lng"], result["formatted"], "blue")
        st_folium(m, height=500, width=800)

# -------------------------------
# Reverse Geocoding
# -------------------------------
else:
    lat = st.number_input("Latitude:", format="%.6f", value=0.0)
    lng = st.number_input("Longitude:", format="%.6f", value=0.0)

    if st.button("🎯 Reverse Geocode"):
        query = f"{lat},{lng}"
        with st.spinner("Fetching address..."):
            st.session_state.result = geocode(query)

    if st.session_state.result:
        result = st.session_state.result
        st.success(f"✅ {result['formatted']}")
        st.info(f"📍 Latitude: {result['lat']} | Longitude: {result['lng']}")
        st.write(f"⏱️ Response Time: {result['time']} seconds")

        m = create_map(result["lat"], result["lng"], result["formatted"], "red")
        st_folium(m, height=500, width=800)

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.caption("🌍 Built by Brian Otieno | Powered by OpenCage, Esri, Stamen, & Streamlit")
