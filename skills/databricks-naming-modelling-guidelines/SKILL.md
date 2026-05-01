---
name: databricks-naming-modelling-guidelines
description: Guidelines for naming conventions, metadata columns, and modeling approaches in the Databricks area of the Data Intelligence Platform. Use this skill when designing, naming, or modeling datasets within Databricks, ensuring consistency and adherence to NZTA standards.
metadata:
  source_page_id: "4095672332"
  source_page_version: "11"
  source_page_title: "DIP - Databricks Naming & Modelling Guidelines"
---
# Databricks Naming & Modelling Guidelines

These guidelines ensure consistent naming, metadata management, and modeling across Databricks within NZTA’s Data Intelligence Platform. They are intended for anyone performing data engineering or modeling in Databricks.

## 1. General Guidelines

- **Metadata timestamps:** Always use UTC for metadata columns (e.g., load time, update time) to prevent confusion with time zones or daylight savings.
- **Snake case:** Prefer `snake_case` for naming, except when object names derive directly from a source system.
- **No plurals or abbreviations:** Avoid plurals and nonstandard abbreviations in table and column names.

## 2. Metadata Columns

- Prefix metadata columns with double underscores, and use all uppercase (e.g., `__LOAD_AT`).
- Key columns for metadata tracking include:
  - `__EXTRACT_AT` (timestamp, mandatory): When data was extracted (UTC)
  - `__LOAD_AT` (timestamp, mandatory): When data was loaded (UTC)
  - `__RECORD_SOURCE` (string, mandatory): Source or filename of record
  - Others, as required: `__SOURCE_FILE_PATH`, `__SEQUENCE_NUMBER`, `__EXTRACT_RUN_ID`, `__RESCUED_DATA`

| Column             | Type      | Mandatory | Notes                                                |
|--------------------|-----------|-----------|------------------------------------------------------|
| __EXTRACT_AT       | timestamp | Y         | Extraction time (UTC)                                |
| __LOAD_AT          | timestamp | Y         | Load time (UTC)                                      |
| __RECORD_SOURCE    | string    | Y         | Record/source identifier                             |
| __SOURCE_FILE_PATH | string    | N         | Path to source file                                  |
| __SEQUENCE_NUMBER  | integer   | N         | Used for tracking duplicates/logs                    |
| __EXTRACT_RUN_ID   | string    | N         | Pipeline run ID                                      |
| __RESCUED_DATA     | string    | N         | Only for streaming tables                            |

## 3. Table & Column Naming

### Bronze Layer (Raw Source)
- Table names match the source object/file (lowercase enforced).
- If source lacks a specific name, use snake_case. Example: `assessmentcontracttype`.
- Keep column names as per source (including case), unless absent, then use snake_case.
- Do not use plurals/abbreviations (e.g., avoid `assessments`, `adj_reasons`).

### Copper Layer (Historized Source)
- Table and column names match source. Minimal business rules/calculations.
- Track all changes (SCD2). Recommended to use Lakeflow Declarative Pipelines.
- Add metadata columns like `__START_AT`, `__END_AT`.

### Silver Layer (Business Modeling)
- Tables: `silver_[business_area]` (e.g., `silver_purchasing`), add `_stg_` prefix if staging.
- Use snake_case for both objects and columns.
- Rename columns for business clarity (e.g., `contract_name` not `name`).
- Avoid system-specific/non-standard abbreviations.
- Flags: Use `boolean` type, prefix with `is_` or `has_`.
- Spelling: Use NZ English (e.g., `centre`, not `center`).

### Gold Layer (Analytical)
- Star schema is preferred for analytical modeling.
- Table prefixes:
  - Dimensions: `dim_`
  - Facts: `fact_`
  - Snapshots: `snapshot_`
  - Summaries: `summary_`
- Surrogate keys: `dim_<dimension>_key` (e.g., `dim_camera_site_key`).
- Unknown row: Add default unknown row for dimensions (`0` for integer, `Unknown` for string).

## 4. Column Suffixes

- For date/time columns, use clear suffixes: `_date`, `_datetime`, `_time`, `_datetime_utc`.
- Business dates/times: Store in NZ Standard Time unless specified as UTC.

## 5. Edge Cases

- **Log files/unstructured data:** Add row numbers and use metadata columns to manage duplicates or variable formats.
- **Role-playing dimensions:** Use views for date dimensions playing multiple roles.
- **Fact-less fact tables:** Use for many-to-many relationships; these have no measures.

## 6. Example Naming Conventions

**Dimension Table:**

```
dim_camera_site_key
site_code
site_name
stage_start_datetime
stage_end_datetime
__LOAD_AT
__UPDATE_AT
__START_AT
__END_AT
__IS_ACTIVE
__IS_LATEST
__CHANGE_HASH
```

**Fact Table:**

```
fact_incident_stage_history
incident_id
stage_code
stage_name
stage_start_datetime
stage_end_datetime
dim_incident_key
dim_stage_key
__LOAD_AT
__UPDATE_AT
```

**Metadata Columns:**

```
__EXTRACT_AT
__LOAD_AT
__RECORD_SOURCE
```

**Date Dimension Example:**

```
dim_date
date_key (YYYYMMDD)
date
month
year
week
__LOAD_AT
```

## 7. Source

Source page version: 11
