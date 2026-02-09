from supabase import create_client
import streamlit as st
import supabase

def get_supabase_client():
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["anon_key"]
    return create_client(url, key)

def insertar_obra(data: dict):
    supabase = get_supabase_client()
    response = supabase.table("obra").insert(data).execute()
    return response

def obtener_obras():
    supabase = get_supabase_client()
    response = supabase.table("obra").select("*").order("id_obra", desc=True).execute()
    return response.data

