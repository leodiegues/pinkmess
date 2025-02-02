@default:
    echo 'Hello, world!'

@lint:
    uv run ruff check . --fix

@render-vhs:
    ./scripts/render-vhs-tapes.sh