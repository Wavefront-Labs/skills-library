---
id: computing-software.firmware-embedded-development.arduino.library-manager-registry-submission
name: library-manager-registry-submission
category: computing-software
field: firmware-embedded-development
product: arduino
tags: [arduino-library, library-registry, library-manager, repositories-txt, release-tag, semver, library-properties-version, arduino, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Publish an Arduino library to the Library Manager: registry PR, release tags matching library.properties version, and the indexer rules that silently skip releases."
sources:
  - https://github.com/arduino/library-registry/blob/main/README.md
  - https://github.com/arduino/library-registry/blob/main/FAQ.md
  - https://github.com/arduino/arduino-cli/blob/master/docs/library-specification.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Submitting to the Arduino Library Manager

**Goal:** users install your library by name from the IDE / `arduino-cli lib install`, and
every new release shows up within a day.

## One-time registration
1. Library repo public on GitHub/GitLab/Bitbucket, `library.properties` at the repo root
   (not in a subfolder), passing `arduino-lint --library-manager submit --compliance strict`.
2. Fork `arduino/library-registry`, add the repo URL to `repositories.txt`, open a PR. An automated system
   checks it, registers the library if no problems are found, and reports problems in PR comments (mention
   @ArduinoBot to re-run the check after fixing the library).
3. The `name=` in `library.properties` must not change after registration (see the FAQ's "How can I change
   a library's name?"), must not match an existing library's name (case-insensitive), and must not start with
   `Arduino` for third-party libraries; choose carefully.

## Releasing
- Each release = a **git tag** (or release) whose tree has `library.properties` with a **new** `version=`.
  The indexer runs every hour and picks up new tags.
- Keep the tag and the version aligned (tag `1.4.2`, `version=1.4.2`).
- Use semver. Users with update notifications get every release, so breaking changes need a major bump.

## Indexer pitfalls (release silently missing)
- `version=` not changed from a version already in the index.
- `library.properties` not compliant at that tag (for example `depends=` naming a library that is not
  in the index).
- `.exe` files, symlinks or a `.development` file in the repository, or files flagged by the antivirus scan.
- The requirements are checked at the time of the tag: after fixing a problem, publish a new tag with a new version.
- Check the indexer logs: `http://downloads.arduino.cc/libraries/logs/<host>/<repository slug>/`.

## Dependencies
`depends=<library name>, <library name>` in `library.properties` makes the IDE offer to install them.
Arduino Lint expects names found in the Library Manager index; version constraints such as
`depends=ArduinoHttpClient (>=1.0.0)` are supported.

## Verify
- [ ] `arduino-cli lib search <name>` lists the new version within a few hours of tagging.
- [ ] Indexer log shows no errors for the tag.

## Checked

Date: 2026-10-25. Documentation release: arduino/library-registry README and FAQ on main; Arduino CLI 1.5.1 library specification.

Confirmed: submission is a pull request adding the repository URL to `repositories.txt`; an automated system checks it, registers the library when no problems are found and comments on the pull request (re-run by mentioning @ArduinoBot); the library becomes installable within a day; requirements (`library.properties` in the repository root, no `.exe`, symlinks or `.development` file, a tag, name not already used, third-party names must not start with `Arduino`); the indexer runs every hour; the `version` must differ from every indexed version and `name` must not change; the log URL; `depends` accepts version constraints. Removed unconfirmed claims: "permanently claimed" wording, the "very large files" and "unsupported file types" causes, and the remark that tags are immutable to the indexer.

Method: documentation only; no commands were run.
