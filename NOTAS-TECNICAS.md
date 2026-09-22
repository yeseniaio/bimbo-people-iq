# Notas Tecnicas y Pendientes (uso interno)

> **Audiencia:** organizadores, coaches y perfiles tecnicos. Los participantes no necesitan leer
> esto para empezar — el README y las guias de cada track son suficientes. Aqui viven los
> detalles finos de los datos, las reglas de calculo y los pendientes con el cliente.

**Datos:** `cat_poc_sandbox_peopleai.hackaton_2026_people_ai` (9 tablas + 1 vista, **100% simuladas**).
Referencia completa de columnas, tipos, llaves y queries validados:
**[Track 3 - Databricks App/01. Catalogo-Tablas.md](Track%203%20-%20Databricks%20App/01.%20Catalogo-Tablas.md)**.
Estado de preparacion y acciones del evento: **[PRE-FLIGHT-CHECKLIST.md](PRE-FLIGHT-CHECKLIST.md)**.

---

## Reglas de datos (lo que hay que saber para no romper analisis)

| Regla | Detalle |
|-------|---------|
| **Clima limpio** | En `tbl_yl_sayit` filtra `scale = 'Likert'`; las preguntas de texto abierto tienen columnas desalineadas (comas embebidas en el CSV; ~1,328 de 80,558 filas) |
| **Talento con dato** | Excluye `'Without Data'` y `''` en Performance/Potential/Readiness (la mayoria no tiene evaluacion) |
| **Etiquetas inconsistentes** | Desempenio/potencial/readiness traen variantes de casing y formato entre anios y tablas: normaliza con `LOWER(TRIM())` antes de agrupar |
| **Snapshot reciente** | `personas` es mensual: filtra por `MAX(fecha_de_cierre)` para el estado actual. Evita inflar metricas al cruzar con tablas de 1 fila por persona |
| **Sin pais** | No hay dimension de pais; sitios/BU/organizacion estan codificados |
| **Columnas con caracteres** | Usa backticks para nombres con `/ ? ¿`, espacios, acentos y digitos iniciales |

### Llaves de union

- Entre tablas de persona: `ID_Usuario_sin_prefijos` (= `id_usuario_sin_prefijos` =
  `participant_s_unique_identifier`). **Cobertura parcial** (usa LEFT JOIN); dentro de `personas`
  para conteos usa `id_colaborador` (mas completo).
- `talent_grid` cruza con personas por `id_colaborador` (389/389).
- `tabulador_cedulas_salariales` cruza con personas por `nombre_categoria` (51/51, perfecto) →
  compa-ratio y equidad.
- `datos_de_mercado_sueldos` + `catalogo_puestos` se unen entre si por codigo de puesto, pero
  **NO se unen directo a `personas`** (personas no trae codigo y los titulos no empatan): son de
  **referencia** de mercado.

### Objetos con nota

- **Vista `vw_sayit_personas`:** el cliente la **va a eliminar** (hoy falla porque referencia
  `tbl_yr_sayit`, renombrada a `tbl_yl_sayit`). **No la uses**; si necesitas clima + personas,
  replica el cruce por llave compuesta (id + mes + anio) sobre `tbl_yl_sayit` (patron listo en el
  catalogo y en el notebook de Track 3).

---

## Pendientes / por confirmar

### ✅ Resuelto (21-sep-2026)
- **Compensacion (Esc. 3):** ya existen `datos_de_mercado_sueldos` (benchmark tipo Mercer),
  `tabulador_cedulas_salariales` (bandas internas, cruzan perfecto con personas) y
  `catalogo_puestos`. Habilita compa-ratio, equidad interna y comparacion contra mercado (referencia).
- **Talento / Sucesion:** `talent_grid` (389 personas, cruza por `id_colaborador`) + `dim_talent_grid`
  habilitan analisis de competencias, traits, drivers y risk factors.
- **Acceso y Genie:** participantes agregados al grupo `DnA - Databricks Hackaton Developers`;
  Genie probado por el cliente.

### 🔄 En curso (cliente) — confirmar antes del evento
- **`sayit.csv`:** el cliente esta corrigiendo la desalineacion de columnas (1,328/80,558 filas) y
  el comentario desactualizado de `tbl_yl_sayit` ("37.080 / 387" → real **80,558 / 1,075**).
  Interino: filtrar `scale='Likert'`.
- **Vista `vw_sayit_personas`:** el cliente la eliminara. Confirmar que ya quedo.

### 🗓️ Se resuelve el DIA del evento (on-demand)
- **Documentos Ask HR (Esc. 1) y Carpeta Azul (Esc. 5):** se aportaran/definiran durante el
  hackathon. El flujo esta listo (subir a volumen ➜ `ai_parse_document` ➜ Vector Search / Genie;
  Vector Search y embeddings ya operativos). Mientras tanto se trabaja la parte estructurada.
- **Grants de service principal (Track 3):** el organizador los crea on-demand cuando un equipo
  despliega una app (ver PRE-FLIGHT §F).

### ❓ Por confirmar con el cliente (no bloqueante)
- **Mercado/catalogo vs plantilla:** ?existe una tabla puente puesto↔codigo, o se compara solo via
  `nombre_categoria`/tabulador?
- **Geografia:** el Escenario 2 menciona "+39 paises"; el dato no tiene pais (7 sitios codificados,
  ~1 BU). ?Se agrega geografia o se acota al extracto?
- **Cobertura parcial:** Say It 1,075 personas, capacitacion 1,274, talent_grid 389 vs 2,059 en
  personas. ?Es esperado?
- **Etiquetas de talento:** ?existe un diccionario/mapeo oficial para normalizar
  desempenio/potencial/readiness?
- **9-box mayormente `Without Data`:** ?se cargara la evaluacion completa o se usa el subconjunto?

### Logistica del evento a completar
- Canal de soporte en tiempo real (Slack/Teams).
- Ubicacion de recursos de codigo (repo).
- Agenda por bloques del 23 y 24 de septiembre.
- Reglas de acceso al workspace y credenciales de los equipos.
- Premios y categorias finales.

---

*Repositorio adaptado de un hackathon previo de Grupo Bimbo (BimboBricks IQ). Datos 100% simulados.*
