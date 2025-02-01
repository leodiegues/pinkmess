@default:
    echo 'Hello, world!'

@lint:
    uv run ruff check . --fix
