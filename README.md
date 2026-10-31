# Excessive Agency Fixture (OWASP LLM06)

A small, deterministic fixture pair for evaluating whether a reviewer (human or AI)
can tell a vulnerable agent implementation from a secure one.

- `vulnerable/app.py`: summarizer agent that runs any tool call the model emits
- `secure/app.py`: same agent with per-task tool allow-list, path restriction, human approval
- `common.py`: in-memory filesystem + deterministic mock LLM (obeys instructions found in documents, simulating indirect prompt injection)
- `tests/test_fixture.py`: pass/fail checks, no network, no randomness
- `ANSWER_KEY.md`: hidden key (would be withheld from the evaluated model)

Run: `python3 tests/test_fixture.py`
All secrets and domains are fake.
