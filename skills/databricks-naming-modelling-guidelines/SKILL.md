---
name: databricks-naming-modelling-guidelines
description: Provides comprehensive naming and modelling guidelines for data engineering and modelling in Databricks. Use when creating, naming, and structuring schemas, tables, columns, metadata, and layers according to NZTA standards. Applicable for Databricks, not PowerBI or Azure Data Factory.
metadata:
  source_page_id: "4095672332"
  source_page_version: "11"
  source_page_title: "DIP - Databricks Naming & Modelling Guidelines"
---
# Databricks Naming & Modelling Guidelines

This skill provides step-by-step directions and examples for proper naming conventions and structuring of data models in Databricks, as per NZTA Data Chapter standards (Draft as at 2026-03-18). Intended for data engineering and data modelling roles.

## General Guidelines

### 1. Metadata Columns  
- Always store timestamp metadata columns in UTC to ensure consistency and avoid ambiguity from time zones or daylight savings.
- Common metadata columns are prefixed with two underscores (`__`) and are in UPPER CASE (e.g., `__EXTRACT_AT`, `__LOAD_AT`).

#### Advantages of UTC:
- Consistency across global users and systems.
- Simplifies logic (no time zone conversion required).
- Avoids issues with daylight saving.
- Reduces errors in time calculations.

---

### 2. Casing Standards
- Use `snake_case` (lowercase, underscores between words) for table and column names, except when objects are directly based on source system naming.
- Example: `contract_type`, `area_of_interest`.

---

## Layer-specific Guidelines

### Bronze Layer
- Tables are raw, reflect closest possible to source.
- Names should match source (converted to lowercase).  
  - If no clear source name exists, use `snake_case`.
- Avoid plurals and abbreviations.
  - Good: `contract_type`  
  - Avoid: `contract_types`, `adj_reasons`.
- Column names retain source casing unless source is unstructured (e.g., CSV without headers, then use snake_case).

#### Mandatory Metadata Columns (prefixed with `__`):
| Column Name       | Type      | Mandatory | Notes                                    |
|-------------------|-----------|-----------|------------------------------------------|
| __EXTRACT_AT      | timestamp | Yes       | Extraction date from source system       |
| __LOAD_AT         | timestamp | Yes       | Date loaded into Databricks (UTC)        |
| __RECORD_SOURCE   | String    | Yes       | Identifies source/file name              |

- Optional Metadata Columns: `__SOURCE_FILE_PATH`, `__SEQUENCE_NUMBER`, `__EXTRACT_RUN_ID`, `__RESCUED_DATA`

---

### Copper Layer
- Historized copy; fully tracks changes (SCD 2 equivalent).
- Use Lakeflow Declarative Pipelines where possible.
- Table and column names match source.
- Metadata timestamps are in UTC.
- Minimal calculations at this layer; retain original values, store calculated separately.

#### Additional Copper Metadata Columns:
- `__UPDATE_AT`, `__START_AT`, `__END_AT`, `__SOURCE_FILE_NAME`  
- Partition columns: `__YEAR`, `__MONTH`, `__DAY`

---

### Silver Layer
- Combines and transforms data for business area.
- Object naming: `silver_[business_area]`; Staging prefixed by `_stg_` if not for gold.
- Use snake_case for tables and columns.
- Columns can be renamed to reflect business terminology.
- Avoid plurals and nonstandard abbreviations (only use commonly accepted ones like `id`, `km`).

#### Flags
- Store as boolean, prefixed `is_` or `has_` (e.g., `is_resolved`, `has_enforcing_stage`).

#### Date & Time Columns
- Suffix indicates type: `_date`, `_datetime`, `_time`, etc.
- Business dates/times in NZ Standard time (unless column name specifies UTC).

---

### Gold Layer

#### Star Schema Modelling
- Preferred approach; use `dim_` for dimensions, `fact_` for fact tables.
- Flat wide tables allowed in specific scenarios (e.g., data extracts).

#### Dimension Table Guidelines
- Prefix: `dim_` (e.g., `dim_contract`)
- Surrogate keys: incrementing integer named as `dim_<dimension name>_key`
- Include an "unknown row" (key = 0; date = 1899-01-01)
- NZ English spelling for all names and columns
- Mandatory metadata: `__LOAD_AT`, `__UPDATE_AT`, `__IS_LATEST`
- For type 2: `__VERSION`, `__START_AT` (default 1900-01-01 if unknown), `__END_AT` (default 2999-12-31 if unset), `__IS_ACTIVE`, `__CHANGE_HASH`

#### Fact Table Guidelines
- Prefix: `fact_` (e.g., `fact_incident`)
- All records should have the same grain.
- Metadata: `__LOAD_AT`, `__UPDATE_AT`
- Degenerate dimensions: allow business keys not matching dimension objects.
- Fact-less fact tables: for many-to-many relationships, without measures.
- Snapshot tables and summary tables: prefix with `snapshot_` or `summary_`

#### Views
- Prefixed as per the object they represent (e.g., `dim_`, `fact_`, `summary_`).
- Gold objects map directly to single Silver objects.

---

## Examples

### Table Naming Examples
- Source table: `assessment` → Bronze: `assessment`
- Non-specific source: `contract_type`
- Dimension: `dim_incident`
- Fact: `fact_contract`

### Bad Naming (Avoid)
- `assessments` (plural)
- `adj_reasons` (abbreviation and plural)
- `regionCode` (non-snake_case)
- `RegionCode` (camelCase)

### Metadata Column Example
```
customerkey
customer_code
customer_name
address
city
state
__EXTRACT_AT
__LOAD_AT
__UPDATE_AT
__START_AT
__END_AT
__IS_LATEST
__VERSION
__CHANGE_HASH
__SOURCE_FILE_NAME
```

### Surrogate Key Example
```
dim_camera_site_key | site_code | site_name
0                   | Unknown   | Unknown
10                  | S000004   | Waiuku Road
...
```

---

## Edge Cases

- When source columns are not named (e.g., CSV without headers), use snake_case and lowercase.
- If a transformation produces a new field (e.g., concatenated values), retain original source and store calculated value separately.
- Unknown dates: use 1899-01-01.
- Default start date for type 2 dimensions: 1900-01-01; default end date: 2999-12-31.

---

## Source

Source page version: 11
