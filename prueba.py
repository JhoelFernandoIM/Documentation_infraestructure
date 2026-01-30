import streamlit as st
from src.db.supabase_client import get_supabase_client

supabase = get_supabase_client()
st.write("Cliente Supabase creado correctamente")
