A simple, elegant **Streamlit web app** for forward and reverse geocoding using the [OpenCage API](https://opencagedata.com/), with interactive **Leaflet maps** powered by Folium.

---

# OpenCage Geocoder (Streamlit)

Lightweight Streamlit web app for forward and reverse geocoding using the OpenCage Data API. It displays results on an interactive Folium/Leaflet map.

## Features
- Forward geocoding (address/place → lat,lng)
- Reverse geocoding (lat,lng → formatted address)
- Interactive map using Folium + streamlit-folium
- Response time reporting and simple caching (Streamlit cache)
- API key configurable via a `.env` file

## Quickstart (Windows)

1. Create and activate a virtual environment (PowerShell recommended):

```powershell
# create venv
python -m venv venv
# activate in PowerShell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

If you prefer Git Bash / MSYS, use forward slashes to activate:

```bash
source venv/Scripts/activate
```

2. Install dependencies

```powershell
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and set your OpenCage API key (get a free key at https://opencagedata.com/):

```
OPENCAGE_API_KEY=your_api_key_here
```

4. Run the app with Streamlit

```powershell
streamlit run app.py
```

The app will open in your browser (usually at http://localhost:8501).

## Troubleshooting
- "Unable to copy ... venvlauncher.exe" when creating a venv: remove any partial `venv` directory, disable/whitelist the project folder in antivirus (Windows Defender), run PowerShell as Administrator, or try `py -3 -m venv --copies venv` or `python -m pip install --user virtualenv` then `python -m virtualenv venv`.
- Activation fails in Git Bash when using backslashes — use forward slashes: `source venv/Scripts/activate`.
- If Streamlit can't find packages, ensure you activated the venv and `pip install -r requirements.txt` completed without errors.

## Files of interest
- `app.py` — Streamlit application
- `requirements.txt` — Python dependencies

## License & Repo
This repository: https://github.com/Brianoysters/geocode

Built by Brian Otieno

A simple, elegant **Streamlit web app** for forward and reverse geocoding using the [OpenCage API](https://opencagedata.com/), with interactive **Leaflet maps** powered by Folium.

---

## ��� Features
- Forward Geocoding (Address → Coordinates)
- Reverse Geocoding (Coordinates → Address)
- Interactive Leaflet Map
- Response Time Display
- Local & Cloud Caching
- .env-based API Key Management
- One-click Deployment to Streamlit Cloud

---

## ��� Installation

1. Clone or download the project:
   ```bash
   git clone https://github.com/yourusername/opencage-geocoder-app.git
   cd opencage-geocoder-app

