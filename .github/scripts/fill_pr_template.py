#!/usr/bin/env python3
"""
Fill a PR template using GitHub Models when available.
"""

from __future__ import annotations

import argparse
import os
from typing import Optional

from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import UserMessage
from azure.core.credentials import AzureKeyCredential


def call_copilot(prompt: str, token: str) -> Optional[str]:
    client = ChatCompletionsClient(
        endpoint="https://models.github.ai/inference",
        credential=AzureKeyCredential(token),
        api_version="2024-12-01-preview",
    )
    response = client.complete(
        messages=[
            {
                "role": "developer",
                "content": "You fill PR templates for documentation changes.",
            },
            UserMessage(prompt),
        ],
        model="openai/gpt-4.1",
    )
    if response.choices:
        return response.choices[0].message.content
    return None


def build_prompt(template: str, content: str, doc_type: str) -> str:
    return f"""Fill out this PR template for {doc_type} updates. Use the content as the source of truth.

Rules:
- Return ONLY the filled template in Markdown.
- Check the most relevant boxes with an "x".
- Keep sections brief and specific.
- Use bullet points where appropriate.

Template:
{template}

Content:
{content}
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Fill PR template with LLM.")
    parser.add_argument("--template", required=True, help="Path to PR template")
    parser.add_argument("--content", required=True, help="Path to content file")
    parser.add_argument("--output", required=True, help="Path to output file")
    parser.add_argument("--doc-type", required=True, help="instructions or skills")
    args = parser.parse_args()

    template = open(args.template, "r", encoding="utf-8").read()
    content = open(args.content, "r", encoding="utf-8").read()

    token = os.environ.get("GITHUB_TOKEN")
    body = None
    if token:
        try:
            prompt = build_prompt(template, content, args.doc_type)
            body = call_copilot(prompt, token)
        except Exception:
            body = None

    if not body:
        body = template

    with open(args.output, "w", encoding="utf-8") as handle:
        handle.write(body)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
