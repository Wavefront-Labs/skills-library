---
id: computing-software.firmware-embedded-development.arduino.library-versioning-and-releases
name: library-versioning-and-releases
category: computing-software
field: firmware-embedded-development
product: arduino
tags: [library-release, semver, git-tag, library-manager-indexer, arduino-lint, release-workflow, arduino, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Release Arduino library versions the Library Manager will index: semver in library.properties, matching git tags, indexer rules, arduino-lint gates, and fixing bad releases."
sources:
  - https://github.com/arduino/library-registry/blob/main/FAQ.md
  - https://github.com/arduino/arduino-cli/blob/master/docs/library-specification.md
  - https://github.com/arduino/arduino-lint/blob/main/internal/cli/cli.go
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Library versioning and releases

Once a library is in the Arduino Library Manager registry, the indexer checks the repository
every hour and adds an entry for every new git tag (or release) that meets the requirements.

## Release procedure
1. Bump `version=` in `library.properties` (semver; `1.2.0` is correct and `1.2` is accepted, while `r5`, `003`
   and `1.1c` are invalid).
2. Update CHANGELOG/README.
3. Run checks:
   ```sh
   arduino-lint --library-manager update --compliance strict
   arduino-cli compile -b arduino:avr:uno examples/Basic   # and other target FQBNs, or compile-sketches action
   ```
4. Commit, then tag the **same commit**: `git tag 1.3.0 && git push origin 1.3.0` (the indexer reads
   `library.properties` at the tag; keeping the tag name aligned with the version avoids confusion).
5. Create a GitHub release (optional for the indexer, useful for users).

## Indexer rules that bite
- The `version` in the tag's `library.properties` must not be the same as one already in the index.
- `name=` must not change from the value it had when the library was submitted.
- Releases are rejected when the repository contains `.exe` files, symlinks, a `.development` file or files
  flagged by the antivirus scan, or when `library.properties` is not compliant. Check the indexer logs at
  `http://downloads.arduino.cc/libraries/logs/<host>/<repository slug>/`.

## Versioning policy
- MAJOR: API breaks (renamed methods, changed default I2C address, removed boards).
- MINOR: new features, new boards.
- PATCH: fixes with no API change.
- Dependents pin ranges in their `depends=`; breaking a minor release breaks them.

## Automate
GitHub Actions on tag push: `arduino/arduino-lint-action` (with `library-manager: update`),
`arduino/compile-sketches` across FQBNs, and a check that the tag equals the version in
`library.properties`:
```sh
test "$(grep '^version=' library.properties | cut -d= -f2)" = "${GITHUB_REF_NAME#v}"
```

## Verify
- [ ] New version appears in `arduino-cli lib search <name>` within a few hours of tagging.
- [ ] CI blocks tags whose version does not match `library.properties`.

## Checked

Date: 2026-10-25. Documentation release: arduino/library-registry FAQ on main; Arduino CLI 1.5.1 library specification (commit 2026-10-22); arduino-lint flags from source (commit 2026-10-18).

Confirmed: the indexer checks for new tags every hour and adds entries for compliant tags; the `version` must differ from every version already indexed; `name` must not change; requirements (no `.exe` files, no symlinks, no `.development` file, antivirus scan, valid `library.properties` in the repo root); the indexer log URL is `http://downloads.arduino.cc/libraries/logs/<host>/<repository slug>/`; semver, with `1.2` accepted and `r5`, `003`, `1.1c` invalid; `arduino-lint` flags `--library-manager {submit|update|false}` and `--compliance {strict|specification|permissive}`. Fixed: the log URL scheme; the duplicate-version rule says such a tag is rejected, and the claim that a re-pushed tag is never re-indexed was removed because the FAQ does not state it.

Method: documentation only; no commands were run.
