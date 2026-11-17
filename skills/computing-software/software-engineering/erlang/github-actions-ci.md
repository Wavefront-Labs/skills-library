---
id: computing-software.software-engineering.erlang.github-actions-ci
name: github-actions-ci
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-containers-ci, github-actions-ci]
level: practitioner
status: draft
description: "CI for Erlang with erlef/setup-beam: OTP matrix, rebar3 caching and running compile, xref, dialyzer, eunit and ct."
sources:
  - https://github.com/erlef/setup-beam
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# GitHub Actions CI for rebar3 projects
**Goal:** automate the full check suite.

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix: { otp: ['26', '27'] }
    steps:
      - uses: actions/checkout@v4
      - uses: erlef/setup-beam@v1
        with: { otp-version: '${{ matrix.otp }}', rebar3-version: '3' }
      - uses: actions/cache@v4
        with:
          path: |
            _build
            ~/.cache/rebar3
          key: ${{ runner.os }}-otp${{ matrix.otp }}-${{ hashFiles('rebar.lock') }}
      - run: rebar3 do compile, xref, dialyzer, eunit, ct
```
- Pin action versions per your policy; `erlef/setup-beam` is the maintained Erlang/Elixir setup action.
- Cache the PLT (`~/.cache/rebar3`) to avoid rebuilding it each run (location per rebar3 docs).
- Upload `_build/test/logs` as an artifact on failure for Common Test.

## Gotchas
- Matrix OTP versions you actually support; deprecations show first on the newest.

## Self-check
Break a test and confirm CI fails and uploads logs.
