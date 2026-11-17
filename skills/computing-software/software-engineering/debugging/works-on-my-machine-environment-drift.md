---
id: computing-software.software-engineering.debugging.works-on-my-machine-environment-drift
name: works-on-my-machine-environment-drift
category: computing-software
field: software-engineering
product: debugging
tags: [debugging, production-debugging, environment-drift, works-on-my-machine, reproducible-builds, configuration-drift, dev-containers]
level: practitioner
status: draft
description: "Track down works-on-my-machine bugs by diffing environments systematically: versions, lockfiles, env vars, config, OS, locale, data, and making environments reproducible."
sources:
  - https://12factor.net/dev-prod-parity
  - https://containers.dev/
  - https://reproducible-builds.org/
  - https://docs.docker.com/build/building/best-practices/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Works-on-my-machine: environment differences

When code behaves differently across machines, the code is the same - something in the environment is not. Diff the environments systematically instead of guessing.

## Capture both environments
```bash
# runtime and tool versions
python -VV; pip freeze | sort > env-$(hostname).txt      # or: uv pip freeze, poetry export
node -v; npm ls --all --omit=dev > npm-tree.txt
java -version 2>&1; mvn -v; ./gradlew dependencies --configuration runtimeClasspath
go version; go env; dotnet --info
uname -a; cat /etc/os-release; ldd --version             # glibc vs musl (Alpine) differences
locale; echo $TZ; date; ulimit -a
env | sort | grep -v -i -E 'token|secret|password|key' > env-vars.txt
```
Then `diff` the outputs from the working and failing machine (or CI job vs laptop).

## Usual suspects (in order of frequency)
1. **Dependency versions:** no lockfile committed, or the lockfile ignored (`npm install` vs `npm ci`; `pip install -r` without hashes/pins; Gradle dynamic versions `1.+`). Use `npm ci`, `pip install --require-hashes`/`uv sync --frozen`, `go.sum`, Cargo.lock, `dotnet restore --locked-mode`.
2. **Environment variables and config:** a local `.env` with a value missing in CI/prod; different feature flags; config precedence (env overrides file).
3. **Runtime version:** Node 18 vs 20, Python 3.11 vs 3.12, JDK vendor/version. Pin with `.nvmrc`/`.tool-versions` (asdf/mise), `engines`, `requires-python`, Gradle toolchains, `global.json`.
4. **OS and filesystem:** case-insensitive macOS/Windows vs case-sensitive Linux (`import "./Utils"` vs `utils.ts`), path separators, CRLF vs LF (`.gitattributes`), max path length, file permissions/executable bit.
5. **Locale and time zone:** number/date parsing (`1,5` vs `1.5`), sorting/collation, default charset (Java before 18 used platform default; set `-Dfile.encoding=UTF-8`), TZ-dependent dates. See the time/locale bugs skill.
6. **Native libraries:** glibc vs musl, OpenSSL versions, CPU architecture (arm64 Mac vs amd64 CI: different wheels/binaries, Docker `--platform`).
7. **Data:** local DB has different rows, collation, or migrations not applied; caches holding stale values.
8. **Network:** proxies, corporate TLS interception (custom CA), DNS, IPv6 vs IPv4, firewall to internal services.
9. **Resources:** more CPU/memory locally hides races and OOMs that appear in a constrained container.

## Make environments reproducible
- Dev Containers (`.devcontainer/devcontainer.json`) or Nix/devbox so laptops, CI and Codespaces share an image.
- Build once, promote the same artifact/image (by digest) through environments; never rebuild per environment.
- Config validated at startup (fail fast on missing vars - pydantic-settings, envalid, `@ConfigurationProperties` with `@Validated`).
- Infrastructure as code for environments to avoid configuration drift; `terraform plan` shows drift.

## Verify
- [ ] Environment diff explains the behaviour; adding the difference to the working machine reproduces the bug.
- [ ] A guard (lockfile check, version pin, startup validation, CI matrix) prevents recurrence.
