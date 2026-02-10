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

#insetar interesados
def insertar_remitente(data: dict):
    supabase = get_supabase_client()
    response = supabase.table("remitente").insert(data).execute()
    return response.data[0]   # devuelve el registro insertado

def insertar_personal_obra(data: dict):
    supabase = get_supabase_client()
    return supabase.table("personal_obra").insert(data).execute()

def insertar_area_municipal(data: dict):
    supabase = get_supabase_client()
    return supabase.table("area_municipal").insert(data).execute()

def insertar_entidad_externa(data: dict):
    supabase = get_supabase_client()
    return supabase.table("entidad_externa").insert(data).execute()

def obtener_obras_combo():
    supabase = get_supabase_client()
    res = supabase.table("obra").select("id_obra,nombre_obra").execute()
    return res.data

def obtener_interesados():
    supabase = get_supabase_client()
    response = supabase.table("remitente").select("*").order("id_interesado", desc=True).execute()
    return response.data


#INTERESADOS

def obtener_interesados_full():
    supabase = get_supabase_client()
    return supabase.table("remitente").select("*").execute().data

def obtener_personal_obra_full():
    supabase = get_supabase_client()
    return supabase.table("personal_obra") \
        .select("id_personal_obra, rol_obra, remitente(nombre_rs, telefono), obra(nombre_obra)") \
        .execute().data

def obtener_area_municipal_full():
    supabase = get_supabase_client()
    return supabase.table("area_municipal") \
        .select("id_area, nombre_area, nivel, remitente(nombre_rs, telefono)") \
        .execute().data

def obtener_externos_full():
    supabase = get_supabase_client()
    return supabase.table("entidad_externa") \
        .select("id_entidad, tipo_entidad, remitente(nombre_rs, telefono)") \
        .execute().data
