# Pre-Flight Checklist - People AI Hackathon

Lista de verificacion para que el evento **corra sin friccion**. Marca cada item antes del dia.

**Evento:** Grupo Bimbo People AI Hackathon &nbsp;|&nbsp; **Fecha:** 23-24 sep 2026
**Workspace:** `https://adb-709692038187649.9.azuredatabricks.net`
**Datos:** `cat_poc_sandbox_peopleai.hackaton_2026_people_ai` (**10 tablas**, **100% simuladas**)

**Escala:** **5 equipos x 5 personas = 25 participantes.**
**Uso esperado:** la mayoria de los 5 equipos usara **Genie (Track 1)** y **AI/BI Dashboards
(Track 2)**; solo **1-2 equipos** haran **Databricks Apps (Track 3)**. La checklist prioriza en
consecuencia. Con solo 5 equipos, la carga sobre el warehouse es **baja** (ver seccion D).

**Estado general:** Infraestructura ✅. **Acceso ✅** (participantes en el grupo). **Genie ✅**
(probado por el cliente). Concurrencia ✅ (solo 5 equipos). Grants de SP ✅ (los crea el
organizador on-demand). Documentos Ask HR ✅ (se resuelven el dia del evento). **No hay
bloqueadores de dato abiertos.**

> ⚠️ **PARA CONFIRMAR CON EL CLIENTE:**
> 1. `perfiles_puesto_sucesion` — confirmar que es la fuente oficial de perfiles de sucesion
>    (Carpeta Azul estructurada) y si habra documentos narrativos adicionales.
> 2. **Agent Bricks / Knowledge Assistant** — ?esta habilitado en el workspace/region? (solo
>    necesario para el **Track 4 opcional**, si algun equipo usa documentos; ver §I).

Owners: **[C]** Cliente/dato &nbsp; **[O]** Organizador &nbsp; **[DBX]** Equipo Databricks &nbsp; **[E]** Equipos participantes
Prioridad: 🔴 bloqueante &nbsp; 🟠 importante &nbsp; 🟡 recomendado

---

## A. Acceso a los datos (LO MAS CRITICO - sin esto nadie trabaja)

- [x] 🔴 **[O/DBX]** ✅ **HECHO (21-sep-2026):** participantes agregados al grupo
  **`DnA - Databricks Hackaton Developers`** (unico con `SELECT` sobre el schema; `account users`
  solo tiene `BROWSE`). *Pendiente menor: confirmar que la lista final quede cubierta si se suman
  equipos de ultimo momento.*
- [x] 🔴 **[O]** ✅ **HECHO:** confirmar que cada participante puede **entrar al workspace** (SSO/credenciales)
  y ve el catalogo `cat_poc_sandbox_peopleai`.
- [x] 🟠 **[DBX]** ✅ **HECHO:** verificar que el grupo puede **crear objetos** para trabajar (Genie Spaces,
  dashboards, y tablas propias si las necesitan). El grupo ya tiene `CREATE_TABLE`, `EXECUTE`,
  `USE_CATALOG`, `USE_SCHEMA`.

## B. Genie (Track 1 - uso principal)

- [x] 🔴 **[DBX]** ✅ **HECHO (21-sep-2026):** **Genie habilitado** y validado — el cliente creo
  Genie Spaces de prueba con exito.
- [x] 🔴 **[O/DBX]** ✅ **HECHO:** confirmar el **SQL Warehouse** que usaran los Spaces. Existe
  `CBHackaton_IAPeople` (serverless, 2X-Small). Ver seccion D (concurrencia).
- [x] 🟡 **[O]** ✅ **HECHO (22-sep):** 1 Space de demo armado (escenario 2) para el "arte de lo posible".

## C. AI/BI Dashboards (Track 2 - uso principal)

- [x] 🔴 **[DBX]** ✅ **HECHO:** confirmar que pueden **crear dashboards AI/BI** y correr un dataset contra el
  warehouse.
- [x] 🟠 **[O]** ✅ **HECHO (22-sep):** confirmado que pueden **publicar/compartir** el dashboard (demo en vivo).
- [x] 🟡 **[O]** ✅ **HECHO (22-sep):** 1 dashboard de demo (escenario 2: clima + rotacion).

## D. Warehouse (riesgo BAJO con 5 equipos)

- [ ] 🟡 **[O/DBX]** Con **5 equipos** compartiendo `CBHackaton_IAPeople` (serverless, 2X-Small),
  la concurrencia **no es problema** y el dato es chico. No hace falta subir tamanio. Solo
  confirmar que el warehouse **arranca** (serverless: en segundos) y, si acaso, dejar el
  auto-scaling en >=2 clusters por si varios equipos consultan a la vez.
- [ ] 🟡 **[O]** Opcional: **pre-calentar** el warehouse (una query) justo antes de arrancar para
  que la primera experiencia sea instantanea.
- [ ] 🟡 **[O]** Existen otros warehouses serverless por si quieres dar uno dedicado a un equipo
  pesado; con 5 equipos normalmente no es necesario.

## E. Dato (cliente)

> ✅ **No hay bloqueadores de dato abiertos.** Las 10 tablas estan listas para el evento.

- [x] 🟢 **[O]** **Documentos Ask HR (Esc. 1): se resuelven el DIA del evento.** Se aportaran
  on-demand en el hackathon (no bloquean el arranque). Vector Search y embeddings ya estan listos
  para indexar cuando lleguen los documentos; los equipos de esos escenarios trabajan la parte
  estructurada mientras tanto (incl. `perfiles_puesto_sucesion` para sucesion).

## F. Databricks Apps (Track 3 - solo 1-2 de los 5 equipos: on-demand)

> Solo aplica a los 1-2 equipos que elijan Track 3. Atender **cuando** un equipo lo pida, no para todos.

- [x] 🟢 **[O]** **Grants de service principal: los creare on-demand.** ✅ Plan confirmado: cuando
  un equipo despliegue una app, el organizador otorga a su **SP** (las apps NO corren como el
  usuario) `USE_CATALOG` + `USE_SCHEMA` + `SELECT` sobre
  `cat_poc_sandbox_peopleai.hackaton_2026_people_ai`. Sin esto la app no lee dato.
  - Comando de referencia: `databricks grants update schema cat_poc_sandbox_peopleai.hackaton_2026_people_ai --json '{"changes":[{"principal":"<APP_SP>","add":["USE_SCHEMA","SELECT"]}]}' --profile sandbox_gb` (mas `USE_CATALOG` a nivel catalogo).
- [ ] 🟡 **[E]** Usar el `03. Tutorial-Databricks-App.py` (Streamlit/Dash/Gradio) con el
  `app.yaml` y `requirements.txt` incluidos.
- [ ] 🟡 **[DBX]** Confirmar cuota para crear apps nuevas (el workspace ya tiene ~59 apps).

## G. Prueba de humo (correr la manana del evento, ~15 min)

- [x] **[O/DBX]** ✅ **HECHO (22-sep):** prueba de humo completa con una cuenta de participante de prueba (en el grupo):
  - [x] `SELECT COUNT(*) FROM cat_poc_sandbox_peopleai.hackaton_2026_people_ai.tbl_mth_datalake_personas;` regresa 21,478.
  - [x] Crear un Genie Space, agregar `tbl_yl_sayit` + `tbl_mth_datalake_personas`, preguntar
        *"% favorable por dimension en 2025"* y validar que responde (usa `scale='Likert'`).
  - [x] Crear un dashboard AI/BI con un dataset simple y confirmar que renderiza.
  - [ ] (Si habra Track 3) desplegar la app del tutorial y confirmar que **lee** dato (probar el
        grant del SP). *— pendiente, solo si un equipo elige Track 3.*
  - [x] Confirmar que el warehouse arranca y responde en segundos.

## H. Pedido listo para enviar al cliente (dato)

> **Perfiles de sucesion (`perfiles_puesto_sucesion`):** confirmar que es la fuente oficial de
> perfiles de exito para el Escenario 5 (16 roles criticos). ?Habra documentos narrativos
> adicionales (Carpeta Azul) o el equipo trabaja con esta tabla estructurada?
>
> **Documentos (Ask HR):** ?se cargaran documentos al volumen para el Escenario 1, o lo acotamos
> al dato estructurado (People Data + `perfiles_puesto_sucesion`)?

## I. Track 4 - Knowledge Assistant / Agent Bricks (OPCIONAL - solo si hay documentos)

> Solo aplica si un equipo decide trabajar el **Escenario 1 (Ask HR)** o el 5 con **documentos**
> (dato no estructurado). Para dato en tablas NO se necesita nada de esto. Los documentos se
> aportan el dia del evento; atender **cuando** un equipo lo pida.

- [ ] 🟠 **[DBX]** **Confirmar que Agent Bricks / Knowledge Assistant esta habilitado** en el
  workspace (depende de region y features serverless). Si no aparece en el menu **Agents**, ese
  track no esta disponible y los equipos usan Track 1/2/3. **Preguntar mañana** (ver box arriba).
- [ ] 🟡 **[O]** Tener listo un **Volumen de UC** para documentos (ej.
  `cat_poc_sandbox_peopleai.hackaton_2026_people_ai.docs_ask_hr`) y el set de documentos de MUESTRA/ficticios.
- [ ] 🟡 **[O]** Verificar permisos de UC sobre el volumen (`USE CATALOG` + `USE SCHEMA` +
  `READ VOLUME`) para el grupo y para la identidad del agente.
- [ ] 🟡 **[E]** Usar la guia `Track 4 - Knowledge Assistant (Opcional)/01. Guia-Knowledge-Assistant.md`.

---

## Anexo - Recordatorios de dato para los equipos (brief de 2 min)

- **Dato 100% simulado** (ficticio): nombres, correos y salarios no son reales.
- **Clima (`tbl_yl_sayit`):** filtra `scale = 'Likert'` (76,520 filas / 1,072 personas).
- **Sucesion (Esc. 5):** `perfiles_puesto_sucesion` (16 roles) es el **perfil objetivo**; compara candidatos vs `capacidades_criticas` ≈ `talent_grid`.
- **Llave entre tablas de persona:** `ID_Usuario_sin_prefijos` (cobertura parcial - LEFT JOIN);
  dentro de personas usa `id_colaborador`; `talent_grid` cruza por `id_colaborador`; `tabulador`
  por `nombre_categoria`.
- **Snapshot:** `personas` es mensual - filtra `MAX(fecha_de_cierre)` para "hoy" y evita inflar
  metricas al cruzar con tablas de 1 fila por persona.
- **Mercado/catalogo** son de **referencia** (no se unen directo a personas).
- **Etiquetas** de desempenio/potencial/readiness: normaliza con `LOWER(TRIM())`.
- **Clima + personas:** cruza `tbl_yl_sayit` con personas por llave compuesta (id + mes + anio).

Detalle completo en `Track 3 - Databricks App/01. Catalogo-Tablas.md` y en el README (Pendientes).
