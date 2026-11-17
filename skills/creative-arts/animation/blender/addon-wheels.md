---
id: creative-arts.animation.blender.addon-wheels
name: addon-wheels
category: creative-arts
field: animation
product: blender
tags: [blender, addon-wheels, python-wheels, wheels, extensions, blender-manifest, pip-download]
level: advanced
status: docs-checked
description: "Ship third-party Python packages inside a Blender extension: pip download wheels per platform, the manifest wheels list, platforms, split-platform builds and pitfalls."
sources:
  - https://docs.blender.org/manual/en/latest/advanced/extensions/python_wheels.html
  - https://docs.blender.org/manual/en/latest/advanced/extensions/getting_started.html
  - https://docs.blender.org/manual/en/latest/advanced/extensions/addons.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# addon-wheels

Goal: an extension that needs, say, Pillow or a parser installs cleanly offline on every platform without `pip install` at runtime.

## 1. Download wheels for Blender's Python

Check the target Blender's Python version first (`import sys; sys.version` in its Python console); the manual's example uses `--python-version=3.13`. Wheels must be unmodified from PyPI and include their dependencies. Then from the extension folder (for a pure-Python package, `pip wheel jsmin -w ./wheels` is the manual's example):

```bash
pip download pillow --dest ./wheels --only-binary=:all: --python-version=3.13 --platform=win_amd64
pip download pillow --dest ./wheels --only-binary=:all: --python-version=3.13 --platform=manylinux_2_28_x86_64
pip download pillow --dest ./wheels --only-binary=:all: --python-version=3.13 --platform=macosx_11_0_arm64
```
Pure-Python packages produce one `py3-none-any` wheel that serves all platforms. Use the platform identifiers listed on the package's PyPI download page.

## 2. List them in `blender_manifest.toml`

```toml
platforms = ["windows-x64", "linux-x64", "macos-arm64"]
wheels = [
  "./wheels/pillow-12.1.0-cp313-cp313-win_amd64.whl",
  "./wheels/pillow-12.1.0-cp313-cp313-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl",
  "./wheels/pillow-12.1.0-cp313-cp313-macosx_11_0_arm64.whl",
]
```
Installing the extension extracts the wheels into the extension's own `site-packages` directory. List wheel paths with forward slashes; by convention keep them under `./wheels/`.

## 3. Build

```bash
blender --command extension build --split-platforms   # one zip per platform (file-name suffix), limited by `platforms`
blender --command extension validate
```
Without `--split-platforms` one zip contains every platform's wheels (bigger, but one file).

## Import in code

Import normally (`from PIL import Image`), inside functions if the import is slow, so add-on registration stays fast.

## Gotchas

- Wheels must be bundled unmodified from PyPI and their file names must follow Python's binary-distribution naming, so keep the names pip produced.
- With `--split-platforms`, a platform appears only if it is listed in `platforms`: the manual's example lists Windows and macOS and no Linux zip is built, even though a Linux wheel is present.
- The manual's wheel guidance still carries open to-dos (version selection and a policy for conflicting wheel versions), so check the current page before relying on either.

## Verify

Install the built zip with *Install from Disk*, then in the Python console `import PIL; print(PIL.__file__)` (substitute your package) to confirm it loads from the extension's site-packages.

## Checked

Blender 5.2 manual (blender-v5.2-release branch), read 2026-10-27.
- Wheel download commands, `./wheels/` convention, example manifest with `cp313` wheels, `--split-platforms` behaviour and the Mac/Windows-only example: python_wheels page.
- Wheels extracted into the extension's own site-packages: python_wheels page.
- Removed as unconfirmed or wrong: shared site-packages, the sys.path/pip rejection claim, the numpy/requests bundled claim, the conflicting-versions behaviour, and the CPython 3.11 pin (the manual example uses 3.13).

Method: documentation only; no commands were run.
