---
id: computing-software.software-engineering.python.site-module-sitecustomize-and-pth-files
name: site-module-sitecustomize-and-pth-files
category: computing-software
field: software-engineering
product: python
tags: [python, py-runtime-entry, site-sitecustomize, site-module, pth-files, usercustomize, site-packages, python-no-user-site]
level: advanced
status: docs-checked
description: "Understand start-up configuration by site: site-packages, .pth files, sitecustomize/usercustomize, user site, -S and -I flags and the security of auto-executed code."
sources: ["https://docs.python.org/3/library/site.html", "https://docs.python.org/3/using/cmdline.html#cmdoption-I"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# site module, sitecustomize and .pth files

At start-up (unless `-S`), `site` adds site-packages directories to `sys.path`, processes `.pth` files, then imports `sitecustomize` and `usercustomize` if found.

```
python -m site                    # prints sys.path, USER_BASE, USER_SITE, ENABLE_USER_SITE
python -c "import site; print(site.getsitepackages(), site.getusersitepackages())"   # global list is not checked for existence
```

## .pth files (in a site-packages directory)
- One path per line is appended to `sys.path`; non-existing directories are never added and duplicates are skipped. Blank lines and lines starting with `#` are skipped. For backward compatibility, lines starting with `import` (followed by space or tab) are executed with `exec`. In 3.15 those `import` lines are deprecated and ignored when a matching `name.start` file exists (PEP 829); `.start` files list `pkg.mod:callable` entry points called at startup (new in 3.15).
```
# my.pth
/opt/vendor/lib
import mypkg_hooks; mypkg_hooks.install()
```
- Files are processed per site directory in alphabetical order by file name.

## sitecustomize / usercustomize
- After the path changes, `site` imports `sitecustomize` (typically created by an administrator in site-packages) and then `usercustomize` (intended for the user site-packages directory, only if `site.ENABLE_USER_SITE` is true; disable the user site with `-s` or `PYTHONNOUSERSITE`).
- An `ImportError` whose name is that module is silently ignored; **any other exception causes a silent and perhaps mysterious failure of the process**, so keep these files tiny and exception-safe.
- Executable lines (`.pth` import lines, `.start` entry points) always run at startup unless `-S` is given, whether or not the module is ever used, so slow code taxes every start.

## Isolation flags
| Flag | Effect |
|---|---|
| `-I` | isolated mode: implies `-E`, `-P` and `-s`; `sys.path` has neither the script directory nor the user site-packages, and `PYTHON*` variables are ignored |
| `-s` | skip user site-packages |
| `-S` | disable importing `site` and its `sys.path` manipulations (so no `.pth` processing) |
| `-E` | ignore `PYTHON*` environment variables |
| `-P` / `PYTHONSAFEPATH` (3.11+) | do not prepend script dir / cwd to `sys.path` |

## Gotchas
- `.pth` import lines and `sitecustomize` run arbitrary code at start-up, so unexpected files in site-packages deserve review.
- `-P` / `PYTHONSAFEPATH` (3.11+) stops the cwd or script directory being prepended to `sys.path`, and `-I` implies it; otherwise a stray module in those directories can shadow others.
- In a virtual environment, `pyvenv.cfg` is checked: system-level site-packages are searched only if `include-system-site-packages` is `true`, and otherwise the user site is also implicitly not searched.
- Verify behaviour with `python -m site` on your exact interpreter, as details changed in 3.13, 3.14 and 3.15.

## Verify
- [ ] `python -I -c "import sys; print(sys.path)"` shows no cwd entry.
- [ ] A deliberately added `.pth` print line shows up once per interpreter start, then is removed.

## Checked

- 2026-11-03: checked against the CPython docs `library/site.rst` and `using/cmdline.rst` (-E, -I, -P, -s, -S, PYTHONSAFEPATH 3.11, PYTHONNOUSERSITE): .pth rules, 3.15 deprecation of import lines and `.start` files, sitecustomize/usercustomize error handling, `python -m site` output, venv `include-system-site-packages`.
- Removed: coverage.pth and `COVERAGE_PROCESS_START` hooks, editable-install `.pth` names, the `python -v | grep` recipe, the unsourced 3.13 gotcha and the `faulthandler`/proxy use cases.

Method: documentation only; no commands were run.
