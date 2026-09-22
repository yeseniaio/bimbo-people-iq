# Innovation Sprint People + IA - Hackathon

**Grupo Bimbo People AI Hackathon**

Hackathon enfocado en Databricks, GenAI, Genie, AI/BI y Databricks Apps, aplicado a datos de
**People / Recursos Humanos**.

**Fecha:** 23-24 de septiembre de 2026
**Plataforma:** Databricks Workspace (Sandbox) `https://adb-709692038187649.9.azuredatabricks.net`
**Datos:** People / RRHH - **100% SIMULADOS (ficticios)**
**Objetivo del dia:** Demo funcional + presentacion (3 min de pitch)

> ⚠️ **DATOS 100% SIMULADOS.** Todo el dato de este hackathon es **ficticio** — **NO es
> informacion real de Grupo Bimbo**. Nombres, correos y salarios son **inventados/simulados** y
> no representan a personas reales. Aun asi, como buena practica, presenta metricas **agregadas**
> en tus demos.

---

## Elige tu Track

Tres tracks. Cada equipo elige **uno**. Los tres resuelven los mismos escenarios de negocio.

| Track | Para quien | Que construyes | Dificultad | Habilidades |
|-------|-----------|----------------|------------|-------------|
| **Track 1 - Genie Space** | Negocio, analistas | Un espacio conversacional que responde preguntas en lenguaje natural | Facil | Conocimiento del negocio. SQL opcional |
| **Track 2 - AI/BI Dashboard** | Negocio, analistas | Un dashboard AI/BI interactivo con Q&A en lenguaje natural | Facil | Conocimiento del negocio. SQL basico |
| **Track 3 - Databricks App** | Perfil tecnico | Una app desplegada en Databricks Apps | Medio | Python (basico-intermedio), SQL |

- **Track 1** entrega: Genie Space funcional con 5+ preguntas de ejemplo y demo en vivo.
- **Track 2** entrega: AI/BI Dashboard publicado, conectado a los datos, con visualizaciones y Q&A.
- **Track 3** entrega: App desplegada (Streamlit / Dash / Gradio) conectada a los datos.

---

## Elige tu Escenario

Cada equipo elige **uno** de los 5 escenarios. **Todos** se pueden resolver con cualquiera de los
3 tracks: el equipo decide con que track lo aborda.

| # | Escenario | De que trata |
|---|-----------|--------------|
| **1** | **Biblioteca Virtual Inteligente ("Ask HR")** | Consultar, sintetizar y reutilizar conocimiento institucional con GenAI |
| **2** | **Analitica Avanzada de Experiencia del Colaborador** | Detectar patrones y senales tempranas de riesgo: liderazgo, engagement, rotacion |
| **3** | **Revision de Categorias y Compensacion Total** | Acelerar clasificacion organizacional y analisis de compensacion (equidad, bandas, mercado) |
| **4** | **Gestion de Talento Impulsada por IA** | De dashboards descriptivos a experiencias conversacionales con recomendaciones |
| **5** | **Sucesion Basada en Datos** | Identificar y recomendar candidatos de sucesion con evidencia |

Detalle de cada escenario (problema, reto, preguntas de negocio, valor esperado):
**[00. Casos-de-uso.md](00.%20Casos-de-uso.md)**.

---

## Los Datos

Dataset **100% simulado** de People / RRHH en el catalogo `cat_poc_sandbox_peopleai`,
schema `hackaton_2026_people_ai`.

**Tablas de personas:**

| Tabla | De que trata |
|-------|--------------|
| `tbl_mth_datalake_personas` | Foto mensual del colaborador: headcount, demografia, compensacion, evaluacion, bajas |
| `tbl_wkly_capacitacion` | Cursos y capacitacion (tipo, horas, estado, academia) |
| `tbl_wkly_talento` | Revision de talento 2024-2026: potencial, readiness, movilidad |
| `tbl_yl_sayit` | Encuesta de clima "Say It" 2024/2025: favorabilidad por dimension |
| `talent_grid` | Assessment de competencias, traits y drivers por colaborador |

**Tablas de referencia (para comparar):**

| Tabla | De que trata |
|-------|--------------|
| `catalogo_puestos` | Catalogo global de puestos (familia, especialidad, nivel de carrera) |
| `datos_de_mercado_sueldos` | Referencia de mercado: sueldo base y compensacion total |
| `tabulador_cedulas_salariales` | Bandas salariales internas (minimo/medio/maximo) por categoria |
| `dim_talent_grid` | Diccionario del `talent_grid` |

- **Detalle tecnico** (columnas, tipos, llaves, queries listos para copiar):
  [Catalogo de Tablas](Track%203%20-%20Databricks%20App/01.%20Catalogo-Tablas.md).
- **Reglas de datos y notas** (como no romper tus analisis): ver
  [NOTAS-TECNICAS.md](NOTAS-TECNICAS.md).

---

## Documentacion

### Track 1 - Genie Space
| Documento | Descripcion |
|-----------|-------------|
| [Guia de Datos para Genie](Track%201%20-%20Genie%20Space/01.%20Guia-Datos-Genie.md) | Los datos en lenguaje de negocio (sin SQL) + preguntas de ejemplo |
| [Guia para Crear tu Genie Space](Track%201%20-%20Genie%20Space/02.%20Guia-Crear-Genie-Space.md) | Paso a paso + template de instrucciones listo para copiar |

### Track 2 - AI/BI Dashboard
| Documento | Descripcion |
|-----------|-------------|
| [Guia de Datos para Dashboard](Track%202%20-%20AI-BI%20Dashboard/01.%20Guia-Datos-Dashboard.md) | Metricas, dimensiones y datasets sugeridos por escenario |
| [Guia para Crear tu AI/BI Dashboard](Track%202%20-%20AI-BI%20Dashboard/02.%20Guia-Crear-AIBI-Dashboard.md) | Paso a paso: dataset, visualizaciones, filtros y Genie sobre el dashboard |

### Track 3 - Databricks App
| Documento | Descripcion |
|-----------|-------------|
| [Catalogo de Tablas](Track%203%20-%20Databricks%20App/01.%20Catalogo-Tablas.md) | Referencia tecnica completa de los datos |
| [Notebook de Ejemplo](Track%203%20-%20Databricks%20App/02.%20Notebook-Ejemplo.py) | SQL y PySpark listos para ejecutar por escenario |
| [Tutorial: Crear una Databricks App](Track%203%20-%20Databricks%20App/03.%20Tutorial-Databricks-App.py) | 3 frameworks (Streamlit, Dash, Gradio) con app.yaml y requirements |

### General
| Documento | Descripcion |
|-----------|-------------|
| [Casos de Uso](00.%20Casos-de-uso.md) | Los 5 escenarios en detalle |
| [Docs-Ejemplo (MUESTRAS)](Docs-Ejemplo%20%28MUESTRAS%29/00.%20LEEME-ADVERTENCIA.md) | Documentos de MUESTRA (ficticios) para ilustrar formatos |

---

## Inicio Rapido

1. Entra al workspace y abre el catalogo `cat_poc_sandbox_peopleai` > schema `hackaton_2026_people_ai`.
2. Elige tu escenario en [00. Casos-de-uso.md](00.%20Casos-de-uso.md).
3. Elige tu track y sigue su guia:
   - **Track 1:** crea tu Genie Space con el template de instrucciones, agrega 5+ preguntas y prueba.
   - **Track 2:** crea un dataset, arma visualizaciones, agrega filtros y activa Q&A/Genie.
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
| Viabilidad a produccion | 15% | Que tan facil es llevarlo a datos productivos? |
| Presentacion | 10% | Claridad, storytelling, manejo del tiempo |

---

## Tips para Ganar

1. **Empieza simple, itera rapido** - mejor algo funcional que algo ambicioso a medias.
2. **Enfocate en el insight, no en la herramienta** - se evalua impacto de negocio.
3. **Usa los templates** - las guias de este repo tienen codigo y config listos para copiar.
4. **Presenta agregado** - metricas y tendencias, no registros individuales.
5. **Valida antes de la demo** - corre tus queries/preguntas para confirmar que responden.
6. **Prepara la historia** - la narrativa importa tanto como la solucion.

---

## Estructura del Repositorio

```
bimbo-people-iq/
├── README.md                                   <- Este documento (arranque para participantes)
├── 00. Casos-de-uso.md                         <- Los 5 escenarios en detalle
│
├── Track 1 - Genie Space/
│   ├── 01. Guia-Datos-Genie.md
│   └── 02. Guia-Crear-Genie-Space.md
├── Track 2 - AI-BI Dashboard/
│   ├── 01. Guia-Datos-Dashboard.md
│   └── 02. Guia-Crear-AIBI-Dashboard.md
├── Track 3 - Databricks App/
│   ├── 01. Catalogo-Tablas.md                  <- Referencia tecnica de los datos
│   ├── 02. Notebook-Ejemplo.py
│   └── 03. Tutorial-Databricks-App.py
│
├── Docs-Ejemplo (MUESTRAS)/                     <- MUESTRAS ficticias (formato de documentos)
│
├── OBJETIVOS-VALOR.md                          <- (interno) que valor debe llevarse el negocio
├── NOTAS-TECNICAS.md                           <- (interno) reglas de datos + pendientes
└── PRE-FLIGHT-CHECKLIST.md                      <- (interno) preparacion del evento
```

> **Organizadores y coaches:** ver [OBJETIVOS-VALOR.md](OBJETIVOS-VALOR.md) (que deben lograr los
> usuarios de negocio), [NOTAS-TECNICAS.md](NOTAS-TECNICAS.md) (reglas de datos y pendientes) y
> [PRE-FLIGHT-CHECKLIST.md](PRE-FLIGHT-CHECKLIST.md) (estado de preparacion).
