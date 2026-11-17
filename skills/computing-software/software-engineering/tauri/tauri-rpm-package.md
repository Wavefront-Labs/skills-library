---
id: computing-software.software-engineering.tauri.tauri-rpm-package
name: tauri-rpm-package
category: computing-software
field: software-engineering
product: tauri
tags: [rpm-package, tauri, rpm-signing]
level: advanced
status: docs-checked
description: "Configure, build, sign, verify and debug a Tauri RPM package: scripts, dependencies, license, GPG signing and rpm query commands."
sources:
  - "https://v2.tauri.app/distribute/rpm/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tauri RPM package

Goal: configure, build, sign and inspect an RPM. Build on the oldest base system you support that provides WebKitGTK 4.1 (glibc compatibility, for example Ubuntu 22.04 or Debian 12).

## Configure (`tauri.conf.json > bundle > linux > rpm`)

- Scripts: `preInstallScript`, `postInstallScript`, `preRemoveScript`, `postRemoveScript`, each a path to a shell script (for example in `src-tauri/scripts`).
- `conflicts`, `depends`, `obsoletes` (installed packages listed as obsoletes are automatically removed), `provides`, `files`, `desktopTemplate` (custom desktop file), `epoch` (not recommended unless necessary; it alters version comparison), `release`.
- License: `license = "MIT"` in `Cargo.toml`, or `bundle > license` and `bundle > licenseFile` in `tauri.conf.json`.

Build with `tauri build`; the RPM lands in `src-tauri/target/release/bundle/rpm`.

## Sign

Generate a key with `gpg --gen-key`, then export it before building:

```bash
export TAURI_SIGNING_RPM_KEY=$(cat /path/to/my_super_private.key)
export TAURI_SIGNING_RPM_KEY_PASSPHRASE=password   # if the key has a passphrase
```

To verify locally only: `gpg --export -a 'Tauri-App' > RPM-GPG-KEY-Tauri-App`, `sudo rpm --import RPM-GPG-KEY-Tauri-App`, set `%_signature gpg`, `%_gpg_name` and related macros in `~/.rpmmacros`, then:

```bash
rpm -v --checksig tauri-app-0.0.0-1.x86_64.rpm
```

## Debug the package

- Info: `rpm -qip package_name.rpm`
- Specific fields: `rpm -qp --queryformat '[%{NAME} %{VERSION} %{RELEASE} %{ARCH} %{SIZE}\n]' package_name.rpm`
- Contents: `rpm -qlp package_name.rpm`
- Scripts: `rpm -qp --scripts package_name.rpm`
- Dependencies: `rpm -qp --requires package_name.rpm`
- Dependents: `rpm -q --whatrequires package_name.rpm`
- Install trouble: `rpm -ivvh package_name.rpm` (or `-Uvvh` for an installed package) for very verbose output.

## Checked

Checked 2026-11-08 against the Tauri v2 RPM page: the glibc/WebKitGTK 4.1 build-system advice, rpm config keys (the page's prose says conflict, its example uses conflicts), license settings, output directory, GPG signing variables, local verification steps and every rpm query command. No claims removed.

Method: docs-only read of cited pages, 2026-11-08
