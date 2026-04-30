---
name: databricks-naming-modelling-guidelines
description: Provides standardized naming conventions and data modelling guidelines for Databricks in NZTA's Data Intelligence Platform. Use this skill when designing, naming, and structuring tables, columns, and metadata in Databricks to ensure clarity, consistency, and alignment with organizational practices across bronze, copper, silver, and gold data layers.
metadata:
  source_page_id: "4095672332"
  source_page_version: "11"
  source_page_title: "DIP - Databricks Naming & Modelling Guidelines"
---
# Databricks Naming & Modelling Guidelines Agent Skill

## Purpose

This skill provides step-by-step guidelines for naming tables, columns, metadata fields, and modelling data in Databricks within the NZTA Data Intelligence Platform. It is intended for data engineers and data modellers to ensure best practices and consistency across data layers.

## Step-by-Step Instructions

### General Principles

- **Applicable To:** Databricks data modelling and engineering only (not PowerBI or Azure Data Factory).
- **Casing:** Prefer `snake_case` (lowercase, underscores) for table and column names, except when based directly on the source system.
- **Avoid:** Plurals and abbreviations (unless commonly understood).
- **Metadata Columns:** All timestamps must be in UTC.

---

### Bronze Layer

- **Purpose:** Store raw data, closely matching the source.
- **Schemas:** Use source-based schemas (e.g., bronze_[source]).
- **Table Naming:**
  - Use the source table/file name if available.
  - All names in lowercase.
    - Examples: `assessmentcontracttype`, `h_contract`, `area_of_interest`, `fault_linkedevent`.
  - If no source name, use `snake_case`: 
    - Examples: `contract_type`, `infringement_notice`, `adjudication_reason`.
  - **Do NOT use plurals or abbreviations.**  
- **Column Naming:**
  - Keep column names as per source, including casing.
  - If source has no header: use `snake_case`.
- **Metadata Columns:**
  - Prefix all metadata columns with two underscores (`__`) and use UPPER CASE.
    - Examples:
      - `__EXTRACT_AT` (Mandatory, timestamp, extraction date)
      - `__LOAD_AT` (Mandatory, timestamp, loaded to Databricks, in UTC)
      - `__RECORD_SOURCE` (Mandatory, string, source/filename)
      - Other optional fields: `__SOURCE_FILE_PATH`, `__SEQUENCE_NUMBER`, `__EXTRACT_RUN_ID`, `__RESCUED_DATA`.
- **Partition Columns:** Example:
  - `customer_key`, `customer_code`, `customer_name`, `address`, `city`, `state`, `__EXTRACT_AT`, `__LOAD_AT`, `__SOURCE_FILE_NAME`

---

### Copper Layer

- **Purpose:** Historized copy of source; performs like SCD2.
- **Schemas:** Use copper_[source].
- **Naming Conventions:** Match source table and column names.
- **Metadata Columns:** All timestamps in UTC.
  - `__EXTRACT_AT` (Mandatory, inherited from bronze)
  - `__LOAD_AT` (Mandatory, inherited from bronze)
  - `__UPDATE_AT`, `__START_AT`, `__END_AT`, `__SOURCE_FILE_NAME`
- **Calculations:** Minimal, e.g., data type conversions, hashing business key, handling duplicates, assigning row numbers.
- **Example of metadata in copper tables:**
  - `customer_key`, `customer_code`, ... `__EXTRACT_AT`, `__LOAD_AT`, `__UPDATE_AT`, `__START_AT`, `__END_AT`, `__IS_LATEST`, `__VERSION`, `__CHANGE_HASH`, `__SOURCE_FILE_NAME`
- **Edge Case:** For log files with variable columns, assign row numbers for easier management.

---

### Silver Layer

- **Purpose:** Combine, transform, and normalize data for business usage.
- **Table Naming:**
  - Prefix with `silver_[business_area]`, e.g., `silver_purchasing`.
  - For staging objects, prefix with `_stg_`.
  - Avoid plurals and use snake_case.
- **Column Naming:**
  - May rename columns for clarity, context, and business terms (not just using 'name').
    - Example: Rename `name` to `contract_name`.
  - Use meaningful names, avoid requiring table name context.
- **Abbreviations:** Only if commonly used and clear to non-experts.
- **Flags:** Use boolean with prefixes `is_` or `has_`.
  - Examples: `is_site_enforcing`, `is_resolved`, `has_enforcing_stage`
- **Spelling:** Use NZ English.
- **Date/Time Fields:** 
  - Use clear suffixes: `_date`, `_datetime`, `_time`, `_utc`.
  - Business dates/times in NZ Standard Time unless otherwise specified.

---

### Gold Layer

- **Purpose:** Model data for analytics, BI, and reporting (star schema recommended).
- **Table Naming:**
  - Dimensions: Prefix with `dim_`, e.g., `dim_contract`
  - Facts: Prefix with `fact_`, e.g., `fact_incident_stage_history`
  - Snapshot: Prefix with `snapshot_`, e.g., `snapshot_sales_by_month`
  - Summary: Prefix with `summary_`, e.g., `summary_sales_by_month`
- **Dimension Tables:**
  - Must have a surrogate key: `dim_<dimension name>_key`
    - Example: `dim_camera_site_key`
  - Include an "unknown" row with surrogate key 0.
  - For date dimensions, use `YYYYMMDD` as key and default date `1899-01-01` for unknowns.
  - Metadata columns include: `__LOAD_AT`, `__UPDATE_AT`, `__VERSION`, `__START_AT` (`1900-01-01` default), `__END_AT` (`2999-12-31` default), `__IS_ACTIVE`, `__IS_LATEST`, `__CHANGE_HASH`.
- **Fact Tables:**
  - Prefix with `fact_`.
  - Granularity: Ensure all records have same grain.
  - Metadata columns: `__LOAD_AT`, `__UPDATE_AT`.
  - Business/natural keys not required unless needed for filtering; consider views if necessary.
  - Fact-less fact tables allowed (no measures).
- **Views:** Follow naming conventions of primary object.

---

## Examples

- **Bronze Table:** `bronze_pace.assessmentcontracttype` (raw, matches source name)
- **Copper Table:** `copper_pace.customer_code` (historized, matches source name)
- **Silver Table:** `silver_sales.contract_name`
- **Gold Dimension:** `dim_camera_site` with surrogate key `dim_camera_site_key`; unknown row has key 0, unknown data defaults.
- **Fact Table:** `fact_contract` with grain defined as "one row per contract event".

---

## Edge Cases

- **Source File with No Headers:** Use snake_case for column names.
- **Log Files:** Assign row numbers to manage non-uniform structure.
- **Daylight Savings Time:** Always store metadata timestamps in UTC.
- **Unknown Keys/Values:** Provide an "unknown" row with default values in dimension tables.

---

## Source

Source page version: 11
