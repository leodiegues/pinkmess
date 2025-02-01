from pydantic_ai import RunContext

from pinkmess.note import Note


def extract_note_text(ctx: RunContext[Note]) -> str:
    """
    Extracts the text from a note.
    """
    note = ctx.deps

    if note.content is None:
        note.load()

    text = note.content or ""

    if not text:
        raise ValueError("Note content is empty.")

    return text


def edit_markdown_frontmatter(ctx: RunContext[str]) -> str:
    """
    Edits the markdown frontmatter.
    """
    text = ctx.deps
    return text
