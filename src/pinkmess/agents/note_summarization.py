from pydantic_ai import Agent

from pinkmess.agents.common import extract_note_text
from pinkmess.config import settings
from pinkmess.note import Note


note_summarization_agent = Agent(
    model=settings.llm_model,
    model_settings=settings.llm_settings,
    deps_type=Note,
    result_type=str,
    tools=[extract_note_text],
    system_prompt=(
        "Based on this note text, generate a one paragraph summary in the same "
        "language as the note that faithfully, conciselly and comprehensively "
        "summarizes it's content. The summary should be self-contained. "
        "Answer only with the summary paragraph, nothing else."
    ),
)
