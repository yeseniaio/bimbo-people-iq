# Objetivos de Valor - Que deben lograr los usuarios de negocio

Checklist de **requisitos de exito** del hackathon desde la optica de negocio: que un usuario de
People / RRHH (no tecnico) **entienda y viva el valor de la plataforma Databricks**. No es una
lista de infraestructura (esa esta en `PRE-FLIGHT-CHECKLIST.md`); es la lista de **resultados**.

**Definicion de exito:** al cierre, cada participante de negocio puede decir *"le pregunte a mis
datos en lenguaje natural, obtuve una respuesta confiable y construi algo util yo mismo, sin
depender de un equipo tecnico"* — y sabe **como llevarlo a sus datos reales**.

Prioridad: 🔴 imprescindible &nbsp; 🟠 importante &nbsp; 🟡 deseable

---

## A. El "momento aha" que cada usuario de negocio debe vivir

- [ ] 🔴 **Hablar con los datos en lenguaje natural.** Cada participante hace **al menos 1
  pregunta en Genie** en espanol y recibe una respuesta con su grafico — sin escribir SQL.
- [ ] 🔴 **Obtener una respuesta confiable, con evidencia.** El usuario ve que Genie **muestra el
  SQL / la fuente** y entiende que no es una "caja negra" (confianza).
- [ ] 🔴 **Construir algo el mismo.** Cada equipo produce un **entregable funcional** (Genie
  Space o dashboard AI/BI) hecho por ellos, no por un coach.
- [ ] 🟠 **De descriptivo a conversacional.** El usuario experimenta preguntar "por que" y "que
  pasaria si" sobre un dashboard (no solo ver numeros estaticos).
- [ ] 🟠 **Sin infraestructura.** El usuario nota que **no configuro servidores ni clusters**
  (serverless): entra y trabaja.
- [ ] 🟡 **Autoservicio real.** El usuario expresa que podria repetir esto **sin ayuda** la
  proxima vez.

## B. Mensajes de valor que deben quedar claros (por capacidad)

- [ ] 🔴 **Genie** = *"le hablo a mis datos como a un analista, en mi idioma, sin SQL, y aprende
  de mi negocio."*
- [ ] 🔴 **AI/BI Dashboards** = *"tableros que ademas responden preguntas de seguimiento y
  explican los porques."*
- [ ] 🟠 **Databricks Apps** = *"convierto el analisis en una herramienta que otros usan"* (para
  los 1-2 equipos tecnicos; el resto lo ve en las demos).
- [ ] 🔴 **Unity Catalog / gobierno** = *"un solo lugar, con permisos y trazabilidad — datos
  confiables y seguros."* (Clave para People: dato sensible.)
- [ ] 🟠 **Una sola plataforma** = *"datos, IA, tableros y apps en el mismo lugar, sin mover
  informacion entre herramientas."*
- [ ] 🟠 **IA generativa aplicada a People** = *"puedo resumir, clasificar y recomendar sobre
  informacion de personas"* (ai_query, Ask HR).

## C. Valor de negocio por escenario (que problema real resuelve)

- [ ] 🟠 **Esc. 1 Ask HR:** "encuentro y reutilizo conocimiento sin buscar manualmente".
- [ ] 🔴 **Esc. 2 Experiencia del Colaborador:** "detecto focos rojos de clima/rotacion **antes**
  y priorizo acciones". (Escenario mejor soportado — buen candidato a demo estrella.)
- [ ] 🟠 **Esc. 3 Compensacion:** "comparo equidad interna y mercado en minutos, no dias".
- [ ] 🔴 **Esc. 4 Gestion de Talento:** "paso de tableros descriptivos a recomendaciones
  accionables para lideres".
- [ ] 🟠 **Esc. 5 Sucesion:** "identifico y comparo sucesores con evidencia, no por intuicion".

## D. Habilitacion durante el evento (para que el valor aterrice)

- [ ] 🔴 **Demo "el arte de lo posible"** al inicio: un Genie Space + un dashboard AI/BI en vivo
  con estos datos, para fijar la vara de lo alcanzable en el dia.
- [ ] 🔴 **Cada escenario ligado a un dolor real de People** (no un ejercicio tecnico): el brief
  arranca por el problema de negocio, no por la tabla.
- [ ] 🟠 **Coaches enfocados en desbloquear, no en construir por el equipo** (el valor se siente
  cuando lo hacen ellos).
- [ ] 🟠 **Lenguaje de negocio, no jerga.** Guias y demos en terminos de People (clima, rotacion,
  talento), no de ingenieria de datos.
- [ ] 🟡 **Reconocer el "primer insight"** de cada mesa en voz alta para reforzar el momento aha.

## E. Cierre y demos (evidenciar el valor)

- [ ] 🔴 Cada equipo presenta **en vivo** (no slides): **Problema - Solucion - Demo - Impacto**.
- [ ] 🔴 El pitch responde explicitamente **"cuanto valor genera"** (tiempo ahorrado, riesgo
  detectado, decision habilitada).
- [ ] 🟠 Al menos una demo muestra la transicion **dashboard ➜ pregunta conversacional ➜ accion**.
- [ ] 🟠 Criterio de jueces **Impacto en negocio = 30%** comunicado y aplicado (el valor pesa mas
  que la complejidad tecnica).

## F. Captura de valor y siguiente paso (que el valor no muera el viernes)

- [ ] 🔴 **Identificar 3-5 casos de uso reales** que los participantes quieran llevar a sus
  datos productivos (lista con dueno).
- [ ] 🟠 **Identificar champions**: quienes "se prendieron" y pueden impulsar adopcion en sus areas.
- [ ] 🟠 **Camino a produccion** claro por caso: que se necesita para pasar del dato simulado al
  real (accesos, fuentes, gobierno).
- [ ] 🟠 **Readout ejecutivo**: resumen de 1 pagina de los mejores casos y su valor potencial.
- [ ] 🟡 **Encuesta corta** post-evento: "?pudiste responder tus preguntas sin ayuda tecnica?"
  y NPS de la experiencia.

## G. Como medimos que el negocio "lo entendio" (metricas de exito)

- [ ] % de participantes que **crearon un entregable funcional** (meta: 100% de los 5 equipos).
- [ ] % que **hizo al menos 1 pregunta exitosa en Genie** (meta: alto / todos).
- [ ] # de **casos de uso reales** identificados para datos productivos (meta: >=3).
- [ ] # de **champions** identificados por area.
- [ ] Satisfaccion / NPS de los participantes de negocio.
- [ ] Menciones espontaneas de valor ("esto me ahorraria X", "esto lo necesito en mi area").

---

> Nota: dato 100% simulado. El objetivo del dia es que el negocio **entienda y quiera** la
> plataforma; el paso siguiente es replicar los casos ganadores sobre datos reales de People con
> el gobierno adecuado.
