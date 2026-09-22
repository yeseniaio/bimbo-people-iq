# Pre-Flight Checklist - People AI Hackathon

Lista de verificacion para que el evento **corra sin friccion**. Marca cada item antes del dia.

**Evento:** Grupo Bimbo People AI Hackathon &nbsp;|&nbsp; **Fecha:** 23-24 sep 2026
**Workspace:** `https://adb-709692038187649.9.azuredatabricks.net`
**Datos:** `cat_poc_sandbox_peopleai.hackaton_2026_people_ai` (9 tablas, **100% simuladas**)
**Ultima verificacion:** 21-sep-2026

**Uso esperado:** la mayoria de los equipos usara **Genie (Track 1)** y **AI/BI Dashboards
(Track 2)**; solo **un par de equipos** haran **Databricks Apps (Track 3)**. La checklist
prioriza en consecuencia.

**Estado general:** Infraestructura ✅ lista. **Acceso ✅** (participantes en el grupo) y
**Genie ✅** (probado por el cliente). Los pendientes restantes son: **limpieza de dato (cliente:
vista, sayit)**, **concurrencia del warehouse** para Genie+dashboards, y el **grant de SP** solo
para los pocos equipos de Track 3.

Owners: **[C]** Cliente/dato &nbsp; **[O]** Organizador &nbsp; **[DBX]** Equipo Databricks &nbsp; **[E]** Equipos participantes
Prioridad: 🔴 bloqueante &nbsp; 🟠 importante &nbsp; 🟡 recomendado

---

## A. Acceso a los datos (LO MAS CRITICO - sin esto nadie trabaja)

- [x] 🔴 **[O/DBX]** ✅ **HECHO (21-sep-2026):** participantes agregados al grupo
  **`DnA - Databricks Hackaton Developers`** (unico con `SELECT` sobre el schema; `account users`
  solo tiene `BROWSE`). *Pendiente menor: confirmar que la lista final quede cubierta si se suman
  equipos de ultimo momento.*
- [ ] 🔴 **[O]** Confirmar que cada participante puede **entrar al workspace** (SSO/credenciales)
  y ve el catalogo `cat_poc_sandbox_peopleai`.
- [ ] 🟠 **[DBX]** Verificar que el grupo puede **crear objetos** para trabajar (Genie Spaces,
  dashboards, y tablas propias si las necesitan). El grupo ya tiene `CREATE_TABLE`, `EXECUTE`,
  `USE_CATALOG`, `USE_SCHEMA`.

## B. Genie (Track 1 - uso principal)

- [x] 🔴 **[DBX]** ✅ **HECHO (21-sep-2026):** **Genie habilitado** y validado — el cliente creo
  Genie Spaces de prueba con exito.
- [ ] 🔴 **[O/DBX]** Confirmar el **SQL Warehouse** que usaran los Spaces. Existe
  `CBHackaton_IAPeople` (serverless, 2X-Small). Ver seccion D (concurrencia).
- [ ] 🟡 **[O]** Tener 1 Space de demo ya armado (escenario 2) para el "arte de lo posible".

## C. AI/BI Dashboards (Track 2 - uso principal)

- [ ] 🔴 **[DBX]** Confirmar que pueden **crear dashboards AI/BI** y correr un dataset contra el
  warehouse.
- [ ] 🟠 **[O]** Confirmar que pueden **publicar/compartir** el dashboard (para la demo en vivo).
- [ ] 🟡 **[O]** Tener 1 dashboard de demo (escenario 2: clima + rotacion).

## D. Warehouse y concurrencia (afecta a Genie + AI/BI = casi todos)

- [ ] 🔴 **[O/DBX]** Como Genie y dashboards comparten warehouse y habra ~30 equipos, revisar
  **auto-scaling / max clusters** de `CBHackaton_IAPeople`. Un 2X-Small puede **encolar** con
  mucha concurrencia. Opciones: subir tamanio, subir max clusters, o **repartir** equipos entre
  los otros warehouses serverless que ya existen.
- [ ] 🟡 **[O]** El warehouse es **serverless** (arranca en segundos); no hace falta dejarlo
  prendido, pero puedes pre-calentarlo antes de arrancar.

## E. Bloqueadores de dato (limpieza - cliente)

- [ ] 🔴 **[C]** **Eliminar la vista `vw_sayit_personas`.** Hoy falla
  (`UC_DEPENDENCY_DOES_NOT_EXIST`) porque referencia una tabla renombrada. El cliente confirmo
  que la va a eliminar. La doc ya enruta a los equipos a un cruce de reemplazo sobre
  `tbl_yl_sayit`, asi que eliminarla evita que alguien tropiece.
- [ ] 🟠 **[C]** **Reexportar `sayit.csv` con comillas (RFC-4180) o como Parquet/Delta.**
  **1,328 de 80,558** filas tienen columnas desalineadas (comas en texto libre). Ver el pedido
  listo para enviar en la seccion H. Interino: filtrar `scale = 'Likert'`.
- [ ] 🟡 **[C]** **Corregir el comentario de `tbl_yl_sayit`** en Unity Catalog: dice
  "37,080 filas / 387 personas"; el real es **80,558 / 1,075**.
- [ ] 🟡 **[C]** Definir escenarios que dependen de **documentos** (Ask HR, Carpeta Azul): hoy el
  volumen solo tiene CSV. Decidir si se cargan documentos o se acota el alcance (Vector Search y
  embeddings ya estan listos si llegan los documentos).

## F. Databricks Apps (Track 3 - solo un par de equipos: on-demand)

> Solo aplica a los equipos que elijan Track 3. Atender **cuando** un equipo lo pida, no para todos.

- [ ] 🟠 **[DBX]** Por cada app creada: otorgar a su **service principal** (las apps NO corren
  como el usuario) `USE_CATALOG` + `USE_SCHEMA` + `SELECT` sobre
  `cat_poc_sandbox_peopleai.hackaton_2026_people_ai`. **Sin esto la app no lee dato** (falla
  silenciosa mas comun de Track 3).
- [ ] 🟡 **[E]** Usar el `03. Tutorial-Databricks-App.py` (Streamlit/Dash/Gradio) con el
  `app.yaml` y `requirements.txt` incluidos.
- [ ] 🟡 **[DBX]** Confirmar cuota para crear apps nuevas (el workspace ya tiene ~59 apps).

## G. Prueba de humo (correr la manana del evento, ~15 min)

- [ ] **[O/DBX]** Con una cuenta de participante de prueba (en el grupo):
  - [ ] `SELECT COUNT(*) FROM cat_poc_sandbox_peopleai.hackaton_2026_people_ai.tbl_mth_datalake_personas;` regresa 21,478.
  - [ ] Crear un Genie Space, agregar `tbl_yl_sayit` + `tbl_mth_datalake_personas`, preguntar
        *"% favorable por dimension en 2025"* y validar que responde (usa `scale='Likert'`).
  - [ ] Crear un dashboard AI/BI con un dataset simple y confirmar que renderiza.
  - [ ] (Si habra Track 3) desplegar la app del tutorial y confirmar que **lee** dato (probar el
        grant del SP).
  - [ ] Confirmar que el warehouse arranca y responde en segundos.

## H. Pedido listo para enviar al cliente (dato)

> **Vista:** Confirmamos la **eliminacion de `vw_sayit_personas`** (hoy falla porque referencia
> una tabla renombrada). Ya documentamos el cruce de reemplazo, asi que se puede eliminar sin
> impacto.
>
> **Encuesta Say It (`tbl_yl_sayit`):** detectamos ~**1,328** filas con **columnas
> desalineadas**. Las respuestas de texto libre traen comas y, al no venir entre comillas en el
> CSV, empujan el contenido a las columnas siguientes. Ejemplo real: una sola frase de valores
> quedo repartida entre `question`, `favorability`, `dimention` y `scale`, dejando `year` vacio
> (por eso aparecen valores como *"zero net carbon emissions"* en `favorability`). **?Pueden
> reexportar `sayit.csv` con los campos de texto entre comillas dobles (RFC-4180) — o entregarlo
> en Parquet/Delta —** para alinear las 80,558 filas? Interino: filtramos `scale='Likert'`.
>
> **Comentario de tabla:** el comment de `tbl_yl_sayit` dice "37,080/387"; el real es
> **80,558 filas / 1,075 personas** — ?lo pueden corregir?
>
> **Documentos (Ask HR / Carpeta Azul):** ?se cargaran documentos al volumen para los escenarios
> 1 y 5, o acotamos esos escenarios al dato estructurado?

---

## Anexo - Recordatorios de dato para los equipos (brief de 2 min)

- **Dato 100% simulado** (ficticio): nombres, correos y salarios no son reales.
- **Clima (`tbl_yl_sayit`):** filtra `scale = 'Likert'`.
- **Llave entre tablas de persona:** `ID_Usuario_sin_prefijos` (cobertura parcial - LEFT JOIN);
  dentro de personas usa `id_colaborador`; `talent_grid` cruza por `id_colaborador`; `tabulador`
  por `nombre_categoria`.
- **Snapshot:** `personas` es mensual - filtra `MAX(fecha_de_cierre)` para "hoy" y evita inflar
  metricas al cruzar con tablas de 1 fila por persona.
- **Mercado/catalogo** son de **referencia** (no se unen directo a personas).
- **Etiquetas** de desempenio/potencial/readiness: normaliza con `LOWER(TRIM())`.
- **No uses `vw_sayit_personas`** (sera eliminada); replica el cruce sobre `tbl_yl_sayit`.

Detalle completo en `Track 3 - Databricks App/01. Catalogo-Tablas.md` y en el README (Pendientes).
