# Databricks notebook source
# MAGIC %md
# MAGIC # Tutorial: Crear una Databricks App - People AI Hackathon
# MAGIC
# MAGIC Como construir y desplegar una **Databricks App** en Python conectada a los datos de
# MAGIC People / RRHH. Cubrimos **3 frameworks** con el mismo ejemplo concreto:
# MAGIC un **Dashboard de Experiencia del Colaborador** (clima Say It + rotacion).
# MAGIC
# MAGIC | Framework | Perfil | Cuando usarlo |
# MAGIC |-----------|--------|---------------|
# MAGIC | **Streamlit** | Rapido | Prototipo en minutos, todo en Python, widgets |
# MAGIC | **Dash** | Profesional | Dashboards de produccion, interactividad rica |
# MAGIC | **Gradio** | Facil | Demos tipo chat / interfaces conversacionales (ideal para Genie) |
# MAGIC
# MAGIC - **Catalogo:** `cat_poc_sandbox_peopleai` / **Schema:** `hackaton_2026_people_ai`
# MAGIC - **Datos:** ver `01. Catalogo-Tablas.md`. Query base validada: % Favorable por dimension.
# MAGIC
# MAGIC > **AVISO:** el dato es **100% simulado** (ficticio, no real). La app corre con un
# MAGIC > **service principal** (no con tu usuario); da acceso a la tabla al SP en Unity Catalog.
# MAGIC > Buena practica: aunque `clean_name`/`email_empresa`/`salario_mensual` son simulados,
# MAGIC > consulta y muestra siempre datos **agregados** (en produccion serian PII real).

# COMMAND ----------

# MAGIC %md
# MAGIC ## 0. Conceptos clave (aplican a los 3 frameworks)
# MAGIC
# MAGIC 1. **Estructura minima de una app:**
# MAGIC    ```
# MAGIC    mi_app/
# MAGIC    |-- app.py            # la aplicacion
# MAGIC    |-- app.yaml          # comando de arranque + recursos (env valueFrom)
# MAGIC    |-- requirements.txt  # dependencias extra (los frameworks ya vienen preinstalados)
# MAGIC    ```
# MAGIC 2. **Autenticacion:** usa `Config()` del SDK. Nunca escribas tokens en el codigo.
# MAGIC    En la app se inyectan `DATABRICKS_CLIENT_ID` / `DATABRICKS_CLIENT_SECRET`.
# MAGIC 3. **Recursos:** el ID del SQL Warehouse llega por `app.yaml` con `valueFrom`
# MAGIC    (nunca hardcodeado). Agrega el warehouse como recurso de la app en la UI.
# MAGIC 4. **Puerto:** la app debe escuchar en `DATABRICKS_APP_PORT` (default 8000). Nunca 8080.
# MAGIC 5. **Runtime:** Python 3.11, 2 vCPU, 6 GB. Dash/Streamlit/Gradio ya estan preinstalados.
# MAGIC
# MAGIC **Conexion SQL comun a los 3 frameworks:**
# MAGIC ```python
# MAGIC import os
# MAGIC from databricks.sdk.core import Config
# MAGIC from databricks import sql
# MAGIC
# MAGIC cfg = Config()  # detecta credenciales del entorno de la app (service principal)
# MAGIC
# MAGIC def run_query(query: str):
# MAGIC     conn = sql.connect(
# MAGIC         server_hostname=cfg.host,
# MAGIC         http_path=f"/sql/1.0/warehouses/{os.getenv('DATABRICKS_WAREHOUSE_ID')}",
# MAGIC         credentials_provider=lambda: cfg.authenticate,
# MAGIC     )
# MAGIC     with conn.cursor() as cur:
# MAGIC         cur.execute(query)
# MAGIC         cols = [c[0] for c in cur.description]
# MAGIC         return [dict(zip(cols, row)) for row in cur.fetchall()]
# MAGIC ```

# COMMAND ----------

# MAGIC %md
# MAGIC ## Query de ejemplo (compartida por los 3 frameworks)
# MAGIC
# MAGIC Solo datos **agregados** (sin PII). Filtra `scale='Likert'`.
# MAGIC
# MAGIC > **Otras ideas de app (dato 21-sep-2026):** compa-ratio salarial cruzando
# MAGIC > `tbl_mth_datalake_personas` con `tabulador_cedulas_salariales` por `nombre_categoria`;
# MAGIC > tablero de competencias con `talent_grid` (+ `dim_talent_grid`); referencia de mercado
# MAGIC > con `datos_de_mercado_sueldos`. Ver queries validadas en `02. Notebook-Ejemplo.py`.
# MAGIC ```sql
# MAGIC SELECT dimention,
# MAGIC        ROUND(100.0 * SUM(CASE WHEN favorability='Favorable' THEN 1 END) / COUNT(*), 1) AS pct_favorable,
# MAGIC        COUNT(*) AS respuestas
# MAGIC FROM cat_poc_sandbox_peopleai.hackaton_2026_people_ai.tbl_yl_sayit
# MAGIC WHERE scale = 'Likert' AND dimention <> '' AND year = :anio
# MAGIC GROUP BY dimention
# MAGIC HAVING COUNT(*) >= 100
# MAGIC ORDER BY pct_favorable
# MAGIC ```

# COMMAND ----------

# MAGIC %md
# MAGIC # ============================================================
# MAGIC # OPCION A - STREAMLIT (rapido)
# MAGIC # ============================================================
# MAGIC
# MAGIC Crea 3 archivos en una carpeta `app_streamlit/`.

# COMMAND ----------

# MAGIC %md
# MAGIC ### `app_streamlit/app.yaml`
# MAGIC ```yaml
# MAGIC command: ["streamlit", "run", "app.py"]
# MAGIC env:
# MAGIC   - name: DATABRICKS_WAREHOUSE_ID
# MAGIC     valueFrom: sql-warehouse
# MAGIC ```
# MAGIC
# MAGIC ### `app_streamlit/requirements.txt`
# MAGIC ```
# MAGIC databricks-sdk
# MAGIC databricks-sql-connector
# MAGIC pandas
# MAGIC ```
# MAGIC (Streamlit ya viene preinstalado; no hace falta listarlo.)

# COMMAND ----------

# MAGIC %md
# MAGIC ### `app_streamlit/app.py`
# MAGIC ```python
# MAGIC import os
# MAGIC import streamlit as st
# MAGIC import pandas as pd
# MAGIC from databricks.sdk.core import Config
# MAGIC from databricks import sql
# MAGIC
# MAGIC st.set_page_config(page_title="Experiencia del Colaborador", layout="wide")  # primero!
# MAGIC
# MAGIC CATALOG, SCHEMA = "cat_poc_sandbox_peopleai", "hackaton_2026_people_ai"
# MAGIC
# MAGIC @st.cache_resource(ttl=300)
# MAGIC def get_connection():
# MAGIC     cfg = Config()
# MAGIC     return sql.connect(
# MAGIC         server_hostname=cfg.host,
# MAGIC         http_path=f"/sql/1.0/warehouses/{os.getenv('DATABRICKS_WAREHOUSE_ID')}",
# MAGIC         credentials_provider=lambda: cfg.authenticate,
# MAGIC     )
# MAGIC
# MAGIC @st.cache_data(ttl=300)
# MAGIC def clima_por_dimension(anio: int) -> pd.DataFrame:
# MAGIC     q = f"""
# MAGIC         SELECT dimention,
# MAGIC                ROUND(100.0*SUM(CASE WHEN favorability='Favorable' THEN 1 END)/COUNT(*),1) AS pct_favorable,
# MAGIC                COUNT(*) AS respuestas
# MAGIC         FROM {CATALOG}.{SCHEMA}.tbl_yl_sayit
# MAGIC         WHERE scale='Likert' AND dimention <> '' AND year = {anio}
# MAGIC         GROUP BY dimention HAVING COUNT(*) >= 100
# MAGIC         ORDER BY pct_favorable
# MAGIC     """
# MAGIC     with get_connection().cursor() as cur:
# MAGIC         cur.execute(q)
# MAGIC         cols = [c[0] for c in cur.description]
# MAGIC         return pd.DataFrame(cur.fetchall(), columns=cols)
# MAGIC
# MAGIC st.title("Experiencia del Colaborador - Clima Say It")
# MAGIC anio = st.selectbox("Anio", [2025, 2024])          # filtro
# MAGIC df = clima_por_dimension(anio)
# MAGIC
# MAGIC c1, c2 = st.columns(2)
# MAGIC c1.metric("Favorabilidad promedio", f"{df['pct_favorable'].mean():.1f}%")   # KPI
# MAGIC c2.metric("Dimensiones evaluadas", len(df))
# MAGIC
# MAGIC st.bar_chart(df.set_index("dimention")["pct_favorable"])                     # grafico
# MAGIC st.dataframe(df, use_container_width=True)
# MAGIC ```
# MAGIC
# MAGIC **Como agregar Genie:** incrusta un enlace al Genie Space del equipo, o llama a la
# MAGIC Conversations API del Space con el SDK para responder preguntas en lenguaje natural.

# COMMAND ----------

# MAGIC %md
# MAGIC # ============================================================
# MAGIC # OPCION B - DASH (profesional)
# MAGIC # ============================================================

# COMMAND ----------

# MAGIC %md
# MAGIC ### `app_dash/app.yaml`
# MAGIC ```yaml
# MAGIC command: ["python", "app.py"]
# MAGIC env:
# MAGIC   - name: DATABRICKS_WAREHOUSE_ID
# MAGIC     valueFrom: sql-warehouse
# MAGIC ```
# MAGIC
# MAGIC ### `app_dash/requirements.txt`
# MAGIC ```
# MAGIC databricks-sdk
# MAGIC databricks-sql-connector
# MAGIC dash-bootstrap-components
# MAGIC pandas
# MAGIC plotly
# MAGIC ```
# MAGIC (Dash ya viene preinstalado; `dash-bootstrap-components` no.)

# COMMAND ----------

# MAGIC %md
# MAGIC ### `app_dash/app.py`
# MAGIC ```python
# MAGIC import os
# MAGIC import dash
# MAGIC from dash import dcc, html, Input, Output
# MAGIC import dash_bootstrap_components as dbc
# MAGIC import pandas as pd
# MAGIC import plotly.express as px
# MAGIC from databricks.sdk.core import Config
# MAGIC from databricks import sql
# MAGIC
# MAGIC CATALOG, SCHEMA = "cat_poc_sandbox_peopleai", "hackaton_2026_people_ai"
# MAGIC cfg = Config()
# MAGIC
# MAGIC def clima_por_dimension(anio: int) -> pd.DataFrame:
# MAGIC     q = f"""
# MAGIC         SELECT dimention,
# MAGIC                ROUND(100.0*SUM(CASE WHEN favorability='Favorable' THEN 1 END)/COUNT(*),1) AS pct_favorable
# MAGIC         FROM {CATALOG}.{SCHEMA}.tbl_yl_sayit
# MAGIC         WHERE scale='Likert' AND dimention <> '' AND year = {anio}
# MAGIC         GROUP BY dimention HAVING COUNT(*) >= 100 ORDER BY pct_favorable
# MAGIC     """
# MAGIC     conn = sql.connect(
# MAGIC         server_hostname=cfg.host,
# MAGIC         http_path=f"/sql/1.0/warehouses/{os.getenv('DATABRICKS_WAREHOUSE_ID')}",
# MAGIC         credentials_provider=lambda: cfg.authenticate,
# MAGIC     )
# MAGIC     with conn.cursor() as cur:
# MAGIC         cur.execute(q)
# MAGIC         cols = [c[0] for c in cur.description]
# MAGIC         return pd.DataFrame(cur.fetchall(), columns=cols)
# MAGIC
# MAGIC app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], title="Experiencia del Colaborador")
# MAGIC
# MAGIC app.layout = dbc.Container([
# MAGIC     html.H2("Experiencia del Colaborador - Clima Say It", className="my-3"),
# MAGIC     dbc.Row([
# MAGIC         dbc.Col(dcc.Dropdown(id="anio", options=[2025, 2024], value=2025), width=3),
# MAGIC         dbc.Col(html.Div(id="kpi", className="fs-4 fw-bold")),
# MAGIC     ], className="mb-3"),
# MAGIC     dcc.Graph(id="grafico"),
# MAGIC ], fluid=True)
# MAGIC
# MAGIC @app.callback(Output("grafico", "figure"), Output("kpi", "children"), Input("anio", "value"))
# MAGIC def actualizar(anio):
# MAGIC     df = clima_por_dimension(anio)
# MAGIC     fig = px.bar(df, x="pct_favorable", y="dimention", orientation="h",
# MAGIC                  labels={"pct_favorable": "% Favorable", "dimention": "Dimension"})
# MAGIC     kpi = f"Favorabilidad promedio: {df['pct_favorable'].mean():.1f}%"
# MAGIC     return fig, kpi
# MAGIC
# MAGIC if __name__ == "__main__":
# MAGIC     app.run(host="0.0.0.0", port=int(os.environ.get("DATABRICKS_APP_PORT", 8000)))
# MAGIC ```

# COMMAND ----------

# MAGIC %md
# MAGIC # ============================================================
# MAGIC # OPCION C - GRADIO (facil / conversacional)
# MAGIC # ============================================================
# MAGIC
# MAGIC Ideal si tu escenario es conversacional (Ask HR): Gradio + Genie/Foundation Models.

# COMMAND ----------

# MAGIC %md
# MAGIC ### `app_gradio/app.yaml`
# MAGIC ```yaml
# MAGIC command: ["python", "app.py"]
# MAGIC env:
# MAGIC   - name: DATABRICKS_WAREHOUSE_ID
# MAGIC     valueFrom: sql-warehouse
# MAGIC ```
# MAGIC
# MAGIC ### `app_gradio/requirements.txt`
# MAGIC ```
# MAGIC databricks-sdk
# MAGIC databricks-sql-connector
# MAGIC pandas
# MAGIC ```

# COMMAND ----------

# MAGIC %md
# MAGIC ### `app_gradio/app.py`
# MAGIC ```python
# MAGIC import os
# MAGIC import gradio as gr
# MAGIC import pandas as pd
# MAGIC from databricks.sdk.core import Config
# MAGIC from databricks import sql
# MAGIC
# MAGIC CATALOG, SCHEMA = "cat_poc_sandbox_peopleai", "hackaton_2026_people_ai"
# MAGIC cfg = Config()
# MAGIC
# MAGIC def clima_por_dimension(anio: int) -> pd.DataFrame:
# MAGIC     q = f"""
# MAGIC         SELECT dimention,
# MAGIC                ROUND(100.0*SUM(CASE WHEN favorability='Favorable' THEN 1 END)/COUNT(*),1) AS pct_favorable
# MAGIC         FROM {CATALOG}.{SCHEMA}.tbl_yl_sayit
# MAGIC         WHERE scale='Likert' AND dimention <> '' AND year = {int(anio)}
# MAGIC         GROUP BY dimention HAVING COUNT(*) >= 100 ORDER BY pct_favorable
# MAGIC     """
# MAGIC     conn = sql.connect(
# MAGIC         server_hostname=cfg.host,
# MAGIC         http_path=f"/sql/1.0/warehouses/{os.getenv('DATABRICKS_WAREHOUSE_ID')}",
# MAGIC         credentials_provider=lambda: cfg.authenticate,
# MAGIC     )
# MAGIC     with conn.cursor() as cur:
# MAGIC         cur.execute(q)
# MAGIC         cols = [c[0] for c in cur.description]
# MAGIC         return pd.DataFrame(cur.fetchall(), columns=cols)
# MAGIC
# MAGIC def ver_clima(anio):
# MAGIC     df = clima_por_dimension(anio)
# MAGIC     kpi = f"Favorabilidad promedio {anio}: {df['pct_favorable'].mean():.1f}%"
# MAGIC     return kpi, df
# MAGIC
# MAGIC with gr.Blocks(title="Experiencia del Colaborador") as demo:
# MAGIC     gr.Markdown("## Experiencia del Colaborador - Clima Say It")
# MAGIC     anio = gr.Dropdown([2025, 2024], value=2025, label="Anio")     # filtro
# MAGIC     kpi = gr.Label(label="KPI")                                    # KPI
# MAGIC     tabla = gr.Dataframe(label="% Favorable por dimension")        # "grafico"/tabla
# MAGIC     anio.change(ver_clima, inputs=anio, outputs=[kpi, tabla])
# MAGIC     demo.load(ver_clima, inputs=anio, outputs=[kpi, tabla])
# MAGIC
# MAGIC port = int(os.environ.get("DATABRICKS_APP_PORT", 8000))
# MAGIC demo.launch(server_name="0.0.0.0", server_port=port)
# MAGIC ```
# MAGIC
# MAGIC **Como agregar Genie (chat):** cambia a `gr.ChatInterface` y en la funcion de respuesta
# MAGIC llama al Genie Space del equipo (Conversations API via `WorkspaceClient`) o a un
# MAGIC Foundation Model (cliente OpenAI-compatible del SDK). Ver skill `databricks-python-sdk`.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Despliegue (igual para los 3 frameworks)
# MAGIC
# MAGIC Desde tu terminal con el CLI de Databricks (perfil del workspace del hackathon):
# MAGIC
# MAGIC ```bash
# MAGIC # 1. Crear la app una sola vez
# MAGIC databricks apps create experiencia-colaborador --profile <PERFIL>
# MAGIC
# MAGIC # 2. Subir el codigo al workspace (carpeta con app.py, app.yaml, requirements.txt)
# MAGIC databricks sync ./app_streamlit /Workspace/Users/<tu_usuario>/experiencia-colaborador --profile <PERFIL>
# MAGIC
# MAGIC # 3. Desplegar
# MAGIC databricks apps deploy experiencia-colaborador \
# MAGIC   --source-code-path /Workspace/Users/<tu_usuario>/experiencia-colaborador --profile <PERFIL>
# MAGIC
# MAGIC # 4. Ver estado y logs
# MAGIC databricks apps get experiencia-colaborador --profile <PERFIL>
# MAGIC databricks apps logs experiencia-colaborador --profile <PERFIL>
# MAGIC ```
# MAGIC
# MAGIC **Antes de desplegar:**
# MAGIC 1. En la UI de la app, agrega el **SQL Warehouse** como recurso con la clave
# MAGIC    `sql-warehouse` (asi `valueFrom: sql-warehouse` resuelve el ID).
# MAGIC 2. Da al **service principal de la app** permiso `SELECT` sobre
# MAGIC    `cat_poc_sandbox_peopleai.hackaton_2026_people_ai` en Unity Catalog.
# MAGIC 3. Verifica que consultas **solo agregados** (nada de `clean_name`, `email_empresa`,
# MAGIC    `salario_mensual` a nivel individual).
# MAGIC
# MAGIC ## Problemas comunes
# MAGIC | Problema | Solucion |
# MAGIC |----------|----------|
# MAGIC | La app no arranca | Revisa `databricks apps logs`; verifica el `command` del `app.yaml` |
# MAGIC | Import error | Agrega el paquete a `requirements.txt` |
# MAGIC | Sin acceso a la tabla | Da SELECT al SP de la app en Unity Catalog |
# MAGIC | Conflicto de puerto | Escucha en `DATABRICKS_APP_PORT` (8000). Nunca 8080 |
# MAGIC | Dash sin estilos | Usa `dash-bootstrap-components` con `dbc.themes.BOOTSTRAP` |
