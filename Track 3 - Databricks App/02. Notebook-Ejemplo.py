# Databricks notebook source
# MAGIC %md
# MAGIC # Notebook de Ejemplo - People AI Hackathon
# MAGIC
# MAGIC Queries SQL y PySpark listos para ejecutar sobre los datos de People / RRHH.
# MAGIC Todas las queries de este notebook fueron **validadas** contra el workspace.
# MAGIC
# MAGIC - **Catalogo:** `cat_poc_sandbox_peopleai`
# MAGIC - **Schema:** `hackaton_2026_people_ai`
# MAGIC - **Tablas:** `tbl_mth_datalake_personas`, `tbl_wkly_capacitacion`, `tbl_wkly_talento`, `tbl_yr_sayit`
# MAGIC
# MAGIC Organizado por escenario del hackathon. Referencia de columnas: `01. Catalogo-Tablas.md`.
# MAGIC
# MAGIC > **AVISO DE PRIVACIDAD:** `clean_name`, `email_empresa` y `salario_mensual` son
# MAGIC > confidenciales. Agrega o anonimiza en cualquier demo. No muestres PII individual.

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
sayit       = spark.table(f"{CATALOG}.{SCHEMA}.tbl_yr_sayit")

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
# MAGIC UNION ALL SELECT 'sayit', COUNT(*), COUNT(DISTINCT participant_s_unique_identifier) FROM tbl_yr_sayit;

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
# MAGIC FROM tbl_yr_sayit
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
  FROM tbl_yr_sayit
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
# MAGIC   FROM tbl_yr_sayit WHERE scale='Likert' GROUP BY 1
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
# MAGIC Categoria y plan estan **hasheados** (comparables entre si, no legibles). No hay
# MAGIC mercado externo (Mercer): esto es **benchmark interno** de equidad y dispersion.

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
# MAGIC   FROM tbl_yr_sayit WHERE scale='Likert' GROUP BY 1
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
# MAGIC Recuerda: agrega/anonimiza PII, filtra `scale='Likert'` en clima, y normaliza etiquetas.
