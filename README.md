# Innovation Sprint People + IA - Hackathon

**Grupo Bimbo People AI Hackathon**

Hackathon de Grupo Bimbo enfocado en Databricks, GenAI, Genie, AI/BI y Databricks Apps,
aplicado a los datos de **People / Recursos Humanos**.

**Fecha:** 23-24 de septiembre de 2026
**Plataforma:** Databricks Workspace (Sandbox) `https://adb-709692038187649.9.azuredatabricks.net`
**Datos:** People / RRHH - **100% SIMULADOS (ficticios)** - Personas, Capacitacion, Talento y Clima "Say It"
**Objetivo del dia:** Demo funcional + presentacion (~30 min de armado, 3 min de pitch)

> ⚠️ **DATOS 100% SIMULADOS.** Todo el dato de este hackathon es **ficticio/simulado** — **NO es
> informacion real de Grupo Bimbo**. Los nombres (`clean_name`) **no son reales**, los correos
> (`email_empresa`) son **simulados** y los salarios (`salario_mensual`) estan **completamente
> simulados**. Categorias, planes, sitios y organizaciones vienen codificados. Nada representa
> a personas, correos ni remuneraciones reales.

---

## Elige tu Track

Tres tracks. Cada equipo elige **uno**. Los tres resuelven los mismos escenarios de negocio.

| Track | Para quien | Que construyes | Dificultad | Habilidades |
|-------|-----------|----------------|------------|-------------|
| **Track 1 - Genie Space** | Negocio, analistas | Un espacio conversacional que responde preguntas en lenguaje natural | Facil | Conocimiento del negocio. SQL opcional |
| **Track 2 - AI/BI Dashboard** | Negocio, analistas | Un dashboard AI/BI interactivo con Q&A en lenguaje natural | Facil | Conocimiento del negocio. SQL basico |
| **Track 3 - Databricks App** | Perfil tecnico | Una app desplegada en Databricks Apps (dashboard, herramienta operativa o app de analisis) | Medio | Python (basico-intermedio), SQL, front-end basico |

- **Track 1** entrega: Genie Space funcional con 5+ preguntas de ejemplo, instrucciones configuradas y demo en vivo.
- **Track 2** entrega: AI/BI Dashboard publicado, conectado a los datos, con visualizaciones y Genie/Q&A.
- **Track 3** entrega: App desplegada (Dash / Streamlit / Gradio) con UI funcional conectada a los datos; puede integrar Genie.

---

## Elige tu Escenario

Cada equipo elige **uno** de los 5 escenarios. **Todos** pueden resolverse con cualquiera
de los 3 tracks: el equipo decide con que track lo aborda.

| # | Escenario | Enfoque | Datos que mejor lo apoyan |
|---|-----------|---------|---------------------------|
| **1** | **Biblioteca Virtual Inteligente** ("Ask HR") | Consultar, sintetizar y reutilizar conocimiento institucional con GenAI | Genie sobre las tablas de People + documentos (ver aviso) |
| **2** | **Analitica Avanzada de Experiencia del Colaborador** | Detectar patrones, correlaciones y senales tempranas de riesgo (liderazgo, engagement, rotacion) | `tbl_yl_sayit` + `tbl_mth_datalake_personas` |
| **3** | **Automatizacion de Revision de Categorias y Compensacion Total** | Acelerar clasificacion organizacional y analisis de compensacion | `tbl_mth_datalake_personas` + `tabulador_cedulas_salariales` + `datos_de_mercado_sueldos` + `catalogo_puestos` |
| **4** | **Gestion de Talento Impulsada por IA** | Pasar de dashboards descriptivos a experiencias conversacionales con recomendaciones | `tbl_wkly_talento` + `talent_grid` + `tbl_mth_datalake_personas` + `tbl_wkly_capacitacion` |
| **5** | **Sucesion Basada en Datos** | Identificar y recomendar candidatos de sucesion con evidencia, respetando privacidad | `tbl_wkly_talento` + `talent_grid` + `tbl_mth_datalake_personas` |

Detalle completo de cada escenario en **[00. Casos-de-uso.md](00.%20Casos-de-uso.md)**.

---

## Los Datos

Dataset **100% simulado (ficticio)** de People / RRHH. **9 tablas** + **1 vista** + **1 volumen** (actualizado 21-sep-2026). No es dato real de Grupo Bimbo.

**Catalogo:** `cat_poc_sandbox_peopleai` &nbsp;&nbsp; **Schema:** `hackaton_2026_people_ai`

**Tablas de personas / hechos:**

| Tabla | Filas | Personas | Contenido |
|-------|-------|----------|-----------|
| `tbl_mth_datalake_personas` | 21,478 | 2,059 | Snapshot mensual: headcount, demografia, compensacion, 9-box, bajas. Sep-2024 a Ago-2026 |
| `tbl_wkly_capacitacion` | 37,118 | 1,274 | Eventos de capacitacion: curso, horas, estado, academia proveedora |
| `tbl_wkly_talento` | 2,974 | 2,974 | Revision de talento 2024-2026: potencial, readiness, fortalezas, movilidad |
| `tbl_yl_sayit` | 80,558 | 1,075 | Encuesta de clima "Say It" 2024/2025: favorabilidad por dimension |
| `talent_grid` | 389 | 389 | Assessment de competencias, traits y drivers (sten/percentil por atributo) |

**Tablas de referencia / catalogo:**

| Tabla | Filas | Contenido |
|-------|-------|-----------|
| `catalogo_puestos` | 958 | Catalogo global de puestos: familia, especialidad, nivel de carrera |
| `datos_de_mercado_sueldos` | 825 | Referencia de mercado (Mercer): sueldo base, efectivo garantizado, compensacion total |
| `tabulador_cedulas_salariales` | 51 | Bandas salariales internas (minimo/medio/maximo) por categoria |
| `dim_talent_grid` | 203 | Diccionario del `talent_grid` |

Ademas la vista `vw_sayit_personas` (clima + personas). **Nota: hoy esta rota** — ver pendientes.

**Llaves de union principales:** tablas de persona por `ID_Usuario_sin_prefijos` (LEFT JOIN, traslape parcial); `talent_grid` por `id_colaborador`; `tabulador` por `nombre_categoria` (match perfecto). El dato de **mercado/catalogo NO se une directo a personas** (referencia).

> **AVISO - DATOS SIMULADOS:** `clean_name`, `email_empresa` y `salario_mensual` son
> **ficticios** (nombres inventados, correos simulados, salarios completamente simulados);
> compensacion, sitios y organizaciones vienen codificados. No corresponden a personas reales,
> asi que no hay dato personal real que proteger. Aun asi, como buena practica de demo,
> presenta metricas agregadas en vez de filas individuales.

Referencia tecnica completa (columnas, tipos, queries validados, JOINs): **[Track 3/01. Catalogo-Tablas.md](Track%203%20-%20Databricks%20App/01.%20Catalogo-Tablas.md)**.

### Reglas importantes de los datos

| Regla | Detalle |
|-------|---------|
| **Clima limpio** | En `tbl_yl_sayit` filtra `scale = 'Likert'`; las preguntas de texto abierto tienen columnas desalineadas (comas embebidas en el CSV) |
| **Talento con dato** | Excluye `'Without Data'` y `''` en Performance/Potential/Readiness (la mayoria no tiene evaluacion) |
| **Etiquetas inconsistentes** | Desempenio/potencial/readiness traen variantes de casing y formato entre anios: normaliza antes de agrupar |
| **Snapshot reciente** | `personas` es mensual: filtra por `MAX(fecha_de_cierre)` para el estado actual |
| **Sin pais** | No hay dimension de pais; sitios/BU/organizacion estan hasheados |
| **Columnas con caracteres** | En `talento` usa backticks para nombres con `/ ? ¿` y digitos iniciales |

---

## Documentacion

### Track 1 - Genie Space
| Documento | Descripcion |
|-----------|-------------|
| [Guia de Datos para Genie](Track%201%20-%20Genie%20Space/01.%20Guia-Datos-Genie.md) | Los datos en lenguaje de negocio (sin SQL) + preguntas de ejemplo por escenario |
| [Guia para Crear tu Genie Space](Track%201%20-%20Genie%20Space/02.%20Guia-Crear-Genie-Space.md) | Paso a paso: crear Space, agregar tablas, instrucciones y preguntas. Incluye template de instrucciones |

### Track 2 - AI/BI Dashboard
| Documento | Descripcion |
|-----------|-------------|
| [Guia de Datos para Dashboard](Track%202%20-%20AI-BI%20Dashboard/01.%20Guia-Datos-Dashboard.md) | Metricas, dimensiones y datasets sugeridos por escenario |
| [Guia para Crear tu AI/BI Dashboard](Track%202%20-%20AI-BI%20Dashboard/02.%20Guia-Crear-AIBI-Dashboard.md) | Paso a paso: dataset, visualizaciones, filtros, forecasting y Genie sobre el dashboard |

### Track 3 - Databricks App
| Documento | Descripcion |
|-----------|-------------|
| [Catalogo de Tablas](Track%203%20-%20Databricks%20App/01.%20Catalogo-Tablas.md) | Referencia tecnica completa: columnas, tipos, queries validados, JOINs |
| [Notebook de Ejemplo](Track%203%20-%20Databricks%20App/02.%20Notebook-Ejemplo.py) | Notebook con SQL y PySpark listos para ejecutar por escenario |
| [Tutorial: Crear una Databricks App](Track%203%20-%20Databricks%20App/03.%20Tutorial-Databricks-App.py) | Tutorial con 3 frameworks (Streamlit, Dash, Gradio): app.yaml, requirements.txt y app.py |

### General
| Documento | Descripcion |
|-----------|-------------|
| [Casos de Uso](00.%20Casos-de-uso.md) | Los 5 escenarios en detalle: problema, reto, preguntas de negocio, tablas y valor esperado |
| [Docs-Ejemplo (MUESTRAS)](Docs-Ejemplo%20%28MUESTRAS%29/00.%20LEEME-ADVERTENCIA.md) | Documentos de MUESTRA para escenarios que requieren fuentes no incluidas en el dato. **Leer la advertencia** |

---

## Inicio Rapido

1. Entra al workspace y abre el catalogo `cat_poc_sandbox_peopleai` > schema `hackaton_2026_people_ai`.
2. Elige tu escenario en [00. Casos-de-uso.md](00.%20Casos-de-uso.md).
3. Elige tu track y sigue su guia:
   - **Track 1:** lee la Guia de Datos, crea tu Genie Space con el template de instrucciones, agrega 5+ preguntas y prueba.
   - **Track 2:** crea un dataset, arma visualizaciones, agrega filtros y activa Q&A/Genie sobre el dashboard.
   - **Track 3:** corre el Notebook de Ejemplo, elige framework y despliega tu app con el Tutorial.
4. Valida tus queries/preguntas antes de la demo.
5. Prepara tu pitch de 3 min: **Problema - Solucion - Demo en vivo - Impacto**.

---

## Evaluacion

| Criterio | Peso | Que se evalua |
|----------|------|---------------|
| Impacto en el negocio | 30% | Resuelve un problema real de People? Cuanto valor genera? |
| Funcionalidad | 25% | Funciona en vivo? Es usable? Demo real, no slides |
| Creatividad | 20% | Enfoque original? Uso inteligente de las herramientas? |
| Viabilidad a produccion | 15% | Que tan facil es llevarlo a datos productivos de Bimbo? |
| Presentacion | 10% | Claridad, storytelling, manejo del tiempo |

Consideracion transversal: **privacidad y gobierno**. Las soluciones que manejan dato
sensible de personas deben demostrar agregacion/anonimizacion y buen uso de Unity Catalog.

---

## Tips para Ganar

1. **Empieza simple, itera rapido** - mejor algo funcional que algo ambicioso a medias.
2. **Enfocate en el insight, no en la herramienta** - se evalua impacto de negocio.
3. **Usa los templates** - los documentos de este repo tienen codigo y config listos para copiar.
4. **Cuida el dato sensible** - agrega y anonimiza; no muestres nombres/salarios individuales.
5. **Valida antes de la demo** - corre tus queries/preguntas para confirmar que responden.
6. **Prepara la historia** - la narrativa importa tanto como la solucion.

---

## Estructura del Repositorio

```
bimbo-people-iq/
├── README.md                                   <- Este documento
├── 00. Casos-de-uso.md                         <- Los 5 escenarios en detalle
│
├── Track 1 - Genie Space/
│   ├── 01. Guia-Datos-Genie.md
│   └── 02. Guia-Crear-Genie-Space.md
│
├── Track 2 - AI-BI Dashboard/
│   ├── 01. Guia-Datos-Dashboard.md
│   └── 02. Guia-Crear-AIBI-Dashboard.md
│
├── Track 3 - Databricks App/
│   ├── 01. Catalogo-Tablas.md                  <- Referencia tecnica de los datos
│   ├── 02. Notebook-Ejemplo.py
│   └── 03. Tutorial-Databricks-App.py
│
└── Docs-Ejemplo (MUESTRAS)/                     <- MUESTRAS (no son dato real). Leer advertencia
    ├── 00. LEEME-ADVERTENCIA.md
    ├── S1_Ask-HR_Base-Conocimiento (MUESTRA).md
    ├── S3_Mercer_Benchmark-Compensacion (MUESTRA).md
    └── S5_Carpeta-Azul_Perfil-Sucesion (MUESTRA).md
```

---

# ⚠️ PENDIENTES / POR CONFIRMAR CON EL EQUIPO (antes del evento)

> Esta seccion lista lo que **no** esta en el dato del workspace hoy y lo que hay que
> aclarar o completar. Los documentos de `Docs-Ejemplo (MUESTRAS)/` son **solo muestras**
> ilustrativas creadas como placeholder; **no** son datos de Bimbo.
>
> **Actualizacion 21-sep-2026:** el equipo de dato agrego varias tablas de referencia. Esto
> **resuelve** parte de los pendientes anteriores (ver "Resueltos" abajo).

### ✅ Resuelto desde la ultima version (21-sep-2026)
- **Escenario 3 (Compensacion) — dato de mercado y bandas.** Ahora existen:
  `datos_de_mercado_sueldos` (825, benchmark tipo Mercer), `tabulador_cedulas_salariales`
  (51, bandas internas que **cruzan perfecto con personas** por `nombre_categoria`) y
  `catalogo_puestos` (958). Ya se puede hacer compa-ratio y equidad interna, y comparar
  contra mercado como referencia.
- **Talento / Sucesion — assessment de competencias.** `talent_grid` (389 personas, cruza por
  `id_colaborador`) + su diccionario `dim_talent_grid` habilitan analisis de competencias,
  traits, drivers y risk factors.

### 1. Documentos no estructurados AUN NO existen en el dato
El volumen contiene **solo CSV de origen** (incluido el nuevo `tabulador...csv`). Sigue sin
haber politicas, correos, SharePoint, PDFs ni documentos institucionales. Afecta:

- **Escenario 1 (Biblioteca Virtual / Ask HR):** el reto describe "correos, SharePoint,
  archivos locales, repositorios". **Nada de eso esta cargado.** &nbsp;➜ *Confirmar: el
  equipo aportara un set de documentos (PDF/DOCX/MD) para cargar al volumen? Cuales y de
  donde?*
- **Escenario 5 (Sucesion) — "Carpeta Azul":** la documentacion estrategica de sucesion
  **no esta en el volumen** (aunque el dato estructurado de sucesion mejoro con `talent_grid`).
  &nbsp;➜ *Confirmar: se cargara la Carpeta Azul? En que formato?*

Mientras tanto, cada guia resuelve la parte **estructurada** del escenario, y
`Docs-Ejemplo (MUESTRAS)/` muestra como se veria un documento fuente para que, si llega el
dato real, el flujo ya este listo (subir a volumen ➜ `ai_parse_document` ➜ Vector Search / Genie).

### 2. Dato de mercado/catalogo NO se une directo a la plantilla
`datos_de_mercado_sueldos` y `catalogo_puestos` se cruzan entre si por codigo de puesto, pero
**`personas` no trae codigo de puesto** y los titulos no empatan (0 de 105). &nbsp;➜ *Confirmar:
existe una tabla puente puesto↔codigo, o se compara solo via `nombre_categoria`/tabulador?*

### 3. Datos que el escenario asume pero el extracto no tiene
- **Pais / geografia:** el Escenario 2 habla de "+39 paises". El dato **no tiene columna de
  pais**; `lugar_de_trabajo`, BU y organizacion estan **hasheados** (7 sitios, ~1 BU).
  &nbsp;➜ *Confirmar: se agregara geografia o se acota al extracto?*
- **Cobertura parcial entre tablas:** Say It cubre 1,075 personas, capacitacion 1,274,
  talent_grid 389, contra 2,059 en personas. &nbsp;➜ *Confirmar si es esperado.*

### 4. Calidad de dato a validar
- **Vista `vw_sayit_personas` ROTA:** su definicion referencia `tbl_yr_sayit`, que fue
  **renombrada a `tbl_yl_sayit`**. Hoy la vista falla al consultarse. &nbsp;➜ *Actualizar la
  definicion de la vista al nuevo nombre.*
- **Comentario de `tbl_yl_sayit` desactualizado:** dice "37.080 filas / 387 personas"; el
  conteo real es **80,558 / 1,075**. &nbsp;➜ *Corregir el comentario de la tabla.*
- **`tbl_yl_sayit`:** persiste la desalineacion de columnas en preguntas de texto abierto.
  &nbsp;➜ *Recargar el CSV con comillas/escape correctos? (por ahora, filtrar `scale='Likert'`).*
- **Etiquetas inconsistentes** de desempenio/potencial/readiness entre anios, sistemas y
  tablas. &nbsp;➜ *Existe un diccionario/mapeo oficial para normalizarlas?*
- **9-box y talento mayormente `Without Data`.** &nbsp;➜ *Se cargara la evaluacion completa
  o se trabaja con el subconjunto evaluado?*

### 4. Logistica del evento a completar
- Canal de soporte en tiempo real (Slack/Teams).
- Ubicacion de recursos de codigo (el slide referencia un repo de GitHub por definir).
- Confirmar agenda por bloques del 23 y 24 de septiembre.
- Reglas de acceso al workspace y credenciales de los equipos.
- Premios y categorias finales.

---

*Repositorio de referencia: adaptado de un hackathon previo de Grupo Bimbo (BimboBricks IQ).*
