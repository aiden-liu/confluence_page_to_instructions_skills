# Confluence to Copilot Instructions and Skills

This repository syncs Confluence pages into GitHub Copilot instructions and Agent Skills. It uses GitHub Actions to fetch Confluence content, convert it into Markdown instructions or skill directories, and open update PRs automatically.

## What This Generates

- **Copilot instructions** in `instructions/` for task-specific guidance.
- **Agent Skills** in `skills/` with YAML frontmatter and optional references.

## Repository Layout

| Path | Purpose |
| ---- | ------- |
| [config.json](config.json) | Page list and conversion type (instructions or skills). |
| [instructions/](instructions/) | Generated `*.instructions.md` files. |
| [skills/](skills/) | Generated Agent Skill directories with `SKILL.md` + references. |
| [.github/scripts/](.github/scripts/) | Extraction and PR automation scripts. |
| [.github/workflows/](.github/workflows/) | GitHub Actions pipelines for fetch, extract, and PR creation. |
| [prompts/](prompts/) | Prompt used to generate Copilot instructions. |

## Current Instructions

| Title | Description |
| ----- | ----------- |
| [GitHub Actions](instructions/page_2364965145.instructions.md) | Instructions for using GitHub Actions. |
| [Branching Strategy](instructions/page_2664432312.instructions.md) | Trunk-based development with release branches on GitHub. |
| [Best Practices](instructions/page_3249143835.instructions.md) | Code review, repo audits, and knowledge sharing guidance. |
| [Secrets Usage](instructions/page_2745008174.instructions.md) | Key Vault and GitHub Actions secrets handling. |

## Current Skills

| Skill | Description |
| ----- | ----------- |
| [databricks-naming-modelling-guidelines](skills/databricks-naming-modelling-guidelines/SKILL.md) | Databricks naming, metadata, and modeling guidance. |
| [dip-development-standards](skills/dip-development-standards/SKILL.md) | DIP development standards across ADF and Databricks. |

## Workflows

| Workflow | Trigger | Outcome |
| -------- | ------- | ------- |
| [Fetch Confluence Pages](.github/workflows/fetch-confluence-pages.yml) | Manual or `config.json` change | Downloads Confluence pages into a `pages` artifact. |
| [Extract Instructions with Copilot](.github/workflows/extract-instructions.yml) | After fetch | Creates `temp_instructions` artifact. |
| [Extract Skills with Copilot](.github/workflows/extract-skills.yml) | After fetch | Creates `temp_skills` artifact. |
| [Create/Update Instruction PRs](.github/workflows/create-instruction-prs.yml) | After extract instructions | Commits updates and opens PRs. |
| [Create/Update Skill PRs](.github/workflows/create-skill-prs.yml) | After extract skills | Commits updates and opens PRs + skill zip artifacts. |
| [Fill PR Templates](.github/workflows/fill-pr-template.yml) | After PR creation | Auto-fills PR bodies using the template. |

## Configuration

Update [config.json](config.json) with Confluence page IDs and a `conversion_type`:

```json
{
	"pages": [
		{"id": "123456789", "version": "latest", "conversion_type": "instructions"},
		{"id": "987654321", "version": "latest", "conversion_type": "skills"}
	]
}
```

## Requirements

The workflows expect these GitHub settings:

- `CONFLUENCE_EMAIL` (repo variable)
- `CONFLUENCE_API_TOKEN` (repo secret)
- `GITHUB_TOKEN` (provided automatically in workflows)

> [!IMPORTANT]
> The extraction workflows call GitHub Models via `azure-ai-inference` using `GITHUB_TOKEN`. Ensure the token has `models: read` permissions in the workflow.

## Local Scripts

These scripts are used by the workflows and can be run locally with Python 3.11:

- [extract_instructions.py](.github/scripts/extract_instructions.py)
- [extract_skills.py](.github/scripts/extract_skills.py)
- [fill_pr_template.py](.github/scripts/fill_pr_template.py)
- [zip_skill_dir.py](.github/scripts/zip_skill_dir.py)

## Skill Authoring Reference

The Agent Skills format reference is stored in [create-skill.md](.github/instructions/create-skill.md).