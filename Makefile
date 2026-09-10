.PHONY: test paper lint install clean

install:
	python3 -m venv .venv && .venv/bin/pip install pydantic pytest pytest-asyncio --quiet

test:
	@echo "Running Reality Anchor tests..."
	.venv/bin/pytest tests/ -v --tb=short 2>&1
	@echo "If tests pass, the system is safe to iterate on."

paper:
	AGY_ENV=paper python3 main.py

lint:
	.venv/bin/python3 -m py_compile core/config.py core/events.py core/registry.py core/plugins.py core/logging.py risk/engine.py data/pipeline.py && echo "Lint OK"

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null; true
