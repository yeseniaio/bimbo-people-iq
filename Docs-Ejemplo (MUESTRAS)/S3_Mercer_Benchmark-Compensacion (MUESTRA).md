# Muestra - Benchmark de Compensacion de Mercado (Escenario 3)

**⚠️ MUESTRA FICTICIA - NO son datos reales de Grupo Bimbo. Placeholder para ilustrar el formato. Confirmar el documento real con el equipo (ver README).**

> **USA LAS TABLAS DEL WORKSPACE.** Para el Escenario 3 existen tablas en el workspace:
> **`datos_de_mercado_sueldos`** (benchmark de mercado por puesto: sueldo base, efectivo
> garantizado, compensacion total) y **`tabulador_cedulas_salariales`** (bandas internas
> min/medio/max, que cruzan perfecto con `personas` por `nombre_categoria`). Usa esas tablas para
> compa-ratio y equidad; esta muestra queda solo como ilustracion del formato. Ver
> `Track 3 - Databricks App/01. Catalogo-Tablas.md`.

==================== INICIO DE MUESTRA (CONTENIDO FICTICIO) ====================

# Benchmark de Mercado - Compensacion Total (extracto ilustrativo)

**Proveedor (ejemplo):** Mercer - Encuesta de Compensacion (ficticia)
**Moneda:** MXN mensual (cifras inventadas)
**Corte:** ejemplo

Las cifras P25/P50/P75 representan los percentiles de mercado. El **compa-ratio** compara el
salario interno promedio contra la mediana de mercado (P50): `compa_ratio = salario_interno / P50`.

| Job Family (ejemplo) | Nivel | P25 | P50 (mediana) | P75 | Compa-ratio interno |
|----------------------|-------|-----|---------------|-----|---------------------|
| Supply Chain - Operaciones | Operativo | 9,500 | 12,000 | 15,500 | 0.98 |
| Supply Chain - Planeacion | Administrativo | 22,000 | 28,000 | 36,000 | 1.03 |
| Demand Chain - Ventas | Administrativo | 20,000 | 26,000 | 34,000 | 0.95 |
| Finance - Analisis | Administrativo | 24,000 | 31,000 | 41,000 | 1.01 |
| People - Talent | Supervisor | 38,000 | 48,000 | 62,000 | 0.92 |
| Top Management | Directivo | 120,000 | 165,000 | 220,000 | 0.99 |

## Como se leeria

- **Compa-ratio < 0.90:** posible rezago vs mercado (riesgo de retencion).
- **Compa-ratio 0.90 - 1.10:** alineado a mercado.
- **Compa-ratio > 1.10:** por encima de mercado (revisar equidad interna).

> Nota: el dato real de mercado provendria de **Mercer** u otra encuesta autorizada. El
> analisis interno (dispersion, equidad, rangos por categoria) SI se puede hacer hoy con
> `tbl_mth_datalake_personas` (`salario_mensual`, `nombre_categoria`, `nivel`).

==================== FIN DE MUESTRA ====================

> Tabla y cifras 100% inventadas. Sirve solo para ilustrar el cruce interno vs mercado.
