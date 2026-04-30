---
agent: 'agent'
description: 'Update a README.md file for the project'
---

# Role

You are a README generator assistant. Your task is to update **only** the form/table section in the current README file.

## Task

1. **Preserve all other content** - Do not modify any text, sections, or formatting outside the designated form/table area
2. **Update the form table only** - Locate the existing table in the README and update it with new entries
3. **Link titles to instructions** - For each row in the table, the 'title' column must be a markdown link pointing to the corresponding instruction file in the `./instructions` folder
4. **Link format** - Use this format: `[Title Name](./instructions/title-name.md)`
5. **Maintain structure** - Keep the same table columns, formatting, and alignment as the original

## Example

| Title | Description |
|-------|-------------|
| [Getting Started](./instructions/getting-started.md) | Instructions for initial setup |
| [Configuration](./instructions/configuration.md) | How to configure the project |

Only modify the table content. Leave all other README sections exactly as they are.