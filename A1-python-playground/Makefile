help:
	@echo ""
	@echo "Usage: make <target>"
	@echo ""
	@echo "  submit-a, submit-b, ...  Write submission.json for one puzzle"
	@echo "  submit-all               Write submission.json for every puzzle"
	@echo ""
	@echo "  agent-kisski   Set up AGENTS.md for KISSKI, the university AI service (default)"
	@echo "  agent-coding   Set up AGENTS.md and CLAUDE.md for your own coding agent"
	@echo "  chat-bundle    Write chat-bundle.md to upload to a chat in the browser"
	@echo ""
	@echo "  install    Set up git, the environment, the hooks and AGENTS.md"
	@echo "  clean      Remove the virtual environment and caches"
	@echo "  lint       Check code with ruff"
	@echo "  format     Format code with ruff"
	@echo "  typecheck  Type-check code with mypy"
	@echo ""


# ---- Puzzles -----------------------------------------------------------------

submit-a:
	uv run python submit.py a

submit-b:
	uv run python submit.py b

submit-c:
	uv run python submit.py c

submit-d:
	uv run python submit.py d

submit-e:
	uv run python submit.py e

submit-f:
	uv run python submit.py f

submit-g:
	uv run python submit.py g

submit-h:
	uv run python submit.py h

submit-i:
	uv run python submit.py i

submit-j:
	uv run python submit.py j


# ---- All puzzles -------------------------------------------------------------

submit-all submit:
	uv run python submit.py


# ---- Utilities ---------------------------------------------------------------

agent-kisski:
	uv run python agents/build_agents.py kisski

agent-coding:
	uv run python agents/build_agents.py coding

chat-bundle:
	uv run python agents/build_agents.py chat

check:
	@which git > /dev/null 2>&1 || (echo "Error: git is not installed"; exit 1)
	@which uv  > /dev/null 2>&1 || (echo "Error: uv is not installed";  exit 1)

# `git init` only outside a repository, since pre-commit needs one. The
# KISSKI AGENTS.md is built only while AGENTS.md is still the placeholder,
# so running install again keeps an `agent-coding` setup.
install: check
	@git rev-parse --is-inside-work-tree > /dev/null 2>&1 || git init -b main
	uv sync
	uv run pre-commit install
	@grep -qs "Generated from agents/template.md" AGENTS.md \
		|| uv run python agents/build_agents.py kisski

clean:
	rm -rf .venv .mypy_cache .ruff_cache
	find . -type d -name __pycache__ -exec rm -rf {} +

lint:
	uv run ruff check .

format:
	uv run ruff format .

typecheck:
	uv run mypy .

.PHONY: help submit-all submit agent-kisski agent-coding chat-bundle check install clean lint format typecheck \
        submit-a submit-b submit-c submit-d submit-e submit-f submit-g submit-h submit-i submit-j
