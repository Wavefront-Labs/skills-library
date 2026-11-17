---
id: computing-software.software-engineering.python.removed-modules-and-deprecations-in-python-313
name: removed-modules-and-deprecations-in-python-313
category: computing-software
field: software-engineering
product: python
tags: [python, py-versions, py-ver-removals, deprecations-removals-313, pep-594, dead-batteries, python-313, migration]
level: practitioner
status: docs-checked
description: "Migrate off modules and APIs removed in Python 3.13 (PEP 594 dead batteries, 2to3, lib2to3, locale.resetlocale, typing.io) using the replacements named in What's New."
sources: ["https://docs.python.org/3/whatsnew/3.13.html#pep-594-remove-dead-batteries-from-the-standard-library", "https://peps.python.org/pep-0594/", "https://docs.python.org/3/deprecations/index.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Removed modules and deprecations in Python 3.13

Python 3.13 removed the remaining 19 "dead battery" modules of PEP 594 (all deprecated in 3.11): `aifc`, `audioop`, `cgi`, `cgitb`, `chunk`, `crypt`, `imghdr`, `mailcap`, `msilib`, `nis`, `nntplib`, `ossaudiodev`, `pipes`, `sndhdr`, `spwd`, `sunau`, `telnetlib`, `uu`, `xdrlib`. It also removed the `2to3` program and `lib2to3`.

| Removed | Replacement named in What's New |
|---|---|
| `cgi.FieldStorage` | `urllib.parse.parse_qsl()` for GET/HEAD; the `email.message` module or the `multipart` library for POST/PUT |
| `cgi.parse()` | `urllib.parse.parse_qs()` (not for multipart/form-data) |
| `cgi.parse_header()` | the `email` package, e.g. `EmailMessage` (`get_content_type()`, `['content-type'].params`) |
| `cgi.parse_multipart()` | the `email` package or the `multipart` library |
| `crypt` | `hashlib` when only hashing is needed; otherwise PyPI libraries such as `bcrypt`, `argon2-cffi`, `legacycrypt`, `crypt_r` |
| `imghdr`, `sndhdr` | `filetype`, `puremagic` or `python-magic` |
| `mailcap` | `mimetypes` |
| `nntplib` | `pynntp` from PyPI |
| `ossaudiodev` | `pygame` for audio playback |
| `pipes` | `subprocess`; `shlex.quote()` replaces the undocumented `pipes.quote` |
| `spwd` | `python-pam` from PyPI |
| `telnetlib` | `telnetlib3` or `Exscript` from PyPI |
| `uu` | `base64` |
| `audioop` | `audioop-lts` from PyPI |
| `msilib`, `nis`, `xdrlib` | no replacement listed in What's New |

PyPI redistributions exist for most of them under names like `standard-cgi`, `standard-telnetlib`, `standard-pipes` (and `audioop-lts`); treat them as a stopgap.

## Other 3.13 removals
- `locale.resetlocale()` is removed; use `locale.setlocale(locale.LC_ALL, "")`.
- The `typing.io` and `typing.re` namespaces are removed (deprecated since 3.8); import the names from `typing`.
- Chained `classmethod` descriptors are no longer supported.

## Find uses
- Search your code and dependencies for imports of the modules above; an old dependency that imports `cgi` or `telnetlib` breaks on 3.13.
- The "Deprecations" page of the docs lists planned removals by version; use it as the planning checklist.

## Gotchas
- A silent fallback such as `try: import cgi` / `except ImportError` hides breakage until production.

## Verify
- [ ] The test suite passes on 3.13, and every entry point imports cleanly.

## Checked
Date: 2026-11-03. Confirmed against "What's New in Python 3.13": the list of 19 modules, per-module replacements, the `2to3`/`lib2to3` removal, `locale.resetlocale()`, `typing.io`/`typing.re`, chained classmethod descriptors. Removed as unconfirmed: replacement suggestions not in that page (passlib, libcst, ruff, pyupgrade, Pillow, `hashlib.scrypt`), earlier-version removals (`imp`, `distutils`, `asyncore`), command-line recipes (`-W error`, ruff, vermin, grep), Docker advice, "JIT and free-threaded are experimental" remark.
Method: documentation only; no commands were run.
