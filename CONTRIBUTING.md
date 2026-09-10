# AGY Contribution Rules

## HARD RULES (Non-Negotiable)

1. **No commits to `main` without a PR.** All changes go through a pull request, including Arena Agent outputs.
2. **No modifications to `core/events.py` or `risk/engine.py` without an explicit architecture review.** These are the two components whose corruption causes real financial loss.
3. **Arena Agent gets the `agent/` branch only.** Never grant write access to `main`.
4. **`make test` must pass before any PR is merged.** Zero exceptions. The tests in `tests/test_end_to_end.py` are the Reality Anchor.
5. **No removal or bypass of `risk.evaluate()`.** Any strategy submitting an order that does not pass through `RiskPolicyEngine.evaluate()` will be rejected.

## Development Workflow

```bash
git checkout -b feature/your-feature
make install   # First time only
make lint      # Must pass
make test      # Must pass
git push origin feature/your-feature
# Open PR -> Request review -> Merge
```

## For Arena Agent

Read `docs/architecture/` BEFORE writing code. Read `docs/research/technical-implementation-blueprint.md` for component dependencies.

You MAY modify:
- `strategies/`
- `data/ingestors/`
- `models/`
- `tests/`

You MAY NOT modify:
- `core/events.py`
- `risk/engine.py`
- `core/registry.py`
