---
id: computing-software.software-engineering.pydantic.install-pydantic-and-follow-version-policy
name: install-pydantic-and-follow-version-policy
category: computing-software
field: software-engineering
product: pydantic
tags: [pydantic, pydantic-install, pip, extras, email-validator, version-policy, experimental-features, python-support]
level: intro
status: docs-checked
description: "Install Pydantic with pip, uv or conda, add the email and timezone extras, and apply the V2 version policy for breaking changes and experimental features."
sources:
  - https://docs.pydantic.dev/latest/install/
  - https://docs.pydantic.dev/latest/version-policy/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: install Pydantic correctly and know what may change between releases.

## Install
```bash
pip install pydantic
uv add pydantic
conda install pydantic -c conda-forge
```
The page says Python 3.10+ with `pip` is all you need. Dependencies: `pydantic-core` (Rust validation logic), `typing-extensions`, `annotated-types`, `typing-inspection`.

## Optional extras
- `email`: email validation via `email-validator`.
- `timezone`: fallback IANA time zone database via `tzdata`.
```bash
pip install 'pydantic[email]'
pip install 'pydantic[email,timezone]'
uv add 'pydantic[email,timezone]'
pip install email-validator tzdata   # manual alternative
```
From the repository: `pip install 'git+https://github.com/pydantic/pydantic@main'`, or with extras `...@main#egg=pydantic[email,timezone]`.

## Version policy (V2)
- No intentional breaking changes in minor releases; deprecated functionality is not removed until V3.
- NOT counted as breaking, so may change in minor releases: bug fixes that break code relying on undocumented behaviour; JSON schema reference format; `msg`, `ctx` and `loc` of `ValidationError` (`type` will not change, so parse errors by `type`); new keys or new errors in `ValidationError`; `__repr__` behaviour; contents of core schemas (`__pydantic_core_schema__`).
- In V3, `pydantic-core` is expected to be merged into Pydantic as an internal sub-module.
- Tags: Git tags prefixed `v`; since v2.13 `pydantic-core` is a workspace member and its releases are tagged `core-vx.y.z`.

## Experimental features
Either located in `pydantic.experimental` (`from pydantic.experimental import feature_name`) or in the main module prefixed `experimental_`. They can change or be removed with little notice. Lifecycle when promoted: copy to the main module (old one warns or is deprecated), then a stub with an error message, then removal.

## Python support
A Python version is dropped when it has reached expected end of life and under 5% of downloads of the most recent minor release use it.

## Checked

Checked 2026-11-07. Compared every claim with the install page (install.md) and the version policy (version-policy.md): pip, uv and conda commands, dependencies, the `email` and `timezone` extras, repository installs, non-breaking change list, V3 `pydantic-core` merge, tagging, experimental naming and lifecycle, and Python support rule. Removed the claim that the `email` extra is needed for `EmailStr`, which the install page does not state, and reworded the Python requirement to the page's wording.

Method: documentation only; no commands were run.
