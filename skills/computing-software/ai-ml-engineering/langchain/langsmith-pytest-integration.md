---
id: computing-software.ai-ml-engineering.langchain.langsmith-pytest-integration
name: langsmith-pytest-integration
category: computing-software
field: ai-ml-engineering
product: langchain
tags: [langchain, langsmith-pytest, langsmith, pytest, llm-testing, evaluation, ci]
level: practitioner
status: docs-checked
description: "Write eval-driven LLM tests with LangSmith's pytest plugin: @pytest.mark.langsmith, logging inputs/outputs/feedback, test suites, caching, rich output."
sources:
  - https://docs.langchain.com/langsmith/pytest
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# LangSmith pytest integration

**Goal:** LLM tests that live with your unit tests, run in CI, and log every case to LangSmith as a dataset example and experiment row.

## Write tests
```python
import pytest
from langsmith import testing as t

@pytest.mark.langsmith(output_keys=["must_contain"])
@pytest.mark.parametrize("question, must_contain", [
    ("How do I reset my password?", "Settings"),
    ("What is the refund window?", "30 days"),
])
def test_support_answers(question, must_contain):
    answer = support_chain.invoke({"question": question})
    t.log_outputs({"answer": answer})
    contains = must_contain.lower() in answer.lower()
    t.log_feedback(key="contains_fact", score=contains)
    assert contains
```
- Every decorated test is synced to a dataset example. Each run creates an experiment with one row per test case; a default boolean `pass` feedback key records pass/fail.
- By default test function arguments are logged as example inputs; `output_keys=[...]` marks arguments that are reference outputs. You can also call `t.log_inputs`, `t.log_outputs` and `t.log_reference_outputs` at any time in the test. Calling any of them twice overwrites the earlier value.
- Log judge scores with `t.log_feedback(key=..., score=...)` without asserting, to track soft metrics.
- Wrap an LLM-as-judge call in `with t.trace_feedback():` so it is traced separately and appears under the feedback key's trace; the `log_feedback` call must be inside the context.
- As a parametrized list grows, the docs suggest `evaluate()` instead, which parallelizes evaluation and gives more control over experiments and datasets.

## Suites and experiments
- By default each test file is its own test suite and dataset. Set `LANGSMITH_TEST_SUITE="support-bot"` to group a whole run into one suite (recommended by the docs for a consolidated view), or pass `test_suite_name` to the marker per test.
- `LANGSMITH_EXPERIMENT="baseline"` names the experiment.
- Experiment metadata can be attached through a `langsmith_experiment_metadata` fixture.

## Running
```bash
export LANGSMITH_API_KEY=... LANGSMITH_TRACING=true
LANGSMITH_TEST_SUITE="support-bot" pytest tests/llm
pytest --langsmith-output tests/llm            # rich per-test display
pip install "langsmith[pytest]"
LANGSMITH_TEST_CACHE=tests/cassettes pytest tests/llm   # cache HTTP requests to disk
```
- With `LANGSMITH_TEST_CACHE` set, requests are cached to that directory and reloaded on later runs; checking the cache into the repository lets CI use it. Cached hosts can be set with `@pytest.mark.langsmith(cached_hosts=[...])`.
- `--langsmith-output` replaces standard pytest output (use plain pytest when debugging) and does not work with `pytest-xdist`.
- `pytest-xdist` parallelism works as normal, async tests are supported, and `ptw` (pytest-watch) can be combined with the cache.

## Checked
Method: docs-checked 2026-11-09 against https://docs.langchain.com/langsmith/pytest (read via targeted greps covering decorator, logging functions, suites, caching, xdist and output flags). Dropped the CI strategy advice, refresh-cassette guidance and the concepts and pytest source links, which were not read.
