
# Sistema experto para diagnosticar fallos de red

## Descripcion

Sistema experto basado en reglas que permite identificar posibles fallos
de conectividad en una red de computadores y mostrar recomendaciones.

## Tecnologias

- Python
- Streamlit
- JSON

## Instalacion

1. Instalar Python.
2. Abrir una terminal en la carpeta del proyecto.
3. Crear y activar un entorno virtual.
4. Instalar las dependencias:

   ```bash
   python -m pip install -r requirements.txt
   ```

## Ejecucion

Ejecutar:

```bash
python -m streamlit run main.py
```

La interfaz se abrira en el navegador.

## Estructura

- `main.py`: interfaz de usuario.
- `motor_inferencia.py`: motor de inferencia y resolucion de conflictos.
- `conocimiento.json`: base de conocimiento con 18 reglas.
- `requirements.txt`: dependencias del proyecto.
- `casos/`: casos de prueba en formato JSON.
- `documentos/`: documentacion tecnica.

## Uso

El usuario puede seleccionar hechos iniciales o cargar un caso JSON.
El sistema aplica las reglas, muestra las inferencias y presenta
las recomendaciones que correspondan.

Tambien permite cargar una base de conocimiento JSON externa.

## Integrantes

- [Esteban Sanchez Buitrago (Toy solito >:)]



