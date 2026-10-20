
import json
#from pathlib import Path

import streamlit as st
from motor_inferencia import motor_inferencia


# NUEVO: titulo y descripcion de la aplicacion.
st.set_page_config(page_title="Sistema experto de redes", page_icon="🌐")
st.title("Sistema experto para diagnosticar fallos de red")
st.write(
    "Selecciona los sintomas observados o carga un caso "
    "para obtener un diagnostico y recomendaciones."
)

# NUEVO: hechos que el usuario puede introducir.
sintomas = {
    "cable_desconectado": "El cable de red esta desconectado",
    "wifi_sin_senal": "El equipo no detecta la senal WiFi",
    "router_encendido": "El router esta encendido",
    "no_obtiene_ip": "El equipo no obtiene una direccion IP",
    "ip_duplicada": "Se detecta una direccion IP duplicada",
    "ping_ip_funciona": "Se puede hacer ping a una direccion IP",
    "no_resuelve_dominio": "No se puede resolver un nombre de dominio",
    "sin_acceso_internet": "El equipo no tiene acceso a Internet",
    "ping_gateway_falla": "Falla el ping a la puerta de enlace",
    "red_lenta": "La red funciona lentamente",
    "muchos_dispositivos": "Hay muchos dispositivos conectados"
}

# NUEVO: recomendaciones asociadas a las conclusiones.
recomendaciones = {
    "recomendar_revisar_cable":
        "Comprueba que el cable este bien conectado en ambos extremos. "
        "Si es necesario, prueba otro cable y otro puerto.",
    "recomendar_revisar_wifi":
        "Comprueba que el WiFi este activado, acercate al router "
        "y verifica la configuracion del punto de acceso.",
    "recomendar_verificar_dhcp":
        "Verifica que el servicio DHCP este activo y que el rango "
        "de direcciones IP tenga direcciones disponibles.",
    "recomendar_cambiar_ip":
        "Revisa la configuracion IP y renueva la direccion del equipo. "
        "Si la red lo permite, utiliza DHCP para evitar duplicados.",
    "recomendar_verificar_dns":
        "Revisa la configuracion del servidor DNS y prueba una consulta "
        "de dominio desde el equipo.",
    "recomendar_revisar_gateway":
        "Comprueba la direccion de la puerta de enlace, la conexion "
        "con el router y su configuracion.",
    "recomendar_limitar_trafico":
        "Identifica los equipos que consumen mas ancho de banda y "
        "limita o distribuye el trafico si es necesario."
}


def cargar_json(ruta):
    # NUEVO: leer y convertir un archivo JSON.
    with open(ruta, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


# NUEVO: permitir cargar una base de conocimiento externa.
archivo_conocimiento = st.file_uploader(
    "Cargar base de conocimiento JSON (opcional)",
    type=["json"]
)

try:
    if archivo_conocimiento is not None:
        conocimiento = json.load(archivo_conocimiento)
    else:
        conocimiento = cargar_json("conocimiento.json")

    reglas = conocimiento["reglas"]

    if not isinstance(reglas, list):
        raise ValueError("La propiedad 'reglas' debe ser una lista.")

except (OSError, json.JSONDecodeError, KeyError, ValueError) as error:
    st.error(f"No se pudo cargar la base de conocimiento: {error}")
    st.stop()


# NUEVO: permitir cargar hechos iniciales desde un caso externo.
archivo_caso = st.file_uploader(
    "Cargar caso inicial JSON (opcional)",
    type=["json"],
    key="caso"
)

hechos_del_caso = []

if archivo_caso is not None:
    try:
        datos_caso = json.load(archivo_caso)
        hechos_del_caso = datos_caso["hechos_iniciales"]

        if not isinstance(hechos_del_caso, list):
            raise ValueError("'hechos_iniciales' debe ser una lista.")

        hechos_desconocidos = [
            hecho for hecho in hechos_del_caso
            if hecho not in sintomas
        ]

        if hechos_desconocidos:
            st.warning(
                "El caso contiene hechos que no estan en la lista "
                f"de sintomas: {hechos_desconocidos}"
            )

    except (json.JSONDecodeError, KeyError, ValueError) as error:
        st.error(f"No se pudo cargar el caso: {error}")
        st.stop()


# NUEVO: seleccionar los sintomas observados.
st.subheader("1. Hechos iniciales")
seleccionados = st.multiselect(
    "Selecciona los sintomas o condiciones conocidos:",
    options=list(sintomas.keys()),
    default=[
        hecho for hecho in hechos_del_caso
        if hecho in sintomas
    ],
    format_func=lambda hecho: sintomas[hecho]
)

# NUEVO: ejecutar el motor cuando se pulsa el boton.
if st.button("Analizar red", type="primary"):
    resultado = motor_inferencia(seleccionados, reglas)

    st.subheader("2. Resultado del razonamiento")

    if resultado["historial"]:
        st.success(
            f"Se ejecutaron {len(resultado['historial'])} reglas."
        )

        for numero, paso in enumerate(resultado["historial"], start=1):
            with st.expander(
                f"Paso {numero}: {paso['regla']} - {paso['nombre']}"
            ):
                st.write("Antecedentes:", paso["antecedentes"])
                st.write("Consecuentes:", paso["consecuentes"])
                st.write("Prioridad:", paso["prioridad"])
                st.write("Hechos nuevos:", paso["nuevos_hechos"])
    else:
        st.info(
            "No se activo ninguna regla. Prueba seleccionando "
            "otros sintomas o revisa la base de conocimiento."
        )

    st.subheader("3. Hechos deducidos")
    if resultado["hechos_deducidos"]:
        st.write(resultado["hechos_deducidos"])
    else:
        st.write("No se dedujeron hechos nuevos.")

    st.subheader("4. Recomendaciones del sistema experto")
    recomendaciones_encontradas = [
        recomendaciones[hecho]
        for hecho in resultado["hechos_finales"]
        if hecho in recomendaciones
    ]

    if recomendaciones_encontradas:
        for recomendacion in recomendaciones_encontradas:
            st.info(recomendacion)
    else:
        st.warning(
            "No se obtuvo una recomendacion. Se necesitan mas hechos "
            "o reglas que permitan llegar a una conclusion."
        )

    with st.expander("Ver memoria de trabajo final"):
        st.write(resultado["hechos_finales"])
