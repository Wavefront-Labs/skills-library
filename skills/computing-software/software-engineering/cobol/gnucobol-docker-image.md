---
id: computing-software.software-engineering.cobol.gnucobol-docker-image
name: gnucobol-docker-image
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, gnucobol-docker-image, cobol-devops, docker-cobol, gnucobol-ci, container-build, github-actions-cobol]
level: practitioner
status: docs-checked
description: "Build and test GnuCOBOL programs in a container or CI runner with reproducible versions."
sources:
  - https://gnucobol.sourceforge.io/
  - https://gnucobol.sourceforge.io/doc/gnucobol.html
  - https://packages.debian.org/stable/gnucobol
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GnuCOBOL in containers and CI
**Goal:** repeatable builds off the mainframe.

```dockerfile
FROM debian:stable-slim
RUN apt-get update && apt-get install -y --no-install-recommends gnucobol \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY src/ ./src/
RUN cobc -x -o app src/main.cob
CMD ["./app"]
```
- On Debian stable the `gnucobol` package is a dependency package for the default GnuCOBOL compiler; it pulls in `gnucobol3`. Which GnuCOBOL release you get depends on the distribution release, so print `cobc --version` (`-V`) in the build log. For a pinned version, build a release from the GnuCOBOL site (3.2 is the current release there).
- `cobc` builds a dynamically loadable module by default; `-x` includes the main function and produces an executable, with the first program in the file as the entry point. `-o` names the output.
- CI steps: `cobc -x -Wall` (`-Wall` does not enable every warning; for example truncation and unreachable-statement warnings need their own flags), run test drivers, compare outputs with golden files, fail on non-zero exit.
- Runtime settings can be given as environment variables (normally the parameter name in upper case with the `COB_` prefix) or in a runtime configuration file named by `COB_RUNTIME_CONFIG`. Environment variables take precedence over the file, so setting them with `ENV` in the Dockerfile or in the CI job works.
- Dynamic CALLs to separately built modules find them via `COB_LIBRARY_PATH`; `cobc -c -static` plus static linking is the alternative the manual describes, which also verifies at build time that all called programs are present.

## Gotchas
- Check that the final image has everything the executable needs at runtime if you use a multi-stage build; this skill has not verified which libcob files to copy, so test by running the image.
- The default `cobc` target is a module, not a program: forgetting `-x` gives a `.so` that cannot be run directly.

## Self-check
`docker run` the image and compare output to the golden file.

## Checked
2026-11-08. Confirmed against the GnuCOBOL homepage and the GnuCOBOL Programmer's Guide (cobc options -x, -o, -V, -Wall, default module target; runtime configuration and COB_ environment variables; COB_LIBRARY_PATH; static CALL) and the Debian package page for `gnucobol` (stable). Removed: claims that libcob shared libraries must be copied into the final image and that container locale affects text files, which none of the pages state.
Method: documentation only; no commands were run.
