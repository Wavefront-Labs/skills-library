---
id: computing-software.digital-forensics-incident-response.log-analysis.package-manager-logs-for-investigations
name: package-manager-logs-for-investigations
category: computing-software
field: digital-forensics-incident-response
product: log-analysis
tags: [package-manager-logs, dnf-history, linux-forensics, dfir]
level: practitioner
status: docs-checked
description: "Use dnf transaction history and the RPM database as evidence: what was installed, removed or changed, install-time ordering and rpm --verify output."
sources: ["https://dnf.readthedocs.io/en/latest/command_ref.html#history-command", "https://man7.org/linux/man-pages/man8/rpm.8.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Package manager logs (dnf history and the RPM database)

Attackers may install tools or remove security agents; package history can show it. This skill covers the DNF and RPM sources that the cited pages document.

## DNF history
- `dnf history` (alias `hist`) lists past transactions; it works only if the `history_record` option is set, so check that setting on the host.
- `dnf history [list] [--reverse] [<spec>...]` prints a table; a spec is a transaction ID, an ID range `a..b`, or a package name. With no spec it lists all known transactions.
- The Action(s) column uses I (install), D (downgrade), O (obsolete), U (upgrade), E (remove), R (reinstall), C (reason change).
- The Altered column can carry flags: `>` the RPM database was changed outside DNF after the transaction, `<` before it, `*` the transaction aborted, `#` it completed with non-zero status, `E` it had warning or error output. A `>` or `<` flag means someone changed packages without DNF: investigate.
- `dnf history info <spec>` describes transactions (latest if none given).
- `dnf history userinstalled` lists packages installed by the user, from groups or module profiles, and outside DNF.
- Transient transactions are listed even though they make no persistent changes.
- Do not run `undo`, `redo` or `rollback` on evidence: they change the system.

## RPM database
- `rpm -qa --last` (the page documents `--last` as ordering the package listing by install time, newest at the top) gives install-time ordering.
- `rpm -V` / `--verify` compares installed files with the database. Output is nine result characters then the file name: S size, M mode, 5 digest, D device, L link path, U user, G group, T mtime, P capabilities; `.` passed, `?` could not be tested. Failures on system binaries are leads for tampering, but also expected for configuration files, so judge by attribute (a `c` marker means a config file).
- Verify results are only as trustworthy as the database and the host. Prefer running against a mounted image with a known-good copy of the tool.

## Gotchas
- Compiled-from-source tools leave no package record.
- Packages added outside the package manager appear only as the `>` or `<` flags above or as verify differences.

## Verify
Every suspicious package action has a transaction ID or install time and is placed on the timeline, with the flag and verify output kept as evidence.

## Checked
Confirmed against the DNF command reference (history command, list/info/userinstalled, action codes, Altered flags, `history_record`) and the rpm(8) man page (`--last`, `--verify` output characters and attribute markers). Removed unconfirmed content: all Debian and Ubuntu content (apt history.log, dpkg.log, debsums; the cited apt(8) man page documents none of it, so that source was dropped), file paths such as `/var/log/dnf.rpm.log`, `/var/lib/dnf/history.sqlite` and yum history locations, the yum, pip, npm, snap, flatpak and apk sections, repository directories, and the example tool list.

Method: docs-only read of cited pages, 2026-11-09
