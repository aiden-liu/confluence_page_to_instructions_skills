---
name: databricks-naming-modelling-guidelines
description: Provides step-by-step guidelines for naming conventions and data modelling in Databricks, including table and column naming, metadata handling, layer-specific rules, and best practices for creating dimensional models. Use this skill when designing, building, or reviewing Databricks data models to ensure consistency, clarity, and compliance.
metadata:
  source_page_id: "4095672332"
  source_page_version: "11"
  source_page_title: "DIP - Databricks Naming & Modelling Guidelines"
---
# Databricks Naming & Modelling Guidelines Skill

This skill provides comprehensive guidance for naming conventions and modelling practices in the Databricks environment, tailored to data engineering and modelling roles. These standards apply to Databricks only (not PowerBI or Azure Data Factory).

## Step-by-Step Instructions

### General Standards

1. **Time Zones**  
   - Always use UTC for metadata columns (e.g., load time, update time) to ensure consistency and avoid daylight saving time issues.

2. **Casing**  
   - Prefer snake_case for tables, columns, and other objects, unless the object directly mirrors the source system.
   - Unity Catalog stores table names in lower case; always use lower case for table names.
   - Silver layer: Use snake_case for all objects and columns.

### Bronze Layer

- **Table Names**
  - If the source has a specific table/file name, replicate the name (in lower case).
  - If no specific name, create a snake_case name.
  - **Do not use plurals** or abbreviations.

  **Table Name Examples:**
  ```
  assessment
  contract_type
  adjudication_reason
  ```

- **Column Names**
  - Retain source column names and casing.
  - If the source lacks column names (e.g., CSV without headers), use snake_case (lower case).

- **Metadata Columns**
  - Prefix with two underscores, upper case.
    - `__EXTRACT_AT` (timestamp): Date extracted from source.
    - `__LOAD_AT` (timestamp, UTC): Date loaded into Databricks.
    - `__RECORD_SOURCE` (string): Source or filename.
    - `__SOURCE_FILE_PATH` (string): Path to source file.
    - Additional optional columns: `__SEQUENCE_NUMBER`, `__EXTRACT_RUN_ID`, `__RESCUED_DATA` (for streaming).

  **Example Columns:**
  ```
  customerkey
  customer_code
  customer_name
  address
  city
  state
  __EXTRACT_AT
  __LOAD_AT
  __RECORD_SOURCE
  ```

### Copper Layer

- **Naming Conventions**
  - Table and column names should match the source.
  - Store in copper schema.
  - Use Lakeflow Declarative Pipelines where possible.

- **Metadata Columns**
  - All timestamps in UTC.
    - `__EXTRACT_AT`, `__LOAD_AT`, `__UPDATE_AT`, `__START_AT`, `__END_AT`
    - `__SOURCE_FILE_NAME` (optional)
  - Minimal calculations: Only for datatype conversion, null handling, etc.

- **Handling Log Files**
  - Assign row numbers if log file rows have variable columns.

### Silver Layer

- **Purpose**
  - Combined and transformed data matching business areas.

- **Naming**
  - Prefix with `silver_`.
  - Avoid plurals and unfamiliar abbreviations.
  - Use snake_case for all object names and columns.

  **Silver Table Examples:**
  ```
  _stg_incident
  dim_incident
  fact_incident
  ```

- **Column Renaming**
  - Columns can be renamed to match business terminology.
  - Use meaningful names; don't rely on table context.

  **Original --> Renamed:**
  ```
  name --> contract_name
  km --> kilometre
  m --> metre
  ```

- **Flags**
  - Boolean fields prefixed with `is_` or `has_`.
    - Example: `is_site_enforcing`, `has_enforcing_stage`

- **Spelling**
  - Use NZ English (e.g., centre, colour).

- **Date/Time Columns**
  - Suffix indicates type: `_date`, `_datetime`, `_time`
  - Business dates/times in NZ Standard time unless specified as UTC.

### Gold Layer

- **Modelling**
  - Prefer star schema for dimensional models.
  - Dimension tables: prefix `dim_`
  - Fact tables: prefix `fact_`
  - Dimension surrogate key: `dim_<dimension_name>_key`
  - Fact tables: consistent grain.

- **Metadata Columns (Dimensions)**
  - `__LOAD_AT`, `__UPDATE_AT`, `__VERSION`, `__START_AT`, `__END_AT`, `__IS_ACTIVE`, `__IS_LATEST`, `__CHANGE_HASH`

  - Unknown row defaults:
    - String: `Unknown`
    - Integer: `0`
    - Boolean: `?`
    - Date/Timestamp: `1899-01-01` (for unknown date)
    - Use surrogate key `0` for unknown rows.

  **Example Dimension Table Names:**
  ```
  dim_contract
  dim_incident
  dim_camera_site
  dim_date
  ```

  **Example Fact Table Names:**
  ```
  fact_contract
  fact_incident_stage_history
  summary_sales_by_month
  snapshot_sales_by_month
  ```

  - Role playing dimensions: create views as needed (mainly for date dimensions).

## Examples

- **Bronze Table Example:**
  ```
  assessment
  __EXTRACT_AT (timestamp, UTC)
  __LOAD_AT (timestamp, UTC)
  ```

- **Copper Table with Log Files:**
  ```
  event_log
  __EXTRACT_AT
  __LOAD_AT
  row_number
  ```

- **Silver Table Renamed Columns:**
  ```
  contract_name
  incident_datetime
  is_resolved
  ```

- **Gold Layer Surrogate Keys:**
  ```
  dim_camera_site_key
  dim_date_key (YYYYMMDD)
  ```

## Edge Cases

- **Source lacks column/table names:** Always default to snake_case.
- **Source provides plural names:** Convert to singular.
- **String fields used as flags:** Convert to boolean with `is_` or `has_` prefix.
- **Ambiguous time zones in source:** Always store in UTC for metadata.
- **Unknown values:** Always provide default unknown row as per data type.

## Source

Source page version: 11
