---
name: dip-development-standards
description: Defines and enforces development standards for the Data Intelligence Platform (DIP), including source control, code quality, CI/CD, security, and reusability. Use this skill to ensure development work meets platform best practices across Azure Data Factory and Databricks.
metadata:
  source_page_id: "4204199938"
  source_page_version: "1"
  source_page_title: "DIP - Development Standards"
---
# DIP Development Standards Skill

This skill provides step-by-step guidance for applying development standards on the Data Intelligence Platform (DIP), supporting engineers and analysts working on Azure Data Factory (ADF) and Databricks. Use this skill when building, reviewing, or deploying code, pipelines, and shared components for any DIP environment.

## Step-by-Step Instructions

### 1. Source Control

- **Store all code** in GitHub Repos (or approved equivalents).
- **Integrate workspace notebooks** with repos; production code must not reside solely in Databricks, notebooks, or local machines.
- **Do NOT commit large artefacts** (data files, models, binaries); store them in approved blob storage and reference as needed.

### 2. Branching Strategy

- Use a **trunk-based model** with a long-lived main (production) branch.
- Create feature branches for individual work items; merge via pull requests (PRs).
- **Branch names:**  
  - Prefix with work item ID (e.g., `feature/JIRA-5678-add-ccs-pipeline`).
  - Use lowercase and hyphens except for Jira IDs.
  - Be specific (e.g., `fix-ccs-quarantine-error`).

#### Branch Types Explained

| Type       | Purpose                                    | Example                                      |
|------------|--------------------------------------------|----------------------------------------------|
| Feature    | New features/enhancements                  | feature/ABC1234-add-ccs-data-pipeline        |
| Refactor   | Restructuring code                         | refactor/DEF4321-move-ccs-to-sdp-pipelines   |
| Bugfix     | Non-critical bug fixes                     | bugfix/GHI5678-fix-duplicate-customers       |
| Hotfix     | Critical fixes for production              | hotfix/GHI8765-fix-hr-data-duplicates        |
| Chore      | Dependencies/docs/non-functional updates    | chore/JKL9012-add-ccs-pipeline-docs          |
| Perf       | Performance improvements                   | perf/MNO1111-refine-job-cluster-config       |

### 3. Pull Requests & Code Reviews

- All merges to main must occur via pull requests.
- **Peer review** is required for material code changes; minor doc/metadata edits may bypass review per team criteria.
- PRs must include links to relevant Jira items and documentation.
- PRs must trigger automated build/test pipelines; merges are blocked if tests fail.

### 4. Commit Hygiene & Message Standards

- **One change per commit**; avoid bundling multiple changes.
- **Frequent commits** help document the project history.
- Follow **Conventional Commits** (prefixes like feat, fix, chore, docs, refactor, test, style, perf, build).
  - Example: `feat(ccs): add access tables`

#### Commit Examples

- Without body: `docs: correct spelling of CHANGELOG`
- With scope: `feat(cluster): add large job cluster template`
- With multi-paragraph body/footers:
  ```
  fix: deduplicate copper customers

  Deduplicated copper customer table as it was causing false negatives...
  Refs: ABC-1234
  ```

### 5. Security & Compliance

- **No secrets, keys, or credentials in code**; use Azure Key Vault and environment variables.
- All repos must have branch protections, mandatory PRs, and audit logging.

### 6. Reproducibility & Traceability

- Production releases must trace to specific commit hashes.
- Production jobs/pipelines record their source commit in metadata.
- Significant releases must be tagged and versioned.

### 7. Workspace Integration

- Notebooks must link to repos and follow same branching/PR process.
- Exploratory notebooks may be used, but production logic must be refactored into repos.

### 8. CI/CD Practices

- All builds, tests, and deployments are automated via Github Actions.
- Pipelines must run stages: build → test → security scan → package → deploy.
- Use Databricks Asset Bundles (DABs) for asset packaging/deployment.

#### Environment Promotion

- Progress changes through Dev → Test → Prod with automated approvals.
- DABs define environment-specific configurations for consistency.

#### Security Controls

- CI/CD must fail on security test failures; no overrides allowed.

#### Secret Management

- Store all secrets in Azure Key Vault; retrieve securely at runtime.

#### Infrastructure-as-Code

- Manage infrastructure exclusively with Terraform (linting, peer review, automated state management).

#### Deployment Governance

- Explicit approvals required for production deployments.
- ServiceNow change requests must be logged/closed for production.
- Rollback mechanisms are required; deployment metadata must be captured.

#### Observability

- Pipelines emit telemetry on duration, failures, and deployment success.
- Alerts trigger for failed builds/tests/deployments.
- Post-deployment validations run automatically.

### 9. Code Quality

- Conform to NZTA coding guidelines for each language.
- Python: use type hints and docstrings; no magic numbers/hard-coded values.
- Notebooks: separate SQL/Python cells, refactor reusable logic.
- Linting/static analysis via CI/CD (flake8, pylint, black).
- Logs are structured (JSON/key-value); never log sensitive data.
- Handle errors gracefully with meaningful messages; implement retries for transient errors.
- Peer review assesses correctness, readability, maintainability, and security.

### 10. Reusability

- Extract shared logic into libraries/components; avoid duplication.
- Version, document, and catalogue all reusable assets.
- Use standard templates and patterns for pipelines, Terraform, DABs.
- Assets catalogued in SharePoint (process/governance) and Confluence (technical).
- Owners/maintainers must be defined; apply deprecation policies to outdated assets.

## Examples

- **Branch name:** `feature/ABC1234-add-ccs-data-pipeline`
- **Commit message:** `fix(tm): resolve client-vehicle joins in silver`
- **Deployment process:** Use Github Actions, automated environment promotion, explicit approvals, rollbacks, and metadata capture.

## Edge Cases

- Minor documentation can bypass peer review only if agreed by team.
- Existing shared libraries/components must be checked for before building new ones.
- For cross-language assets, native language ecosystem suffices (e.g., Python or R, not both).
- No production deployments without ServiceNow change request and explicit approvals.

## Source

Source page version: 1
Detailed reference: [references/REFERENCE.md](references/REFERENCE.md)
