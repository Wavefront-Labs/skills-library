---
id: computing-software.software-engineering.perl.pause-release-process
name: pause-release-process
category: computing-software
field: software-engineering
product: perl
tags: [perl, pause-upload, cpan-release, changes-file, meta-json, release-checklist, pause-release-process]
level: advanced
status: draft
description: "Release a distribution to CPAN through PAUSE: account, permissions, version, Changes, META files, upload and verification."
sources: ["https://pause.perl.org", "https://perldoc.perl.org/perlnewmod", "https://metacpan.org/pod/CPAN::Meta::Spec"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Releasing to CPAN via PAUSE

**Goal:** a clean public release.

## One-time setup
1. Request a PAUSE account at pause.perl.org (manual approval; use a real name and an email you read).
2. Check namespace permissions after your first upload ("first-come" permissions); co-maintainers are added in the PAUSE web UI. Ask via the module list or `modules@perl.org` guidance when taking over or adding top-level namespaces (see the PAUSE and perlnewmod docs).
3. Store credentials in `~/.pause` (`user ...` and `password ...`, file mode 600) for upload tools such as `cpan-upload`, or upload through the web form.

## Release checklist
- Pick a unique, accurate distribution name (`My-Module`) and module names following existing conventions (perlmodstyle).
- Bump `$VERSION`; add an entry to `Changes` (newest first, user-visible changes only).
- Tests green on supported Perls (CI matrix: perl-actions or Docker) and a clean `make disttest`/`dzil test`.
- `META.json` (meta-spec 2) with `license`, `resources`, `prereqs`, `provides` (optional), `x_` extras, `release_status`.
- `LICENSE`/`COPYRIGHT` and POD sections NAME, SYNOPSIS, DESCRIPTION, AUTHOR, LICENSE.
- Developer/trial releases: a version containing `_` (for example `1.02_01`) or a tarball name with `-TRIAL` is not indexed as the main release.
- Upload: `cpan-upload My-Module-1.00.tar.gz` (CPAN::Uploader), `dzil release`, or the PAUSE web form.
- After upload: wait for the indexing mail; confirm on metacpan.org and CPAN Testers reports (hours later); fix regressions with a quick patch release.

## Rules
- A released version is immutable and cannot be re-uploaded with the same filename; you can delete a file for a limited time via PAUSE (it remains on BackPAN).
- Don't ship generated junk (`blib/`, `*.bak`, `.git`), and exclude with `MANIFEST.SKIP`.
- Add a security policy and contact (`SECURITY.md` or POD) and respond to CPAN Security Group reports.
- Follow semantic expectations: breaking API changes get a clear note in Changes and a version bump.

## Self-check
- [ ] The tarball unpacks, `perl Makefile.PL && make test` passes, and `Changes` has the new version at the top.
