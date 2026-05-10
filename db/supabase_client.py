import streamlit as st
from supabase import create_client, Client

@st.cache_resource
def init_connection():
    # Esto nos dirá en la consola de 'Manage app' si las claves existen
    if "SUPABASE_URL" in st.secrets and "SUPABASE_KEY" in st.secrets:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        return create_client(url, key)
    else:
        st.error("Error: Las claves SUPABASE_URL o SUPABASE_KEY no se encuentran en los Secrets de Streamlit.")
        return None
