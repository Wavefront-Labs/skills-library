---
id: computing-software.networking-hardware-and-wireless.apache-httpd.modules-dso-loading
name: modules-dso-loading
category: computing-software
field: networking-hardware-and-wireless
product: apache-httpd
tags: [networking-hardware-and-wireless, apache-httpd, modules, dso, loadmodule, apxs]
level: intro
status: docs-checked
description: "Load and build Apache modules as DSOs: LoadModule, configure flags for shared modules, and apxs for third-party modules."
sources:
  - https://httpd.apache.org/docs/2.4/dso.html
  - https://httpd.apache.org/docs/2.4/configuring.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Modules and DSO loading
Only core functionality is built in; everything else is a module. `mod_so` must be statically compiled; nearly all others can be DSOs (`mod_foo.so`) loaded by `LoadModule` at startup or restart.

## Build shared modules
```
./configure --prefix=/path/to/install --enable-foo
./configure --enable-mods-shared=all
```
- `reallyall` also includes developer modules.
- `--enable-load-all-modules` activates the LoadModule lines for every built module.
- `--enable-mods-static` disables DSO builds for individual modules.

## Third-party modules
```
apxs -cia mod_foo.c
```
`apxs` builds outside the source tree; `-i` installs. Then run `apachectl restart`.

After building, a `LoadModule` directive in httpd.conf must activate the module. Only a basic set loads at startup with `--enable-mods-shared=all`; toggle the `LoadModule` lines to change it.

## Checked
2026-11-04. Confirmed against the DSO support page: mod_so static, LoadModule, configure options, apxs -cia, restart after apxs -i. Removed the IfModule advice and the httpd -M / -l lines, which that page does not cover.
Method: documentation only; no commands were run.
