---
id: computing-software.email-administration.dovecot.pigeonhole-installation-and-version-matching
name: pigeonhole-installation-and-version-matching
category: computing-software
field: email-administration
product: dovecot
tags: [pigeonhole, managesieve, repo-dovecot-org, autogen, with-dovecot, sieve-package]
level: intro
status: docs-checked
description: "Install Pigeonhole for Sieve and ManageSieve from packages or source, and recompile it whenever Dovecot is upgraded."
sources:
  - https://doc.dovecot.org/main/installation/sieve.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Pigeonhole is the project adding the Sieve language (RFC 5228) and the ManageSieve protocol (RFC 5804) to Dovecot. Installing from packages is recommended. Pigeonhole packages are available from repo.dovecot.org, and many distributions package Dovecot and Pigeonhole themselves; search your package manager for dovecot, pigeonhole or sieve.

Source builds: download the latest release from the Pigeonhole download page or get the source, including unreleased changes, from the GitHub repository. For a Git checkout run `./autogen.sh` first to build the automake structure, which needs autotools and libtool.

If Dovecot was installed from sources, Pigeonhole's configure script usually finds the installed `dovecot-config` itself. When it does not, pass `--with-dovecot=<path>`, where the path is a directory containing the `dovecot-config` file. That can be an installed location or an already compiled Dovecot source directory.

Key warning: recompile Pigeonhole whenever you upgrade Dovecot to a new version. Otherwise the Sieve interpreter plugin fails to load with a version error.

## Checked
2026-11-09. Read the Dovecot Sieve (Pigeonhole) Installation page (main documentation, marked pre-release) in full.
Confirmed: RFC 5228 and RFC 5804, repo.dovecot.org packages, distribution packages, download page and GitHub sources,
`./autogen.sh` with autotools and libtool, `--with-dovecot=<path>` forms, and the recompile warning. Removed as
unconfirmed: "scripts silently stop running", the packaged-install matched-set claim, and the post-install plugin
enablement paragraph.
Method: documentation only; no commands were run.
