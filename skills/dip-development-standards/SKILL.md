---
name: dip-development-standards
description: Defines standards and best practices for code management, CI/CD, deployment, and quality assurance on the Data Intelligence Platform (DIP). Use this skill to structure development on Azure Data Factory, Databricks, and related environments for secure, reproducible, and auditable engineering workflows.
metadata:
  source_page_id: "4204199938"
  source_page_version: "1"
  source_page_title: "DIP - Development Standards"
---
# DIP Development Standards

This skill guides agents and teams on the agreed standards for developing, managing, deploying, and reviewing code on the Data Intelligence Platform (DIP), including Azure Data Factory and Databricks. Use this skill whenever engineering or analytics work involves DIP assets, ensuring compliance, security, and traceability.

## Step-by-Step Instructions

### 1. Source Control and Code Management

- **Store all source code in Github Repos** (or a NZTA-approved equivalent).
- **Never keep production code isolated in Databricks workspaces or local machines.** Databricks notebooks must be linked to repos.
- **Do not commit large artefacts (data files, models) to source control.** Store them in approved blob storage and reference from code.

### 2. Branching Strategy

- **Follow trunk-based branching:** Maintain a long-lived `main` branch for production.
- **Create feature branches** for individual work items. Merge via pull requests (PRs).
- **Branch naming:**
  - Prefix with work item ID (e.g., `feature/JIRA-5678-add-ccs-pipeline`).
  - Use lowercase letters and hyphens; exceptions allowed for Jira IDs.
- **Branch types:**
  - `feature/` for new features
  - `refactor/` for restructuring
  - `bugfix/` for non-critical fixes
  - `hotfix/` for urgent fixes
  - `chore/` for non-functional tasks
  - `perf/` for performance improvements

### 3. Pull Requests and Code Reviews

- **All merges to main via PRs.**
- **Peer review required** for all material code changes.
- **Minor, low-risk updates** (e.g., documentation) may skip review if agreed.
- **PRs must include links** to Jira items and documentation.
- **Automated build/test pipelines** must run on PRs; merges blocked if tests fail.

### 4. Commit Hygiene

- **One change per commit; frequent commits.**
- **Commit messages:**
  - Follow [Conventional Commits](https://www.conventionalcommits.org/).
  - Prefix with type: `feat`, `fix`, `chore`, `docs`, `refactor`, `test`, `style`, `perf`, `build`.
- **Examples:**
  - `feat(ccs): add access tables`
  - `fix(tm): resolve client-vehicle joins`
  - `docs: update README`
- **Squash or rebase private branches only, never rewrite shared history.**

### 5. Security and Compliance

- **No secrets, keys, credentials in code.** Use Azure Key Vault and env variables.
- **Github repos:** Enable branch protection, PR requirement, audit logging.
- **Production releases:** Trace back to commit hash; all jobs/pipelines must record source commit.

### 6. Workspace Integration

- Refactor production logic from Databricks notebooks into repos.
- Notebooks must follow branching/PR process.

### 7. CI/CD Practices

- **Automate builds, tests, deployments** with Github Actions; no manual production edits.
- **Standard pipeline stages:** build → test → security scan → package → deploy.
- **Databricks deployments use DAB** (Databricks Asset Bundles) for jobs/flows.
- **Promote changes Dev → Test → Prod** via automated processes and approvals.

### 8. Security in CI/CD

- Static/dynamic security scanning.
- Dependency vulnerability checks.
- Secret detection; fail pipelines on security issues.

### 9. Configuration and Secret Management

- Store all secrets in Azure Key Vault.
- DAB must use injected secrets for configs.

### 10. Infrastructure-as-Code (IaC)

- Provision all platform infra (clusters, policies) with Terraform.
- Secure, version-control Terraform state.
- Peer review all infra changes; automate validation and deployment.

### 11. Deployment Governance

- Explicit approval for production deployments.
- ServiceNow change requests required for each deployment.
- Logs must capture deployment metadata and approvers.
- Rollback mechanisms must always exist.

### 12. Observability

- Pipelines emit telemetry (duration, failures, success).
- Automatic alerts for build/test/deploy failures.
- Smoke tests/data quality checks run post-deployment.

### 13. Code Quality

- **Follow NZTA coding guidelines** for each language.
- Python: Type hints, docstrings, avoid magic numbers, use config params.
- **Linting and static analysis**: Fail builds on critical issues.
- **Structured logging:** Use JSON/key-value, never log sensitive data.
- **Error handling:** Catch and log exceptions; retry policies for transient fails.
- **Peer reviews:** Assess readability, correctness, security, and maintainability.
- **Security by design:** Scan dependencies/code, prohibit unsafe patterns (e.g., no `eval`).

### 14. Reusability

- Shared libraries for common logic; versioned and documented.
- Team/domain/org-level scope as appropriate; stricter governance at org-level.
- Standard templates for CI/CD, IaC, Databricks bundles.
- Assets catalogued in SharePoint and Confluence; Unity Catalog links datasets to reusable logic.

## Examples

- **Branch name:** `feature/ABC1234-add-ccs-data-pipeline`
- **Commit message:** `fix: deduplicate copper customers`
- **Pull request:** Links to Jira work and documents, passes automated tests, reviewed by peer.

## Edge Cases

- **Work item IDs may use uppercase letters** in branch names as exception.
- **Minor doc/meta changes** may merge without review if team agrees criteria.
- **Never squash or rebase public branches**; impacts traceability.
- **Ad-hoc notebooks allowed for exploration,** but production logic must move to repos.

## Source

Source page version: 1
