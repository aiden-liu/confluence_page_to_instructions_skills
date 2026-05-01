---
name: dip-development-standards
description: Provides development standards for the Data Intelligence Platform (DIP), covering code management, branching, commit hygiene, CI/CD, security, code quality, and reusability. Use this skill to ensure engineering work on DIP is consistent, auditable, secure, and optimised across Azure Data Factory and Databricks environments.
metadata:
  source_page_id: "4204199938"
  source_page_version: "1"
  source_page_title: "DIP - Development Standards"
---
# DIP Development Standards Agent Skill

This skill guides data and platform engineers, data analysts, and scientists on best practices and required standards for development work on the Data Intelligence Platform (DIP), specifically for Azure Data Factory (ADF) and Databricks. It ensures code is managed, deployed, and maintained in a secure, auditable, and standardised way.

## Step-by-Step Instructions

1. **Code Management**
   - Store all code in Github Repos (or approved equivalents).
   - No production code may be kept solely in Databricks workspaces or local machines.
   - Workspace notebooks must be source-controlled via repo integration.
   - Large artefacts (data, models, binaries) must not be committed; use blob storage and reference them.

2. **Branching Strategy**
   - Use trunk-based branching with a long-lived main branch.
   - Feature branches are for individual work items, merged via pull requests.
   - Branch names must be descriptive and prefixed with a work item ID (e.g., `feature/JIRA-5678-add-pipeline`).
   - Use lowercase letters and hyphens for branch names (except Jira IDs).
   - Branch types and prefixes:
     - `feature/` – New features/enhancements
     - `refactor/` – Restructuring without new features
     - `bugfix/` – Non-critical bug fixes
     - `hotfix/` – Critical fixes direct to production
     - `chore/` – Non-functional tasks
     - `perf/` – Performance improvements

3. **Pull Requests & Code Reviews**
   - All merges to main occur via pull requests.
   - Peer review is required for material code changes.
   - Minor, low-risk updates may skip peer review if agreed by teams.
   - PRs must link relevant Jira work items and documentation.
   - Automated build/test pipelines must run on PRs; merges blocked if tests fail.

4. **Commit Hygiene**
   - One change per commit; avoid multi-purpose commits.
   - Commit frequently and use clear, descriptive messages.
   - Follow Conventional Commits specification:
     - Prefix: `feat`, `fix`, `chore`, `docs`, `refactor`, `test`, `style`, `perf`, `build`
     - Example: `feat(cluster): add job cluster template`
   - Never rewrite shared history; squash/rebase allowed on private branches.

5. **Security & Compliance**
   - Do not store secrets, keys, or credentials in code.
   - Use Azure Key Vault and environment variables.
   - Branch protection, mandatory PRs, and audit logging required in Github.

6. **Reproducibility & Traceability**
   - Every production release must trace to a commit hash.
   - Jobs/pipelines record commit hash in metadata.
   - Tag and version code for significant releases.

7. **Workspace Integration**
   - Databricks notebooks must be linked to repos and follow branch/PR processes.
   - Exploration notebooks must be refactored before deploying to production.

8. **CI/CD Practices**
   - Automate all builds, tests, and deployments with Github Actions.
   - Pipelines: build → test → security scan → package → deploy.
   - Use Databricks Asset Bundles (DAB) for packaging/deployment.
   - Progress changes through Dev → Test → Prod automatically.
   - Embed static/dynamic security scans, dependency vulnerability scanning, and secret checks.
   - Store all secrets in Azure Key Vault; retrieve at runtime.

9. **Infrastructure-as-Code (IaC)**
   - Use Terraform for all platform infrastructure.
   - Validate templates via CI/CD before deployment.
   - Peer review and trace IaC changes; store Terraform state securely.

10. **Deployment Governance**
    - Require explicit approval from authorised reviewers for production deployments.
    - Log approved ServiceNow change requests.
    - Pipeline logs capture approval metadata.
    - Build rollback mechanisms for all deployments.

11. **Observability & Feedback**
    - Pipelines emit telemetry for build/deployment success/failure.
    - Alerts trigger on failures.
    - Run post-deployment validations (smoke tests, data quality checks) automatically.

12. **Standardisation & Reuse**
    - CI/CD templates, YAML bundles, and DAB-based patterns are standardised and reused.
    - Share common pipeline checks in templates.

13. **Code Quality**
    - Adhere to agreed NZTA coding guidelines.
    - Python: use type hints and docstrings.
    - Separate SQL and Python in notebooks; reusable logic in libraries.
    - Avoid magic numbers; use configuration parameters.
    - Automatic linting/static analysis in CI/CD (flake8, pylint, black for Python).
    - Structured logging (JSON/key-value), avoid logging sensitive data.
    - Handle errors gracefully, show clear logs, and implement retries.
    - Peer review for all code merges—check for readability, maintainability, security, documentation, and tests.

14. **Reusability & Modularity**
    - Move reusable logic to libraries, not duplicated in pipelines.
    - Version and document all libraries for reuse.
    - Benchmark, optimise, and refactor inefficient Spark queries.

15. **Discoverability & Documentation**
    - Catalogue all reusable assets in SharePoint (process) and Confluence (technical).
    - Link Unity Catalog datasets to transformations/libraries.
    - Include documentation on purpose, dependencies, versioning, and usage.

16. **Governance & Maintenance**
    - Assign owners/maintainers to reusable assets.
    - Apply deprecation policies and migration guidance.
    - Review assets periodically for compliance, security, relevance.

## Examples

- **Branch Naming:**  
  `feature/ABC1234-add-data-pipeline`  
  `bugfix/GHI5678-fix-duplicate-customers`

- **Commit Messages:**  
  `docs: correct spelling of CHANGELOG`  
  `feat(cluster): add large job cluster template`  
  `fix: deduplicate copper customers  
  Deduplicated customer table causing false negatives.  
  Refs: ABC-1234`

- **PR Requirements:**  
  Include relevant Jira links, documentation, and run build/test/scan stages.

## Edge Cases

- Large files or models must NOT be committed—use blob storage.
- Minor documentation changes may skip peer review if team-approved.
- Do not rewrite shared git history after PR merges.
- Never store secrets in code or Github variables; use Key Vault always.
- Multiple changes must be made as separate commits and PRs.

## Source

Source page version: 1
