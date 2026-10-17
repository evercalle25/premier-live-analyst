import streamlit as st
import requests

st.set_page_config(page_title="Premier Live Analyst", layout="wide")

st.title("⚽ Premier Live Analyst")
st.caption("Diagnóstico de conexión con API-Football")

API_KEY = st.secrets["API_FOOTBALL_KEY"]
BASE = "https://v3.football.api-sports.io"
HEADERS = {"x-apisports-key": API_KEY}

st.subheader("1. Probando conexión con la API")

try:
    with st.spinner("Consultando partidos en vivo de la Premier League..."):
        r = requests.get(
            f"{BASE}/fixtures",
            headers=HEADERS,
            params={"live": "all", "league": 39, "season": 2026},
            timeout=15,
        )

    st.write(f"**Código de respuesta:** {r.status_code}")

    data = r.json()

    st.subheader("2. Respuesta de la API")
    st.write(data)

    response = data.get("response", [])
    st.subheader("3. Partidos en vivo encontrados")
    st.write(f"**Cantidad:** {len(response)}")

    if response:
        for f in response:
            home = f["teams"]["home"]["name"]
            away = f["teams"]["away"]["name"]
            hg = f["goals"]["home"]
            ag = f["goals"]["away"]
            minute = f["fixture"]["status"]["elapsed"]
            st.success(f"{home} {hg}-{ag} {away} | {minute}'")
    else:
        st.info("No hay partidos de la Premier League en vivo ahora.")

except Exception as e:
    st.error(f"Error: {e}")
