# Databricks notebook source
# MAGIC %md
# MAGIC # Notebook de Ejemplo - People AI Hackathon
# MAGIC
# MAGIC Queries SQL y PySpark listos para ejecutar sobre los datos de People / RRHH.
# MAGIC Todas las queries de este notebook fueron **validadas** contra el workspace.
# MAGIC
# MAGIC - **Catalogo:** `cat_poc_sandbox_peopleai`
# MAGIC - **Schema:** `hackaton_2026_people_ai`
# MAGIC - **Personas/hechos:** `tbl_mth_datalake_personas`, `tbl_wkly_capacitacion`, `tbl_wkly_talento`, `tbl_yl_sayit` (80,558 filas / 1,075 personas), `talent_grid` (389)
# MAGIC - **Referencia:** `catalogo_puestos`, `datos_de_mercado_sueldos`, `tabulador_cedulas_salariales`, `dim_talent_grid`
# MAGIC
# MAGIC Organizado por escenario del hackathon. Referencia de columnas: `01. Catalogo-Tablas.md`.
# MAGIC Dato actualizado 21-sep-2026 (nuevas tablas de mercado, tabulador y talent grid).
# MAGIC
# MAGIC > ⚠️ **DATOS 100% SIMULADOS:** todo es ficticio (no real). `clean_name`, `email_empresa` y
# MAGIC > `salario_mensual` son nombres/correos/salarios simulados, no de personas reales. Aun asi,
# MAGIC > en demos muestra metricas agregadas en vez de filas individuales.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 0. Setup

# COMMAND ----------

CATALOG = "cat_poc_sandbox_peopleai"
SCHEMA  = "hackaton_2026_people_ai"

spark.sql(f"USE CATALOG {CATALOG}")
spark.sql(f"USE SCHEMA {SCHEMA}")

# Referencias rapidas a las tablas (PySpark)
personas    = spark.table(f"{CATALOG}.{SCHEMA}.tbl_mth_datalake_personas")
capacitacion= spark.table(f"{CATALOG}.{SCHEMA}.tbl_wkly_capacitacion")
talento     = spark.table(f"{CATALOG}.{SCHEMA}.tbl_wkly_talento")
sayit       = spark.table(f"{CATALOG}.{SCHEMA}.tbl_yl_sayit")
# Nuevas tablas (21-sep-2026)
talent_grid = spark.table(f"{CATALOG}.{SCHEMA}.talent_grid")
tabulador   = spark.table(f"{CATALOG}.{SCHEMA}.tabulador_cedulas_salariales")
mercado     = spark.table(f"{CATALOG}.{SCHEMA}.datos_de_mercado_sueldos")
catalogo    = spark.table(f"{CATALOG}.{SCHEMA}.catalogo_puestos")

print("Tablas cargadas. Filas:")
for name, df in [("personas", personas), ("capacitacion", capacitacion),
                 ("talento", talento), ("sayit", sayit)]:
    print(f"  {name:14s} {df.count():>8,}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Perfil rapido de cada tabla
# MAGIC
# MAGIC Reglas clave del dato:
# MAGIC - `personas` es **mensual**: filtra por `MAX(fecha_de_cierre)` para el estado actual.
# MAGIC - `sayit` limpio: filtra `scale = 'Likert'` (el texto abierto trae columnas desalineadas).
# MAGIC - Talento/9-box: excluye `'Without Data'` y `''`.
# MAGIC - Llave entre tablas: `ID_Usuario_sin_prefijos` (traslape parcial, usa LEFT JOIN).

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Conteos y cobertura por tabla
# MAGIC SELECT 'personas' AS tabla, COUNT(*) AS filas, COUNT(DISTINCT id_colaborador) AS personas
# MAGIC FROM tbl_mth_datalake_personas
# MAGIC UNION ALL SELECT 'capacitacion', COUNT(*), COUNT(DISTINCT id_usuario_sin_prefijos) FROM tbl_wkly_capacitacion
# MAGIC UNION ALL SELECT 'talento', COUNT(*), COUNT(DISTINCT ID_Usuario_sin_prefijos) FROM tbl_wkly_talento
# MAGIC UNION ALL SELECT 'sayit', COUNT(*), COUNT(DISTINCT participant_s_unique_identifier) FROM tbl_yl_sayit;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Rango temporal del snapshot mensual de personas
# MAGIC SELECT MIN(fecha_de_cierre) AS desde, MAX(fecha_de_cierre) AS hasta,
# MAGIC        COUNT(DISTINCT fecha_de_cierre) AS meses
# MAGIC FROM tbl_mth_datalake_personas;

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Escenario 2 - Analitica de Experiencia del Colaborador (clima Say It)
# MAGIC
# MAGIC Metrica principal: **% Favorable** por dimension y anio (solo `scale = 'Likert'`).

# COMMAND ----------

# MAGIC %sql
# MAGIC -- % Favorable por dimension y anio
# MAGIC SELECT year,
# MAGIC        dimention,
# MAGIC        ROUND(100.0 * SUM(CASE WHEN favorability = 'Favorable' THEN 1 END) / COUNT(*), 1) AS pct_favorable,
# MAGIC        COUNT(*) AS respuestas
# MAGIC FROM tbl_yl_sayit
# MAGIC WHERE scale = 'Likert' AND dimention <> ''
# MAGIC GROUP BY year, dimention
# MAGIC ORDER BY year, pct_favorable;

# COMMAND ----------

# MAGIC %md
# MAGIC ### Visualizacion: dimensiones con menor favorabilidad (2025)
# MAGIC Usa `display()` para graficar con la UI del notebook, o matplotlib para exportar.

# COMMAND ----------

df_clima = spark.sql("""
  SELECT dimention,
         ROUND(100.0 * SUM(CASE WHEN favorability = 'Favorable' THEN 1 END) / COUNT(*), 1) AS pct_favorable
  FROM tbl_yl_sayit
  WHERE scale = 'Likert' AND dimention <> '' AND year = 2025
  GROUP BY dimention
  HAVING COUNT(*) >= 100
  ORDER BY pct_favorable
""")
display(df_clima)   # En la UI: elige grafico de barras (dimention vs pct_favorable)

# COMMAND ----------

# Grafico con matplotlib (util para exportar imagen o incrustar en una app)
import matplotlib.pyplot as plt

pdf = df_clima.toPandas().head(12)
fig, ax = plt.subplots(figsize=(9, 5))
ax.barh(pdf["dimention"], pdf["pct_favorable"], color="#1B3139")
ax.set_xlabel("% Favorable")
ax.set_title("Dimensiones de clima con menor favorabilidad (2025)")
ax.invert_yaxis()
plt.tight_layout()
plt.show()

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Cruce clima + rotacion: areas con baja favorabilidad y bajas voluntarias
# MAGIC WITH clima AS (
# MAGIC   SELECT participant_s_unique_identifier AS id,
# MAGIC          ROUND(100.0 * SUM(CASE WHEN favorability='Favorable' THEN 1 END)/COUNT(*), 1) AS pct_fav
# MAGIC   FROM tbl_yl_sayit WHERE scale='Likert' GROUP BY 1
# MAGIC ),
# MAGIC pers AS (
# MAGIC   SELECT ID_Usuario_sin_prefijos AS id, grupo_area_funcional,
# MAGIC          MAX(CASE WHEN tipo_de_baja='VOLUNTARIA' THEN 1 ELSE 0 END) AS baja_voluntaria
# MAGIC   FROM tbl_mth_datalake_personas GROUP BY 1,2
# MAGIC )
# MAGIC SELECT p.grupo_area_funcional,
# MAGIC        ROUND(AVG(c.pct_fav),1) AS clima_prom,
# MAGIC        ROUND(100.0*AVG(p.baja_voluntaria),1) AS pct_baja_voluntaria,
# MAGIC        COUNT(*) AS personas
# MAGIC FROM pers p JOIN clima c ON p.id = c.id
# MAGIC GROUP BY 1 ORDER BY clima_prom;

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Rotacion / Attrition (personas)

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Bajas por generacion, tipo y motivo agrupado
# MAGIC SELECT generacion, tipo_de_baja, Agrupador_Motivo_Baja, COUNT(*) AS bajas
# MAGIC FROM tbl_mth_datalake_personas
# MAGIC WHERE fecha_de_baja IS NOT NULL
# MAGIC GROUP BY 1,2,3
# MAGIC ORDER BY bajas DESC;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Headcount activo por area funcional (ultimo cierre mensual)
# MAGIC WITH ult AS (SELECT MAX(fecha_de_cierre) AS m FROM tbl_mth_datalake_personas)
# MAGIC SELECT grupo_area_funcional, COUNT(*) AS headcount
# MAGIC FROM tbl_mth_datalake_personas, ult
# MAGIC WHERE fecha_de_cierre = ult.m AND active = 1
# MAGIC GROUP BY grupo_area_funcional
# MAGIC ORDER BY headcount DESC;

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Escenario 3 - Compensacion y categorias
# MAGIC
# MAGIC Categoria y plan estan **hasheados** (comparables entre si, no legibles).
# MAGIC Ahora hay 3 tablas de compensacion (21-sep-2026):
# MAGIC - `tabulador_cedulas_salariales` (bandas internas): **cruza perfecto con personas** por `nombre_categoria` -> compa-ratio.
# MAGIC - `datos_de_mercado_sueldos` (benchmark tipo Mercer): referencia de mercado por puesto. **No** se une directo a personas.
# MAGIC - `catalogo_puestos`: catalogo de puestos (se une a mercado por codigo, no a personas).

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Rango salarial por nivel y categoria (solo grupos con volumen suficiente)
# MAGIC SELECT nivel, nombre_categoria,
# MAGIC        COUNT(*) AS n,
# MAGIC        ROUND(AVG(salario_mensual)) AS media,
# MAGIC        ROUND(MIN(salario_mensual)) AS minimo,
# MAGIC        ROUND(MAX(salario_mensual)) AS maximo,
# MAGIC        ROUND(MAX(salario_mensual) - MIN(salario_mensual)) AS rango
# MAGIC FROM tbl_mth_datalake_personas
# MAGIC WHERE salario_mensual IS NOT NULL
# MAGIC GROUP BY 1,2
# MAGIC HAVING COUNT(*) >= 20
# MAGIC ORDER BY media DESC
# MAGIC LIMIT 20;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Deteccion de dispersion salarial atipica dentro de una misma categoria
# MAGIC SELECT nombre_categoria,
# MAGIC        COUNT(*) AS n,
# MAGIC        ROUND(AVG(salario_mensual)) AS media,
# MAGIC        ROUND(STDDEV(salario_mensual)) AS desviacion,
# MAGIC        ROUND(STDDEV(salario_mensual) / NULLIF(AVG(salario_mensual),0), 2) AS coef_variacion
# MAGIC FROM tbl_mth_datalake_personas
# MAGIC WHERE salario_mensual IS NOT NULL
# MAGIC GROUP BY 1
# MAGIC HAVING COUNT(*) >= 30
# MAGIC ORDER BY coef_variacion DESC
# MAGIC LIMIT 15;

# COMMAND ----------

# MAGIC %md
# MAGIC ### Compa-ratio: salario vs banda interna (tabulador)
# MAGIC `personas.nombre_categoria` = `tabulador.nombre_categoria` (51/51 match). compa-ratio > 1 =
# MAGIC por arriba del punto medio de la banda; < 1 = por abajo.

# COMMAND ----------

# MAGIC %sql
# MAGIC WITH ult AS (SELECT MAX(fecha_de_cierre) AS m FROM tbl_mth_datalake_personas)
# MAGIC SELECT t.nivel_gb, p.nombre_categoria,
# MAGIC        COUNT(*) AS n,
# MAGIC        ROUND(AVG(p.salario_mensual)) AS salario_prom,
# MAGIC        t.minimo, t.valor_medio, t.maximo,
# MAGIC        ROUND(AVG(p.salario_mensual) / t.valor_medio, 2) AS compa_ratio
# MAGIC FROM tbl_mth_datalake_personas p
# MAGIC JOIN ult ON p.fecha_de_cierre = ult.m
# MAGIC JOIN tabulador_cedulas_salariales t ON p.nombre_categoria = t.nombre_categoria
# MAGIC WHERE p.active = 1 AND p.salario_mensual IS NOT NULL
# MAGIC GROUP BY t.nivel_gb, p.nombre_categoria, t.minimo, t.valor_medio, t.maximo
# MAGIC HAVING COUNT(*) >= 15
# MAGIC ORDER BY compa_ratio DESC
# MAGIC LIMIT 15;

# COMMAND ----------

# MAGIC %md
# MAGIC ### Referencia de mercado (datos_de_mercado_sueldos)
# MAGIC Sueldo base de mercado por nivel de carrera. **Ojo:** es referencia; no se une directo a
# MAGIC `personas` (no hay codigo de puesto compartido; ver Pendientes del README). Nombres de
# MAGIC columna con espacios/acentos -> backticks.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT `Nivel de carrera` AS nivel_carrera,
# MAGIC        ROUND(AVG(`Sueldo Base (12 Meses) Promedio_OP`)) AS sueldo_base_mercado,
# MAGIC        ROUND(AVG(`Compensación en Efectivo Total (Target) Promedio_OP`)) AS comp_efectivo_total,
# MAGIC        COUNT(*) AS puestos
# MAGIC FROM datos_de_mercado_sueldos
# MAGIC GROUP BY `Nivel de carrera`
# MAGIC ORDER BY sueldo_base_mercado DESC;

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Escenario 4 - Gestion de Talento (9-box)
# MAGIC
# MAGIC Las etiquetas de desempenio/potencial son **inconsistentes** entre anios y sistemas
# MAGIC (`Great Work`, `Surpasses`, `3`, `3.5`...). Normaliza con UPPER/TRIM antes de agrupar.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Distribucion 9-box (desempenio x potencial), normalizando etiquetas
# MAGIC SELECT UPPER(TRIM(Performance_Evaluation)) AS desempenio,
# MAGIC        UPPER(TRIM(Potential_Evaluation))   AS potencial,
# MAGIC        COUNT(*) AS n
# MAGIC FROM tbl_mth_datalake_personas
# MAGIC WHERE Performance_Evaluation NOT IN ('Without Data','')
# MAGIC   AND Potential_Evaluation  NOT IN ('Without Data','')
# MAGIC GROUP BY 1,2
# MAGIC ORDER BY n DESC
# MAGIC LIMIT 20;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Cobertura de evaluacion de talento por area (que tanto se ha evaluado)
# MAGIC WITH ult AS (SELECT MAX(fecha_de_cierre) AS m FROM tbl_mth_datalake_personas)
# MAGIC SELECT grupo_area_funcional,
# MAGIC        COUNT(*) AS personas,
# MAGIC        SUM(CASE WHEN Performance_Evaluation NOT IN ('Without Data','') THEN 1 ELSE 0 END) AS con_evaluacion,
# MAGIC        ROUND(100.0 * SUM(CASE WHEN Performance_Evaluation NOT IN ('Without Data','') THEN 1 ELSE 0 END)/COUNT(*),1) AS pct_cobertura
# MAGIC FROM tbl_mth_datalake_personas, ult
# MAGIC WHERE fecha_de_cierre = ult.m AND active = 1
# MAGIC GROUP BY grupo_area_funcional
# MAGIC ORDER BY personas DESC;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Brecha de desarrollo: horas de capacitacion por nivel de potencial
# MAGIC WITH cap AS (
# MAGIC   SELECT id_usuario_sin_prefijos AS id, SUM(horas_de_capacitacion) AS horas
# MAGIC   FROM tbl_wkly_capacitacion
# MAGIC   WHERE estado_de_la_capacitacion IN ('Approved','Completed')
# MAGIC   GROUP BY 1
# MAGIC )
# MAGIC SELECT t.`2026_Potential_Map` AS potencial,
# MAGIC        COUNT(*) AS personas,
# MAGIC        ROUND(AVG(COALESCE(cap.horas,0)),1) AS horas_prom
# MAGIC FROM tbl_wkly_talento t
# MAGIC LEFT JOIN cap ON t.ID_Usuario_sin_prefijos = cap.id
# MAGIC WHERE t.`2026_Potential_Map` NOT IN ('Without Data','')
# MAGIC GROUP BY 1
# MAGIC ORDER BY personas DESC;

# COMMAND ----------

# MAGIC %md
# MAGIC ### Talent Grid: competencias y percentiles (assessment)
# MAGIC `talent_grid` (389 personas) cruza con `personas` por `id_colaborador`. Cada atributo tiene
# MAGIC `_sten` (1-10), `_percentil` (0-100) y `_escala`. Usa `dim_talent_grid` para etiquetar columnas.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Diccionario: que significan las columnas del talent grid (por grupo)
# MAGIC SELECT grupo_competencia, COUNT(*) AS columnas
# MAGIC FROM dim_talent_grid
# MAGIC GROUP BY grupo_competencia
# MAGIC ORDER BY columnas DESC;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Competencias de liderazgo mas altas (percentil) cruzando con perfil de persona
# MAGIC WITH ult AS (SELECT MAX(fecha_de_cierre) AS m FROM tbl_mth_datalake_personas),
# MAGIC persona AS (
# MAGIC   SELECT id_colaborador, nivel, grupo_area_funcional
# MAGIC   FROM tbl_mth_datalake_personas p JOIN ult ON p.fecha_de_cierre = ult.m
# MAGIC )
# MAGIC SELECT pe.grupo_area_funcional,
# MAGIC        ROUND(AVG(g.strategic_mindset_percentil)) AS estrategia,
# MAGIC        ROUND(AVG(g.drives_results_percentil))    AS resultados,
# MAGIC        ROUND(AVG(g.decision_quality_percentil))  AS decision,
# MAGIC        ROUND(AVG(g.builds_effective_teams_percentil)) AS equipos,
# MAGIC        COUNT(*) AS personas
# MAGIC FROM talent_grid g
# MAGIC JOIN persona pe ON g.id_colaborador = pe.id_colaborador
# MAGIC GROUP BY pe.grupo_area_funcional
# MAGIC HAVING COUNT(*) >= 5
# MAGIC ORDER BY estrategia DESC;

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6. Escenario 5 - Sucesion basada en datos
# MAGIC
# MAGIC **Ojo con el casing:** `Readiness` existe en dos tablas con formato distinto:
# MAGIC - `personas.Readiness` = `Ready Now (0-1 Year)`
# MAGIC - `talento.2026_Readiness` = `Ready now (0 - 1 years)`
# MAGIC
# MAGIC Usa comparacion **case-insensitive** (`LOWER(TRIM(...)) LIKE 'ready now%'`).

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Pipeline de sucesion: candidatos "Ready Now" (ultimo snapshot) por area y nivel
# MAGIC WITH latest AS (
# MAGIC   SELECT id_colaborador, ID_Usuario_sin_prefijos, nivel, grupo_area_funcional,
# MAGIC          antiguedad, Readiness, Potential_Evaluation
# MAGIC   FROM tbl_mth_datalake_personas
# MAGIC   QUALIFY ROW_NUMBER() OVER (PARTITION BY id_colaborador ORDER BY fecha_de_cierre DESC) = 1
# MAGIC )
# MAGIC SELECT grupo_area_funcional, nivel,
# MAGIC        COUNT(*) AS candidatos,
# MAGIC        ROUND(AVG(antiguedad),1) AS antiguedad_prom
# MAGIC FROM latest
# MAGIC WHERE LOWER(TRIM(Readiness)) LIKE 'ready now%'
# MAGIC GROUP BY 1,2
# MAGIC ORDER BY candidatos DESC;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Ranking explicable de sucesores: score simple y transparente (no caja negra)
# MAGIC WITH latest AS (
# MAGIC   SELECT id_colaborador, ID_Usuario_sin_prefijos, nivel, grupo_area_funcional,
# MAGIC          antiguedad, Readiness, Potential_Evaluation, Performance_Evaluation
# MAGIC   FROM tbl_mth_datalake_personas
# MAGIC   QUALIFY ROW_NUMBER() OVER (PARTITION BY id_colaborador ORDER BY fecha_de_cierre DESC) = 1
# MAGIC )
# MAGIC SELECT id_colaborador, grupo_area_funcional, nivel, antiguedad,
# MAGIC        Readiness, Potential_Evaluation,
# MAGIC        (CASE WHEN LOWER(TRIM(Readiness)) LIKE 'ready now%' THEN 3
# MAGIC              WHEN LOWER(TRIM(Readiness)) LIKE 'mid%'       THEN 2
# MAGIC              WHEN LOWER(TRIM(Readiness)) LIKE 'well%'      THEN 2
# MAGIC              WHEN LOWER(TRIM(Readiness)) LIKE 'long%'      THEN 1 ELSE 0 END
# MAGIC         + CASE WHEN UPPER(Potential_Evaluation) LIKE '%ESSENTIAL%' THEN 2
# MAGIC                WHEN UPPER(Potential_Evaluation) LIKE '%PROMISING%' THEN 1 ELSE 0 END
# MAGIC        ) AS score_sucesion
# MAGIC FROM latest
# MAGIC WHERE Readiness NOT IN ('Without Data','')
# MAGIC ORDER BY score_sucesion DESC, antiguedad DESC
# MAGIC LIMIT 25;

# COMMAND ----------

# MAGIC %md
# MAGIC ## 7. Cruce integral (las tres tablas por la llave)
# MAGIC
# MAGIC Perfil + talento + clima en una sola vista. Base = `personas`, `LEFT JOIN` al resto.

# COMMAND ----------

# MAGIC %sql
# MAGIC WITH latest AS (
# MAGIC   SELECT id_colaborador, ID_Usuario_sin_prefijos, nivel, grupo_area_funcional, antiguedad
# MAGIC   FROM tbl_mth_datalake_personas
# MAGIC   QUALIFY ROW_NUMBER() OVER (PARTITION BY id_colaborador ORDER BY fecha_de_cierre DESC) = 1
# MAGIC ),
# MAGIC clima AS (
# MAGIC   SELECT participant_s_unique_identifier AS id,
# MAGIC          ROUND(100.0*SUM(CASE WHEN favorability='Favorable' THEN 1 END)/COUNT(*),1) AS pct_favorable
# MAGIC   FROM tbl_yl_sayit WHERE scale='Likert' GROUP BY 1
# MAGIC )
# MAGIC SELECT l.grupo_area_funcional, l.nivel,
# MAGIC        COUNT(*) AS personas,
# MAGIC        ROUND(AVG(l.antiguedad),1) AS antiguedad_prom,
# MAGIC        ROUND(AVG(c.pct_favorable),1) AS clima_prom,
# MAGIC        SUM(CASE WHEN t.`2026_Potential_Map` NOT IN ('Without Data','') THEN 1 ELSE 0 END) AS con_potencial
# MAGIC FROM latest l
# MAGIC LEFT JOIN tbl_wkly_talento t ON l.ID_Usuario_sin_prefijos = t.ID_Usuario_sin_prefijos
# MAGIC LEFT JOIN clima c            ON l.ID_Usuario_sin_prefijos = c.id
# MAGIC GROUP BY 1,2
# MAGIC ORDER BY personas DESC;

# COMMAND ----------

# MAGIC %md
# MAGIC ## 7b. Vista `vw_sayit_personas` (clima + personas) - HOY ESTA ROTA
# MAGIC
# MAGIC Existe una vista `vw_sayit_personas` que cruza clima + personas por una **llave compuesta**
# MAGIC (`id + mes + anio`), acotando personas a los cortes **Sep-2024** y **Jun-2025**. Pero su
# MAGIC definicion aun referencia `tbl_yr_sayit`, que fue **renombrada a `tbl_yl_sayit`**, asi que
# MAGIC `SELECT * FROM vw_sayit_personas` **falla**. Mientras se corrige la vista, replica el cruce:

# COMMAND ----------

# MAGIC %sql
# MAGIC WITH p AS (
# MAGIC   SELECT *,
# MAGIC          CONCAT(id_colaborador, '_',
# MAGIC                 CASE MONTH(fecha_de_cierre) WHEN 9 THEN 'septiembre' WHEN 6 THEN 'junio' END, '_',
# MAGIC                 CAST(YEAR(fecha_de_cierre) AS STRING)) AS llave_compuesta
# MAGIC   FROM tbl_mth_datalake_personas
# MAGIC   WHERE (YEAR(fecha_de_cierre)=2024 AND MONTH(fecha_de_cierre)=9)
# MAGIC      OR (YEAR(fecha_de_cierre)=2025 AND MONTH(fecha_de_cierre)=6)
# MAGIC ),
# MAGIC s AS (
# MAGIC   SELECT *,
# MAGIC          CONCAT(participant_s_unique_identifier, '_',
# MAGIC                 CASE WHEN year=2024 THEN 'septiembre' ELSE 'junio' END, '_',
# MAGIC                 CAST(year AS STRING)) AS llave_compuesta
# MAGIC   FROM tbl_yl_sayit
# MAGIC )
# MAGIC SELECT s.year, s.dimention, s.favorability,
# MAGIC        p.nivel, p.grupo_area_funcional, p.generacion
# MAGIC FROM s
# MAGIC LEFT JOIN p ON s.llave_compuesta = p.llave_compuesta
# MAGIC WHERE s.scale = 'Likert'
# MAGIC LIMIT 50;

# COMMAND ----------

# MAGIC %md
# MAGIC ## 8. PySpark equivalente (para quien prefiere DataFrames)

# COMMAND ----------

from pyspark.sql import functions as F, Window

# Clima por dimension (2025) con PySpark
clima_2025 = (
    sayit
    .filter((F.col("scale") == "Likert") & (F.col("dimention") != "") & (F.col("year") == 2025))
    .groupBy("dimention")
    .agg(
        (F.round(100.0 * F.sum(F.when(F.col("favorability") == "Favorable", 1).otherwise(0)) / F.count("*"), 1)).alias("pct_favorable"),
        F.count("*").alias("respuestas"),
    )
    .filter(F.col("respuestas") >= 100)
    .orderBy("pct_favorable")
)
display(clima_2025)

# COMMAND ----------

# Ultimo snapshot por persona con PySpark (window)
w = Window.partitionBy("id_colaborador").orderBy(F.col("fecha_de_cierre").desc())
personas_ult = (
    personas
    .withColumn("rn", F.row_number().over(w))
    .filter(F.col("rn") == 1)
    .drop("rn")
)
print("Personas (ultimo snapshot):", personas_ult.count())
display(
    personas_ult.filter(F.col("active") == 1)
    .groupBy("grupo_area_funcional").count()
    .orderBy(F.col("count").desc())
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Siguiente paso
# MAGIC
# MAGIC - **Track 1 (Genie):** usa estas queries como ejemplos en el Knowledge Store del Space.
# MAGIC - **Track 2 (AI/BI):** convierte estas queries en datasets del dashboard.
# MAGIC - **Track 3 (App):** ver `03. Tutorial-Databricks-App.py` para exponerlas en una app.
# MAGIC
# MAGIC Recuerda: el dato es simulado (presenta agregados, no filas individuales), filtra `scale='Likert'` en clima, y normaliza etiquetas.
