#!/usr/bin/env python3
"""
Extract skills from HTML pages and emit Agent Skills directories.
"""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Optional, Tuple

from bs4 import BeautifulSoup

from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import UserMessage
from azure.core.credentials import AzureKeyCredential


def call_copilot_api(prompt: str = "", model: str = "openai/gpt-4.1") -> Optional[str]:
    """
    Call the GitHub Copilot API to extract a skill.
    """
    try:
        token = os.environ["GITHUB_TOKEN"]
        endpoint = "https://models.github.ai/inference"

        client = ChatCompletionsClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(token),
            api_version="2024-12-01-preview",
        )

        response = client.complete(
            messages=[
                {
                    "role": "developer",
                    "content": "You are a helpful assistant that extracts Agent Skills from documentation.",
                },
                UserMessage(prompt),
            ],
            model=model,
        )

        if response.choices:
            return response.choices[0].message.content
        print("Error calling Copilot API: No choices returned")
        return None
    except Exception as exc:
        print(f"Exception calling Copilot API: {exc}")
        return None


def extract_text_from_html(html_content: str) -> str:
    """
    Extract clean text from HTML content.
    """
    try:
        soup = BeautifulSoup(html_content, "html.parser")
        for script in soup(["script", "style"]):
            script.decompose()
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        return "\n".join(chunk for chunk in chunks if chunk)
    except Exception as exc:
        print(f"Error parsing HTML: {exc}")
        return html_content


def extract_title_from_html(html_content: str) -> str:
    """
    Extract the title from HTML, falling back to the first meaningful text line.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    heading = soup.find("h1")
    if heading and heading.get_text(strip=True):
        return heading.get_text(strip=True)
    text = extract_text_from_html(html_content)
    for line in text.splitlines():
        cleaned = line.strip()
        if cleaned:
            return cleaned
    return "Skill"


def slugify_name(name: str, page_id: str) -> str:
	"""
	Normalize a candidate name to a valid skill name.
	"""
	value = name.lower()
	value = re.sub(r"[^a-z0-9]+", "-", value)
	value = re.sub(r"-+", "-", value).strip("-")
	if not value:
		value = f"page-{page_id}"
	value = value[:64].strip("-")
	return value or f"page-{page_id}"


def suggest_skill_name(clean_text: str, title: str, page_id: str) -> str:
	"""
	Ask the model for a concise skill name and normalize it.
	"""
	preview = clean_text[:4000]
	prompt = f"""Suggest a short skill name for this content.

Rules:
- Output ONLY the name, no punctuation or extra words.
- Use lowercase letters, numbers, and hyphens only.
- 1-64 characters.
- Must not start or end with a hyphen.
- No consecutive hyphens.

Title: {title}
Content:
{preview}
"""

	suggestion = call_copilot_api(prompt)
	candidate = suggestion.strip() if suggestion else title
	normalized = slugify_name(candidate, page_id)
	if not is_valid_name(normalized):
		normalized = slugify_name(title, page_id)
	return normalized


def is_valid_name(name: str) -> bool:
	if not (1 <= len(name) <= 64):
		return False
	if "--" in name:
		return False
	return re.match(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", name) is not None


def parse_frontmatter(markdown: str) -> Tuple[Optional[dict], str]:
	lines = markdown.splitlines()
	if not lines or lines[0].strip() != "---":
		return None, markdown.strip()
	end_index = None
	for idx, line in enumerate(lines[1:], start=1):
		if line.strip() == "---":
			end_index = idx
			break
	if end_index is None:
		return None, markdown.strip()
	frontmatter_lines = lines[1:end_index]
	body_lines = lines[end_index + 1 :]
	data: dict = {}
	for line in frontmatter_lines:
		if ":" not in line:
			continue
		key, value = line.split(":", 1)
		data[key.strip()] = value.strip().strip('"')
	return data, "\n".join(body_lines).strip()


def read_skill_metadata(skill_path: Path) -> dict:
	"""
	Read metadata block from a SKILL.md frontmatter.
	"""
	try:
		lines = skill_path.read_text(encoding="utf-8").splitlines()
		if not lines or lines[0].strip() != "---":
			return {}
		end_index = None
		for idx, line in enumerate(lines[1:], start=1):
			if line.strip() == "---":
				end_index = idx
				break
		if end_index is None:
			return {}
		frontmatter_lines = lines[1:end_index]
		metadata: dict = {}
		in_metadata = False
		for line in frontmatter_lines:
			stripped = line.strip()
			if stripped == "metadata:":
				in_metadata = True
				continue
			if in_metadata:
				if not line.startswith(" "):
					in_metadata = False
					continue
				if ":" in stripped:
					key, value = stripped.split(":", 1)
					metadata[key.strip()] = value.strip().strip('"')
		return metadata
	except Exception:
		return {}


def find_existing_skill(skills_path: Path, page_id: str, version: str) -> Optional[Path]:
	"""
	Find an existing skill with matching source metadata.
	"""
	if not skills_path.exists():
		return None
	for skill_file in skills_path.glob("*/SKILL.md"):
		metadata = read_skill_metadata(skill_file)
		if not metadata:
			continue
		if metadata.get("source_page_id") == page_id and metadata.get("source_page_version") == version:
			return skill_file
	return None


def build_frontmatter(
	name: str,
	description: str,
	source_metadata: dict,
) -> str:
	description = description[:1024]
	metadata_lines = ["metadata:"]
	for key, value in source_metadata.items():
		metadata_lines.append(f"  {key}: \"{value}\"")

	return "\n".join(
		[
			"---",
			f"name: {name}",
			f"description: {description}",
			*metadata_lines,
			"---",
			"",
		]
	)


def build_fallback_description(title: str) -> str:
	return (
		f"Guidance for {title}. Use this skill when working on tasks related to {title.lower()} or when the user"
		" requests help with that topic."
	)


def extract_skill_from_html(
	clean_text: str,
	page_id: str,
	version: str,
	title: str,
) -> Tuple[str, str]:
	text_preview = clean_text[:1000000]
	suggested_name = suggest_skill_name(clean_text, title, page_id)

	prompt = f"""Create an Agent Skill from this content.

Return ONLY a valid SKILL.md file (no code fences) with YAML frontmatter and a Markdown body.

Frontmatter requirements:
- Must include name and description
- name must be 1-64 chars, lowercase letters/numbers/hyphens only, no leading/trailing hyphen, no consecutive hyphens
- description must explain what the skill does and when to use it
- Use this exact name unless it violates the rules: {suggested_name}

Body recommendations:
- Step-by-step instructions
- Examples
- Edge cases
- Include a short source section with: Source page version: {version}

Content to analyze:
{text_preview}
"""

	markdown = call_copilot_api(prompt)
	if not markdown:
		return suggested_name, generate_fallback_skill(title, suggested_name, version, page_id)

	frontmatter, body = parse_frontmatter(markdown)
	name = frontmatter.get("name") if frontmatter else None
	description = frontmatter.get("description") if frontmatter else None

	if not name or not is_valid_name(name):
		name = suggested_name

	if not description:
		description = build_fallback_description(title)

	source_metadata = {
		"source_page_id": page_id,
		"source_page_version": version,
		"source_page_title": title,
	}

	frontmatter_block = build_frontmatter(name, description, source_metadata)
	body = body or generate_fallback_body(title, version)

	return name, f"{frontmatter_block}{body}\n"


def generate_fallback_body(title: str, version: str) -> str:
	return (
		f"# {title}\n\n"
		"## Instructions\n\n"
		"1. Review the source content and extract actionable steps.\n"
		"2. Apply the steps to the user request.\n"
		"3. Confirm output matches the required format.\n\n"
		"## Examples\n\n"
		"- Input: User asks for help with the topic.\n"
		"- Output: Provide structured steps and references.\n\n"
		"## Edge Cases\n\n"
		"- Missing context in the source page.\n"
		"- Conflicting guidance between sections.\n\n"
		f"Source page version: {version}\n"
		"Detailed reference: [references/REFERENCE.md](references/REFERENCE.md)\n"
	)


def generate_fallback_skill(title: str, name: str, version: str, page_id: str) -> str:
	description = build_fallback_description(title)
	source_metadata = {
		"source_page_id": page_id,
		"source_page_version": version,
		"source_page_title": title,
	}
	frontmatter_block = build_frontmatter(name, description, source_metadata)
	body = generate_fallback_body(title, version)
	return f"{frontmatter_block}{body}\n"


def build_reference_markdown(title: str, version: str, reference_text: str) -> str:
	trimmed = reference_text[:200000]
	return (
		f"# {title} - Technical Reference\n\n"
		f"Source page version: {version}\n\n"
		"## Extracted Reference Content\n\n"
		f"{trimmed}\n"
	)


def process_pages_directory(
	pages_dir: str = "pages",
	skills_dir: str = "skills",
	output_dir: str = "temp_skills",
) -> None:
	pages_path = Path(pages_dir)
	skills_path = Path(skills_dir)
	output_path = Path(output_dir)
	output_path.mkdir(exist_ok=True)

	html_files = list(pages_path.glob("*.html"))
	print(f"Found {len(html_files)} HTML files to process")

	if not html_files:
		print("No HTML files found in pages directory")
		return

	for html_file in html_files:
		print(f"\nProcessing: {html_file.name}")

		try:
			with html_file.open("r", encoding="utf-8") as f:
				html_content = f.read()

			page_id = html_file.stem.split("page_", 1)[-1]
			title = extract_title_from_html(html_content)
			clean_text = extract_text_from_html(html_content)

			version = "N/A"
			version_line = next(
				(line for line in html_content.splitlines() if "<!-- Version:" in line),
				None,
			)
			if version_line:
				version = version_line.split("<!-- Version:")[1].split("-->")[0].strip()
				print(f"  - Detected version: {version}")
			else:
				print("  - No version info found")

			existing_skill = find_existing_skill(skills_path, page_id, version)
			if existing_skill:
				print(f"  - Existing skill found ({existing_skill}), skipping extraction")
				continue

			skill_name, skill_markdown = extract_skill_from_html(
				clean_text,
				page_id,
				version,
				title,
			)

			skill_dir = output_path / skill_name
			skill_dir.mkdir(parents=True, exist_ok=True)
			output_file = skill_dir / "SKILL.md"

			if output_file.exists():
				existing = output_file.read_text(encoding="utf-8")
				if f"source_page_version: \"{version}\"" in existing:
					print("  - Skill already up-to-date, skipping")
					continue

			output_file.write_text(skill_markdown, encoding="utf-8")
			print(f"  - Saved to: {output_file}")

			reference_dir = skill_dir / "references"
			reference_dir.mkdir(parents=True, exist_ok=True)
			reference_path = reference_dir / "REFERENCE.md"
			reference_path.write_text(
				build_reference_markdown(title, version, clean_text),
				encoding="utf-8",
			)
		except Exception as exc:
			print(f"  - Error processing {html_file.name}: {exc}")
			continue


if __name__ == "__main__":
	process_pages_directory()
	print("\n- All files processed!")
