---
id: computing-software.firmware-embedded-development.platformio.git-and-local-library-dependencies
name: git-and-local-library-dependencies
category: computing-software
field: firmware-embedded-development
product: platformio
tags: [git-dependency, lib-deps-git, symlink-dependency, file-dependency, private-repo, lib-extra-dirs, platformio, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Depend on libraries from Git or local paths in PlatformIO: git URLs with tags/commits, private repos and tokens, symlink:// for live editing, file://, and lib_extra_dirs."
sources:
  - https://docs.platformio.org/en/latest/core/userguide/pkg/cmd_install.html
  - https://docs.platformio.org/en/latest/projectconf/sections/env/options/library/lib_deps.html
  - https://docs.platformio.org/en/latest/projectconf/sections/env/options/library/lib_extra_dirs.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Git and local dependencies

## Git
Repository specification: `[<name>=][<scheme>://][<user>[:<password>]@]<hostname>[:<port>][:][/]<path>[#<commit-ish|branch|tag>]`.
Supported schemes: `http`, `https`, `git`, `git+http`, `git+https`, `git+ssh`, `hg+http`,
`hg+https`, `hg+ssh`, `svn+http`, `svn+https`, `svn+ssh`.
```ini
lib_deps =
    https://github.com/acme/AcmeDriver.git#v1.4.0          ; tag
    https://github.com/acme/AcmeDriver.git#4f2a9c1d0b3e     ; commit (full hash)
    https://github.com/acme/AcmeDriver.git#develop          ; branch (moves)
    AcmeDriver=https://github.com/acme/AcmeDriver.git       ; custom package folder name
    git+ssh://user@git.example.org/acme/private-lib.git     ; SSH
```
- The package at a URL is installed by cloning it; if the repository uses submodules, they are
  cloned too.
- Use `name=` to set the storage folder name.
- Use tags or commits for deterministic builds; a branch moves.
- Do not put credentials in committed files.

## Local
```ini
lib_deps =
    FooLib=symlink://../shared/drivers/AcmeDriver   ; live link
    file://../vendor/AcmeDsp                        ; copy
```
- `file://<folder>` copies all files from the local folder to the package manager: changes in
  the source folder do **not** affect the installed package.
- `symlink://<folder>` creates a symbolic link: changes in the source folder **do** affect the
  installed package.
- The folder must contain a manifest with name and version. Its manifest dependencies are
  installed too.
- Local TAR or ZIP archives (`.tar.gz`, `.tar`, `.tgz`, `.zip`) work with `file://<archive>`;
  remote archives work with an `http://` or `https://` URL.
- The project `lib` folder holds private libraries, each in its own subfolder; the LDF searches
  it first.
- `lib_extra_dirs` (storage folders whose subfolders are libraries) is deprecated since 6.0 and
  will be removed; use `symlink://` dependencies instead.

## Monorepo pattern
```
firmware/
  apps/sensor/platformio.ini   -> lib_deps = symlink://../../libs/radio
  libs/radio/library.json
```
Each library has a `library.json` with its own dependencies; apps declare only direct ones.

## Gotchas
- Two dependencies that resolve to the same library name from different sources: give each an
  explicit `name=`.
- Check `pio pkg list` to see what was actually installed.

## Verify
- [ ] Clean CI build resolves Git dependencies at the pinned tag or commit (`pio pkg list`).
- [ ] Editing a symlinked library triggers recompilation of that library.

## Checked
2026-10-26 against platformio-docs (develop, last commit 2026-09-19): `pio pkg install`
package specifications, `lib_deps` and `lib_extra_dirs`. Confirmed: repository syntax and
schemes, `#` refs, `name=` syntax, submodule cloning, `file://` copy versus `symlink://` link
semantics, manifest requirement, archive forms, `lib_extra_dirs` deprecation. Corrected: the
draft said submodules are not fetched (the docs say they are cloned). Removed as unconfirmed:
the `${sysenv}` token URL form and credential helper advice, Windows symlink behaviour, shallow
clones, "repos without a manifest still work", and `pio pkg update` re-fetch behaviour.
Method: documentation only; no commands were run.
