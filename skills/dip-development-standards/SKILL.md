---
name: dip-development-standards
description: Provides comprehensive standards for development work on the Data Intelligence Platform (DIP). Use this skill to guide code management, branching, commit hygiene, CI/CD, infrastructure, code quality, reusability, and governance on Azure Data Factory and Databricks projects.
metadata:
  source_page_id: "4204199938"
  source_page_version: "1"
  source_page_title: "DIP - Development Standards"
---
# DIP Development Standards

This skill summarizes best practices and mandatory standards for engineering teams working on the Data Intelligence Platform (DIP), particularly within Azure Data Factory and Databricks environments. Follow these steps and recommendations for secure, auditable, and high-quality development.

## 1. Code Management

- Store ALL source code in Github Repos or an approved equivalent.
- Never keep production code only in Databricks workspaces or on local machines; workspaces must sync with repos.
- Large artefacts (data files, binaries, models) should be kept in blob storage and referenced, **not** committed to repos.

### Branching Strategy

- Use trunk-based branching with a long-lived main branch.
- Create feature branches for individual work items. Merge via Pull Request (PR).
- Branch names: lowercase, hyphens-separated, prefixed with work item IDs (e.g. `feature/ABC1234-add-ccs-data-pipeline`).

#### Branch Types

| Type        | Purpose                                | Example                                         |
|-------------|----------------------------------------|-------------------------------------------------|
| feature     | New features/enhancements               | feature/ABC1234-add-ccs-data-pipeline           |
| refactor    | Restructuring existing code             | refactor/DEF4321-move-ccs-to-sdp-pipelines      |
| bugfix      | Fixing non-critical bugs                | bugfix/GHI5678-fix-duplicate-customers          |
| hotfix      | Critical fixes for production           | hotfix/GHI8765-fix-hr-data-duplicates           |
| chore       | Non-functional tasks or dependencies    | chore/JKL9012-add-ccs-pipeline-docs             |
| perf        | Performance improvements                | perf/MNO1111-refine-job-cluster-config          |

## 2. Pull Requests & Code Reviews

- All merges to main must occur via PRs. Peer review required for material code changes.
- High-risk/production changes **must** always be reviewed.
- PRs must include links to relevant Jira tickets and documentation.
- Automated build/test pipelines run on PRs; merges blocked if tests fail.

## 3. Commit Hygiene

- One change per commit. Commit often and keep commits small.
- Use Conventional Commits format:
  - feat(scope): add access tables
  - fix(scope): resolve client-vehicle joins in silver
- Common types: feat, fix, chore, docs, refactor, test, style, perf, build.

#### Commit Examples

- `docs: correct spelling of CHANGELOG`
- `feat(cluster): add large job cluster template`
- `fix: deduplicate copper customers`

## 4. Security and Compliance

- **Never** store secrets, keys, or credentials in code; use Azure Key Vault and environment variables.
- Github repos require branch protection, mandatory PRs, and audit logging.
- Releases trace back to commit hash; jobs/pipelines record source commit in metadata.

## 5. Workspace Integration

- Databricks notebooks must be linked to repos and use the same branching/PR process.
- Refactor any production logic developed in ad-hoc notebooks into repos.

## 6. CI/CD Practices

- Automate all builds, tests, and deployments via Github Actions.
- No manual deployments or direct edits in production.
- CI/CD pipelines: build → test → security scan → package → deploy.
- Use Databricks Asset Bundles (DABs) for packaging/deployment.

### Environment Promotion

- Deployment sequence: Dev → Test → Prod, automated with approvals.
- DABs must define environment-specific configs.

### Security

- CI/CD pipelines must fail on security test failures.

## 7. Configuration & Secret Management

- Store all secrets in Azure Key Vault.
- Pipelines must securely retrieve secrets at runtime.

## 8. Infrastructure-as-Code (IaC)

- Use Terraform for provisioning clusters, networking, policies, etc.
- Validate templates in CI/CD; store Terraform state securely.
- Peer review all infrastructure changes.

## 9. Deployment Governance

- All production deployments require explicit approvals and ServiceNow change requests.
- Pipeline logs must capture approval and deployment data.
- Rollback mechanisms required.
- Deployment metadata must be catalogued.

## 10. Observability & Feedback

- Pipelines must emit telemetry (duration, failures, success).
- Alerts must trigger on build/test/deployment failures.
- Smoke tests and data quality checks run post-deployment.

## 11. Standardisation & Reuse

- Standardise CI/CD templates and DAB-based patterns across teams.
- Embed pipeline checks (linting, testing, observability) into shared templates.

## 12. Code Quality

- Follow NZTA coding guidelines for each language.
- Python: Use type hints, docstrings, avoid magic numbers.
- Notebooks: Separate SQL and Python; reusable logic in libraries.
- Run linting/static analysis automatically (flake8/pylint/black for Python).
- Structured logging (JSON/key-value), never log sensitive data.
- Error handling: Meaningful exceptions, retry policies for transient errors.
- All code must undergo peer review, including checks for tests and documentation updates.

## 13. Security by Design

- Scan code for vulnerabilities; prohibit unsafe functions (e.g., eval).
- Shared logic in libraries; functions/modules should be small and testable.

## 14. Performance

- Optimise Spark/Databricks code (partitioning, caching, avoid UDF misuse).
- Benchmark large transformations before production.

## 15. Reusability

- Extract common logic into shared libraries: team, domain, or organisation level.
- Version, document, and catalog libraries; use platform package management (PyPI, R repo).
- Build reusable components (ingestion, schema validation, monitoring).
- Use standard templates for pipelines, Terraform, DABs.
- Document all reusable assets; maintainers and deprecation policies required.

## 16. Edge Cases & Exceptions

- Large artefacts: Never commit to source; reference blob storage.
- Minor (low-risk/documentation) changes may bypass review if team-approved.
- Do **not** rewrite shared repo history (e.g., avoid force-push to main).
- Teams need NOT implement libraries in multiple languages—native language suffices.

## Examples

- Pull request workflow: Feature branch, PR with Jira link, automated tests, peer review, merge to main.
- Commit message: `fix(ccs): resolve double-counting in transactions`.
- Databricks notebook: Linked to repo, PR for production deployment.
- Terraform change: PR, CI/CD validates template, peer review, approved ServiceNow change.

## Source

Source page version: 1
