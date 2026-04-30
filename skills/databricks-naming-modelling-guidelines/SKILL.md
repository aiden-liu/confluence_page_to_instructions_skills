---
name: databricks-naming-modelling-guidelines
description: Guidelines for naming conventions, metadata management, and modelling standards in Databricks, specifically for data engineering and data modelling activities in NZTA's Data Intelligence Platform. Use this skill whenever designing, naming, or modelling tables, columns, or schemas in Databricks to ensure consistency, clarity, and compliance.
metadata:
  source_page_id: "4095672332"
  source_page_version: "11"
  source_page_title: "DIP - Databricks Naming & Modelling Guidelines"
---
# Databricks Naming & Modelling Guidelines

These guidelines provide standards for naming conventions, metadata column usage, data modelling layers, and schema design in Databricks, applicable to data engineering and data modelling roles.

## Step-by-Step Instructions

### 1. **General Guidelines**
- Use UTC for all metadata timestamp columns to ensure consistency and avoid confusion related to daylight saving time and time zones.
- Apply snake_case (lowercase, using underscores) to names wherever possible, except when object names must match the source system.
- Avoid plurals and unnecessary abbreviations in naming.

### 2. **Bronze Layer**
Bronze tables hold raw data, closely mirroring the source.
- **Table Names:** Match source system table/file names; use lowercase due to Unity Catalog requirements.
  - Examples: `assessment`, `contracttype`, `area_of_interest`
- **If no source table name:** Use snake_case (e.g., `contract_type`). Avoid plurals (e.g., use `contract_type` not `contract_types`).
- **Column Names:** Retain source column names and casing. If none, use snake_case (lowercase).
- **Metadata Columns:** Prefix with two underscores and use upper case (e.g., `__EXTRACT_AT`, `__LOAD_AT`). All metadata timestamps in UTC.
- **Partition Columns:** Use `__YEAR`, `__MONTH`, `__DAY`.
- **Typical Example Table:**
  ```
  customerkey customer_code customer_name address city state
  __EXTRACT_AT __LOAD_AT __SOURCE_FILE_NAME
  ```

### 3. **Copper Layer**
Copper tables are historized and track all changes (SCD Type 2 behaviour).
- **Table/Column Names:** Match the source as much as possible.
- **Metadata Columns:** Include and inherit from bronze layer and add:
  - `__UPDATE_AT`, `__START_AT` (default to date added), `__END_AT` (default NULL), `__SOURCE_FILE_NAME`.
- **Minimal Calculations:** Retain original value, store calculated value separately.
- **Example Metadata Fields for Copper:**
  ```
  __EXTRACT_AT __LOAD_AT __UPDATE_AT __START_AT __END_AT __IS_LATEST __VERSION __CHANGE_HASH __SOURCE_FILE_NAME
  ```

### 4. **Silver Layer**
Silver tables transform and integrate data to match business areas.
- **Table Names:** Derived from copper, prefixed with business area. Stage tables are `_stg_` prefixed.
  - E.g., `silver_purchasing`, `_stg_incident`
- **Column Casing:** Use snake_case.
- **Column Naming:** Names should be meaningful, clear (e.g., `contract_name`, not `name`). Columns can be renamed for business clarity.
- **Flags:** Should be boolean, with `is_` or `has_` prefix (e.g., `is_site_enforcing`).
- **Abbreviations:** Use only common ones (e.g., `id`, `km`). Avoid obscure/system-specific abbreviations.
- **Spelling:** Use NZ English (e.g., `centre`, `colour`).
- **Date/Time columns:** Suffix to clarify type, e.g., `event_datetime_utc`. Databricks lacks a `time` type; use string if necessary.

### 5. **Gold Layer**
Gold tables are designed for analytics, typically using a star schema:
- **Star Schema is Preferred:** Follow Kimball methodologies where possible.
- **Table Names:**
  - Dimension tables prefixed with `dim_` (e.g., `dim_incident`)
  - Fact tables prefixed with `fact_` (e.g., `fact_incident_stage_history`)
  - Snapshot and summary tables prefixed as `snapshot_`, `summary_`
- **Surrogate Keys:** Dimensions require unique surrogate keys named as `dim_<dimension>_key` (e.g., `dim_camera_site_key`). For date dimensions, use `YYYYMMDD`.
- **Unknown Row:** Dimension tables should include a default "unknown" row (`0` for integer keys, `1899-01-01` for dates).
- **Business/Natural Keys:** Generally not included in fact tables, unless necessary for model filtering.
- **Fact-less Fact Tables:** May be used for many-to-many relationships; same conventions as fact tables.
- **Views:** Named according to their functional role (e.g., `dim_`, `fact_`, `summary_`).

## Examples

### Valid Table Names
- `assessment`
- `contract_type`
- `dim_contract`
- `fact_incident_stage_history`
- `snapshot_sales_by_month`
- `summary_sales_by_month`

### Invalid Table Names
- `assessments` (plural; use singular)
- `adj_reasons` (abbreviation; use full terms)
- `objectshitdescription` (no snake_case; should be `object_hit_description`)

### Valid Metadata Columns
- `__EXTRACT_AT`
- `__LOAD_AT`
- `__RECORD_SOURCE`
- `__START_AT`
- `__END_AT`

### Edge Cases

- If the source system has non-standard names or abbreviations, retain them only for Bronze/Copper layers.
- Columns without names (e.g., CSV without headers) should always be created in snake_case.
- For streaming tables, include `__RESCUED_DATA` as needed.
- Dimension unknown row: Set integer surrogate key to `0`, date key to `1899-01-01`.

## Source

Source page version: 11

Detailed reference: [references/REFERENCE.md](references/REFERENCE.md)
