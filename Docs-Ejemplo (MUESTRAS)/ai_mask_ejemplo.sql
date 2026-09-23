-- =============================================================================
-- EJEMPLO (MUESTRA) de ai_mask — redacción de PII en columnas de TEXTO LIBRE
-- Esquema: cat_poc_sandbox_peopleai.hackaton_2026_people_ai
-- ai_mask(content STRING, labels ARRAY<STRING>) -> STRING con entidades -> [MASKED]
-- Requiere DBR 15.1+ / warehouse Pro o Serverless (no Classic).
--
-- ⚠️ ESTO ES SOLO UN EJEMPLO de UNA técnica (enmascarar texto libre con IA).
--    El dato del hackathon es 100% SIMULADO, así que NO necesitas enmascararlo.
--    Se incluye para DEMOSTRAR gobierno de dato sensible — un diferenciador en tu demo.
--
-- BUENAS PRÁCTICAS de gobierno en Unity Catalog (lo recomendado para dato real de People):
--   1) RBAC (control de acceso por rol): das permiso a GRUPOS/roles, no a personas. Ej.
--      GRANT SELECT ... TO `grupo_rrhh`. Cada quien ve solo lo que su rol permite.
--   2) COLUMN MASKING (máscara de columna): una columna sensible (salario, nombre) se
--      muestra enmascarada salvo a los roles autorizados — SIN duplicar la tabla.
--        ALTER TABLE t ALTER COLUMN salario_mensual SET MASK mi_mascara;
--   3) ROW FILTER (filtro de fila): cada usuario ve solo SUS filas (ej. su área/país).
--        ALTER TABLE t SET ROW FILTER mi_filtro ON (grupo_area_funcional);
-- ai_mask (abajo) es complementario: sirve para el TEXTO LIBRE (comentarios, notas) donde
-- la PII está incrustada en la frase y una máscara de columna no basta.
-- =============================================================================

-- 1) VISTA PREVIA — comparar original vs enmascarado (no cambia datos)
SELECT
  ID_Usuario_sin_prefijos,
  `2024_Future_scenario`                                                   AS original,
  ai_mask(`2024_Future_scenario`,
          array('person','email','phone','address','organization'))        AS enmascarado
FROM cat_poc_sandbox_peopleai.hackaton_2026_people_ai.tbl_wkly_talento
WHERE `2024_Future_scenario` IS NOT NULL
LIMIT 20;


-- 2) EJEMPLO EN EMAIL (datalake_personas) — enmascara la parte de persona/correo
SELECT
  id_colaborador,
  email_empresa                                       AS original,
  ai_mask(email_empresa, array('email','person'))     AS email_masked
FROM cat_poc_sandbox_peopleai.hackaton_2026_people_ai.tbl_mth_datalake_personas
WHERE email_empresa IS NOT NULL
LIMIT 20;


-- 3) BUENA PRÁCTICA — materializar UNA VEZ una copia enmascarada a Delta
--    (cada llamada es inferencia LLM: córrela una vez y consulta la tabla Delta)
CREATE OR REPLACE TABLE cat_poc_sandbox_peopleai.hackaton_2026_people_ai.talento_texto_masked AS
SELECT
  ID_Usuario_sin_prefijos,
  ai_mask(`Estudios_/_profesion`,                        array('person','organization','address'))            AS estudios_profesion_masked,
  ai_mask(`Especialidad`,                                array('person','organization'))                      AS especialidad_masked,
  ai_mask(`2024_Future_scenario`,                        array('person','email','phone','address','organization')) AS fut_2024_masked,
  ai_mask(`2024_Potential_leadership_strengths`,         array('person','organization'))                      AS strengths_2024_masked,
  ai_mask(`2024_Potential_leadership_opportunity_areas`, array('person','organization'))                      AS opps_2024_masked,
  ai_mask(`2025_Future_scenario`,                        array('person','email','phone','address','organization')) AS fut_2025_masked,
  ai_mask(`2025_Strengths`,                              array('person','organization'))                      AS strengths_2025_masked,
  ai_mask(`2025_Opportunities`,                          array('person','organization'))                      AS opps_2025_masked,
  ai_mask(`2026_Strengths`,                              array('person','organization'))                      AS strengths_2026_masked,
  ai_mask(`2026_Opportunities`,                          array('person','organization'))                      AS opps_2026_masked
FROM cat_poc_sandbox_peopleai.hackaton_2026_people_ai.tbl_wkly_talento;
