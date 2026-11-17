---
id: computing-software.qa-testing-engineering.test-automation.vcr-record-replay-http
name: vcr-record-replay-http
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [vcr-cassettes, record-replay, service-virtualization, vcrpy, pytest-recording, polly-js, http-fixtures]
level: practitioner
status: verified
description: "Record real HTTP interactions once and replay them in tests with VCR-style tools (vcrpy/pytest-recording, Polly.js, Playwright HAR): record modes, filtering secrets, refresh."
sources:
  - https://vcrpy.readthedocs.io/
  - https://github.com/kiwicom/pytest-recording
  - https://netflix.github.io/pollyjs/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Record and replay HTTP (VCR)

**Goal:** deterministic tests against third-party APIs without calling them on every run.

## pytest-recording (vcrpy)
```python
import pytest
@pytest.mark.vcr
def test_get_rates(client):
    assert client.get_rates("EUR")["USD"] > 0

@pytest.fixture(scope="module")
def vcr_config():
    return {"filter_headers": ["authorization", "x-api-key"],
            "filter_query_parameters": ["api_key"],
            "decode_compressed_response": True}
```
```bash
pytest --record-mode=once        # record missing cassettes, replay existing
pytest --record-mode=none        # CI: fail if a request has no cassette
pytest --record-mode=rewrite     # refresh all cassettes (pytest-recording only)
```
Cassettes land in a `cassettes/<module>/<test>.yaml` folder next to the test module (for example `tests/cassettes/test_rates/test_get_rates.yaml`), committed to git. Plain vcrpy (`vcr.VCR(record_mode=...)`) accepts only `once`, `new_episodes`, `none`, `all` (and `any`); `rewrite` raises ValueError there, it is a pytest-recording option (run on vcrpy 8.3 and pytest-recording: with the server stopped, `--record-mode=none` replayed an existing cassette and raised `CannotOverwriteExistingCassetteException` for a test with no cassette).

## JS
Polly.js (`@pollyjs/core` with node-http/fetch adapters, `recordIfMissing`), or Playwright `routeFromHAR` for browser traffic (`har-file-mocking`).

## Rules
- Filter secrets before the first commit of a cassette; scan cassettes in CI for tokens.
- Match on method + path + relevant body, not volatile headers/timestamps (custom matchers).
- Refresh cassettes on a schedule (monthly) or when the API changes, and pair with a small live contract test so drift is detected.

## Gotchas
- Cassettes freeze responses with dates; tests depending on "now" break later. Freeze time too.
- Recording from production with real customer data creates a data leak in the repo.

## Verify
CI runs with `--record-mode=none`, no network access, and passes; a grep for secrets over cassettes finds nothing.
