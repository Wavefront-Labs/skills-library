---
id: computing-software.software-engineering.python.building-binary-wheels-with-cibuildwheel
name: building-binary-wheels-with-cibuildwheel
category: computing-software
field: software-engineering
product: python
tags: [python, python-packaging, cibuildwheel, binary-wheels, manylinux, musllinux, auditwheel, delocate, abi3, c-extensions, scikit-build-core, maturin]
level: advanced
status: gated
description: "Build and publish Python wheels with C/C++/Rust extensions for Linux, macOS and Windows using cibuildwheel, manylinux, abi3 and repair tools."
sources: ["https://cibuildwheel.pypa.io/en/stable/", "https://github.com/pypa/manylinux", "https://packaging.python.org/en/latest/guides/packaging-binary-extensions/", "https://docs.python.org/3/c-api/stable.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Building binary wheels with cibuildwheel

**Goal:** users `pip install` your compiled extension on every major OS/arch/Python
without needing a compiler.

## Build backend
- C/C++: `scikit-build-core` (CMake) or `meson-python`; setuptools still works.
- Rust: `maturin` (has its own CI generator, `maturin generate-ci github`).
- Cython: either backend with Cython as a build requirement.

## cibuildwheel in GitHub Actions
```yaml
jobs:
  wheels:
    strategy:
      matrix:
        os: [ubuntu-latest, ubuntu-24.04-arm, windows-latest, macos-15-intel, macos-latest]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v6
      - uses: pypa/cibuildwheel@v4.3.3      # current release at review; there is no floating @v4 tag (only v4.3-style minor tags), so pin an exact release or sha
      - uses: actions/upload-artifact@v6
        with: { name: wheels-${{ matrix.os }}, path: ./wheelhouse/*.whl }
```
Config lives in pyproject:
```toml
[tool.cibuildwheel]
build = "cp310-* cp311-* cp312-* cp313-*"
skip = "*-win32 *-musllinux_i686"
test-requires = "pytest"
test-command = "pytest {project}/tests -x"
```
Running tests against the INSTALLED wheel catches missing files and linking errors.

## Linux: manylinux and repair
Wheels are built inside manylinux containers (old glibc) so they run on most distros (gated: unconfirmed, source is paywalled or blocked). Container builds need Docker and were not run in this review.
`auditwheel repair` (run automatically) copies non-system shared libs into the wheel
and sets the platform tag. On macOS `delocate` does the same; on Windows `delvewheel`
(the default repair command on Windows since cibuildwheel 4.0; set `repair-wheel-command` to override or `""` to skip).

## Reducing the matrix with abi3
If you only use the Limited C API, build one `cp310-abi3` wheel per platform that works
on 3.10+: setuptools `py_limited_api=True` / `Py_LIMITED_API`, maturin `abi3-py310`
feature. Free-threaded builds are separate `t` wheels (abi3 does not apply to them). With the default `build = "*"`, cibuildwheel 4.3.3 lists `cp314t-*` identifiers (and no `cp313t`), but an explicit `build = "cp310-* ... cp313-*"` list like the one above matches none of them, so add `cp314t-*` to opt in. cibuildwheel runs `abi3audit` on abi3 wheels automatically.

## Also ship an sdist
Build with `python -m build --sdist` in a separate job; publish wheels + sdist together
via trusted publishing (pypa/gh-action-pypi-publish).

## Gotchas
- macOS: set `MACOSX_DEPLOYMENT_TARGET`; universal2 vs separate x86_64/arm64 wheels.
- Emulated aarch64 via QEMU is very slow; use native ARM runners.
- Linking against system OpenSSL etc. on Linux needs install steps in `before-all`.

## Verify
- [ ] `cibuildwheel --platform linux --print-build-identifiers .` lists the wheels you expect for your `build`/`skip` selectors (no Docker needed).
- [ ] `pip download --only-binary=:all: --no-deps --platform <tag> --python-version <ver> yourpkg` succeeds for each target platform/Python (the `--platform` flag is required when not downloading for the current machine).
- [ ] `auditwheel show` reports a manylinux tag, not `linux_x86_64`.
- [ ] Wheel tests pass in cibuildwheel's isolated test environment.
