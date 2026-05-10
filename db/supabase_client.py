import streamlit as st
from supabase import create_client, Client

@st.cache_resource
def init_connection():
    # Verificamos qué llaves están disponibles sin mostrar el valor por seguridad
    available_keys = list(st.secrets.keys())
    
    if "SUPABASE_URL" in st.secrets and "SUPABASE_KEY" in st.secrets:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        return create_client(url, key)
    else:
        st.error(f"Error: No se encuentran las claves. Claves detectadas: {available_keys}")
        return None
