from pydantic_ai import Agent

from pinkmess.agents.common import extract_note_text
from pinkmess.config import settings
from pinkmess.note import Note


note_tag_suggestion_agent = Agent(
    model=settings.llm_model,
    model_settings=settings.llm_settings,
    deps_type=Note,
    result_type=list[str],
    tools=[extract_note_text],
    system_prompt=(
        "Based on this markdown text, extract useful tags so "
        "I can search for this text later. The key point is "
        "that the I can add them to a markdown file YAML frontmatter. "
        "Answer only with the list of tags in the same language as the text "
        "separated by comma. Avoid spaces between commas. If the "
        "tag has more than one word, separate the words with hyphens."
    ),
)
