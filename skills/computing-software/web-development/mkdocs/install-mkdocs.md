---
id: computing-software.web-development.mkdocs.install-mkdocs
name: install-mkdocs
category: computing-software
field: web-development
product: mkdocs
tags: [installation, pip-install, mkdocs-version, windows-path, man-pages]
level: intro
status: docs-checked
description: "Install MkDocs with pip, confirm it with mkdocs --version, and work around Windows PATH problems or add manpages with click-man."
sources:
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/installation.md
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/getting-started.md
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/localizing-your-theme.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
MkDocs needs a recent Python and pip. Check both, upgrade pip if needed, then install:

```bash
python --version
pip --version
pip install --upgrade pip
pip install mkdocs
mkdocs --version
```

If pip is missing, download get-pip.py and run `python get-pip.py`.

**Windows**: when installing Python, tick the option that adds Python to PATH (normally off by default). If commands are not found, prefix them with `python -m`:

```bash
python -m pip install mkdocs
python -m mkdocs
```

For a permanent fix, add the `Scripts` directory of your Python installation to `PATH` (recent Pythons ship `win_add2path.py` under `Tools/Scripts` to do this).

**Manpages** are not installed by pip. Generate them with click-man:

```bash
pip install click-man
click-man --target path/to/man/pages mkdocs
```

Extra for theme localization: `pip install 'mkdocs[i18n]'`.

## Checked

2026-11-04. Confirmed against the MkDocs Installation guide and Getting Started: Python and pip requirements, version checks, pip upgrade, get-pip.py, `pip install mkdocs`, `mkdocs --version`, the Windows PATH option and `python -m` workaround, `win_add2path.py`, the click-man commands; and against Localizing Your Theme (`pip install 'mkdocs[i18n]'`). Removed: nothing beyond a generic verify line.

Method: documentation only; no commands were run.
