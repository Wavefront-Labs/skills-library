---
id: computing-software.firmware-embedded-development.esp-idf.idf-component-manager-dependencies
name: idf-component-manager-dependencies
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [idf-py, idf-component-manager, idf-component-yml, dependencies-lock, esp-component-registry, idf-py-add-dependency, managed-components, esp-idf, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Pull and pin third-party components with the IDF Component Manager: idf_component.yml, version ranges, dependencies.lock, git and local overrides."
sources:
  - https://docs.espressif.com/projects/idf-component-manager/en/latest/
  - https://docs.espressif.com/projects/idf-component-manager/en/latest/reference/manifest_file.html
  - https://docs.espressif.com/projects/idf-component-manager/en/latest/reference/versioning.html
  - https://docs.espressif.com/projects/idf-component-manager/en/latest/reference/dependencies_lock.html
  - https://docs.espressif.com/projects/idf-component-manager/en/latest/use/how_to_offline_usage.html
  - https://components.espressif.com/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IDF Component Manager dependencies

**Goal:** third-party code (LVGL, esp-modbus, sensor drivers, mDNS) declared, versioned and
locked, rather than copied into the repo.

## Add a dependency
```
idf.py add-dependency "espressif/mdns^1.4.0"          # into main/idf_component.yml
idf.py add-dependency --component sensor "lvgl/lvgl~9.2.0"
idf.py reconfigure                                     # resolves, downloads, writes lock
```
`main/idf_component.yml`:
```yaml
dependencies:
  idf: ">=5.2"
  espressif/mdns: "^1.4.0"
  espressif/led_strip:
    version: "~2.5"
    rules:
      - if: 'target in ["esp32s3", "esp32c6"]'
  my_driver:
    git: https://github.com/acme/my_driver.git
    path: components/my_driver
    version: v1.3.0          # any Git ref is accepted (tag, branch or commit); use a tag or commit for releases
  shared_utils:
    path: ../../shared/shared_utils   # local component, for monorepos (not published to the registry)
  # override_path: ../../local/mdns  # key under a registry dependency: use a local copy instead of the registry one
```

## Locking
- `dependencies.lock` at project root records exact resolved versions and hashes. Commit it when
  the project uses only registry and Git sources; do not commit it if it includes local (`path`)
  dependencies, because it then holds environment-specific paths. Do not edit it by hand.
  Builds reuse the locked versions where they still satisfy the constraints; `idf.py update-dependencies` re-solves.
- Downloaded code goes to `managed_components/`, which is not meant to be modified by users (keep it out
  of version control). To patch a dependency, copy it into `components/`: a component in the project
  `components` directory has higher priority than a managed one, or point `override_path` at a local copy.

## Version specs
`^1.4.0` = `>=1.4.0,==1.*`, `~2.5` = `>=2.5.0,==2.5.*`, `*` = any version (avoid). A component can
declare compatible ESP-IDF versions in its own manifest with an `idf` dependency such as `idf: ">=5.0"`.

## CI and offline
- Air-gapped builds: create a partial mirror with `compote registry sync --project-dir PROJECT MIRROR_DIR`
  while online, then add the mirror to `local_storage_url` in `idf_component_manager.yml` so it is checked
  before online sources.
- `IDF_COMPONENT_MANAGER=0` disables the component manager (useful to prove a build doesn't fetch anything).

## Gotchas
- A change in `idf_component.yml` without `idf.py reconfigure` leaves the old lock: CI and laptop
  disagree. Run `idf.py reconfigure` and commit both files together.
- To limit the versions the solver may pick, set `IDF_COMPONENT_CONSTRAINT_FILES` (semicolon-separated
  files, one `component version-constraint` per line) or constrain the dependency in your own manifest.

## Verify
- [ ] Clean clone builds with no network when the mirror in `local_storage_url` holds every dependency.
- [ ] `dependencies.lock` changes only in commits that intend to bump versions.

## Checked

Checked against the idf-component-manager repository docs (main, last commit 2026-10-16) and the ESP-IDF v6.1 component manager guide.
Confirmed: `idf.py add-dependency` (with `--component`, `--path`), `idf.py update-dependencies`, `idf.py reconfigure` generating `dependencies.lock` and `managed_components`; manifest `rules` (all `if` clauses must be true) and the quoted `target in ["esp32", ...]` grammar; `git`, `path`, `version` (any Git ref), `override_path`; `idf` dependency key; version operators `^` and `~` equivalences; lock-file commit guidance (commit unless local sources); `IDF_COMPONENT_MANAGER=0`; `IDF_COMPONENT_CONSTRAINT_FILES`; `compote registry sync` and `local_storage_url`; project `components` directory having priority over managed components. Removed unconfirmed claims: the component cache path and `IDF_COMPONENT_CACHE_PATH`, `IDF_COMPONENT_REGISTRY_URL` as the mirror mechanism, and the exact solver error behaviour.

Method: documentation only; no commands were run.
