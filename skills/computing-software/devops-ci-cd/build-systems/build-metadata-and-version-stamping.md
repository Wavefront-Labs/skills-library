---
id: computing-software.devops-ci-cd.build-systems.build-metadata-and-version-stamping
name: build-metadata-and-version-stamping
category: computing-software
field: devops-ci-cd
product: build-systems
tags: [build-systems, build-metadata, version-stamping, git-describe, build-info, ldflags, version-endpoint, semver-build-metadata, embedding-version, go-ldflags, debug-buildinfo, vcs-info, rust-built-crate, vergen, maven-git-commit-id-plugin, gradle-buildinfo, spring-boot-build-info, npm-version-injection, oci-labels, image-labels, source-date-epoch, reproducible-stamping, bazel-stamping, workspace-status, user-agent-version, sentry-release, crash-reporting-version]
level: practitioner
status: draft
description: "Make every binary and image say what it is: git describe version strings, semver build metadata, commit/date via ldflags, vergen or buildinfo plugins, OCI labels, a /version endpoint."
sources: ["https://semver.org/#spec-item-10", "https://git-scm.com/docs/git-describe", "https://pkg.go.dev/runtime/debug#BuildInfo", "https://github.com/opencontainers/image-spec/blob/main/annotations.md", "https://bazel.build/docs/user-manual#workspace-status", "https://reproducible-builds.org/docs/source-date-epoch/", "Humble & Farley, Continuous Delivery (2010), ch. 6 Build and Deployment Scripting"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Build metadata and version stamping

**Goal:** given a running process, a log line, a crash report or an image on a node, you
can name the exact commit, build and pipeline run that produced it — in one command.

## 1. The version string
Semver `MAJOR.MINOR.PATCH[-prerelease][+buildmetadata]`; build metadata (`+`) is ignored
for precedence and is where commit/build ids go. Derive from Git:
```bash
git describe --tags --always --dirty --match 'v*'
# v1.4.2            → exactly on tag
# v1.4.2-7-g3c1f2ab → 7 commits after v1.4.2, commit 3c1f2ab
# v1.4.2-7-g3c1f2ab-dirty
```
Normalise to a semver-ish string for packages/images: `1.4.2` on tags;
`1.4.3-dev.7+g3c1f2ab` (or `1.4.2-7-g3c1f2ab` as a prerelease) off-tag. Separate from the
version keep: commit SHA (full), commit timestamp, build timestamp (only if reproducibility
isn't a goal — see §6), branch, pipeline run URL/id, builder identity, dirty flag.
Shallow clones break `git describe` (`fatal: No names found`): CI must fetch tags
(`fetch-depth: 0` or `git fetch --tags --depth=…`; GitLab `GIT_DEPTH: 0` for release jobs).

## 2. Embedding per language
**Go** — link-time variables + the toolchain's own VCS info:
```go
package version
var ( Version = "dev"; Commit = "unknown"; Date = "unknown" )
func Info() string {
    bi, _ := debug.ReadBuildInfo()                // contains vcs.revision, vcs.time, vcs.modified when built from a git checkout
    return fmt.Sprintf("%s (%s %s) go=%s", Version, Commit, Date, bi.GoVersion)
}
```
`go build -trimpath -ldflags="-s -w -X example.com/app/internal/version.Version=$VERSION -X …Commit=$SHA -X …Date=$DATE"`.
`go version -m ./app` prints embedded build settings (module versions, vcs.*) — works
on any Go binary even without ldflags. Note `-buildvcs=false` disables vcs stamping.
**Rust** — `built` or `vergen` crates in `build.rs` emit `env!("VERGEN_GIT_SHA")`,
`CARGO_PKG_VERSION`; `cargo auditable` embeds the dependency list for scanners.
**Java** — `git-commit-id-maven-plugin` → `git.properties`; Spring Boot
`build-info` goal + Actuator `/actuator/info` exposes `build.version`, `git.commit.id`;
Gradle `springBoot { buildInfo() }`. Manifest attributes (`Implementation-Version`) via
the jar plugin.
**Node** — inject at build with `define` (esbuild/Vite `import.meta.env.VITE_GIT_SHA`),
or generate `build-info.json` in CI and `require` it; `process.env.npm_package_version`
at runtime from `package.json`.
**Python** — `setuptools-scm`/`hatch-vcs` derive `__version__` from tags; add a
generated `_build_info.py` (sha, date) in CI; expose via `importlib.metadata.version()`.
**.NET** — `SourceLink` + `<InformationalVersion>$(Version)+$(SourceRevisionId)</InformationalVersion>`,
`dotnet build -p:Version=1.4.2 -p:SourceRevisionId=$SHA`; `AssemblyInformationalVersion`
shows in file properties and `Assembly.GetCustomAttribute`.
**Bazel** — `--stamp` with `--workspace_status_command=tools/status.sh` emitting
`STABLE_GIT_COMMIT 3c1f…` / `BUILD_TIMESTAMP`; consume via `stamp = 1` + `x_defs`
(`rules_go`), `version_file`/`info_file` in genrules. `STABLE_` keys don't bust caches
when unchanged; volatile ones (timestamp) are excluded from the action key.

## 3. Images and packages
```bash
docker buildx build \
  --label org.opencontainers.image.revision=$SHA \
  --label org.opencontainers.image.version=$VERSION \
  --label org.opencontainers.image.source=https://github.com/example/app \
  --label org.opencontainers.image.created=$(git show -s --format=%cI HEAD) \
  --build-arg VERSION=$VERSION --build-arg COMMIT=$SHA ...
docker image inspect ghcr.io/example/app:$SHA --format '{{json .Config.Labels}}'
```
`docker/metadata-action` generates these labels automatically. Tag images with the
**commit SHA** (immutable) and the version; `latest` only for humans. Packages carry the
same version in their metadata (`package.json`, `pyproject`, `Cargo.toml`, POM) set by
the pipeline from the Git-derived string, never hand-edited on release.
Helm charts: `appVersion` = app version, `version` = chart version; stamp both.

## 4. Exposing it at runtime
- `app --version` prints the full string + commit + date + builder.
- HTTP `/version` or `/healthz` (or `/actuator/info`) returns JSON
  `{version, commit, build_time, go_version, pipeline_url}` — unauthenticated for
  internal networks, or behind auth; load balancers/monitors can poll it to confirm
  which version serves traffic (use it in deploy verification).
- Log the version once at startup and include `version`/`commit` as structured fields
  in every log line (or as resource attributes in OTel: `service.version`); crash
  reporters (Sentry `release`, Datadog `version` tag) and metrics (`build_info{version,
  commit} 1` gauge — the Prometheus convention) get the same value.
- Outbound `User-Agent: app/1.4.2 (+3c1f2ab)` helps partners and your own gateway logs.

## 5. Where the single source of truth lives
The pipeline computes `VERSION`, `SHA`, `DATE` **once** (first job) and passes them as
outputs/variables/artifacts to every build step and image — never recomputed per
language or re-derived in a later job with a different checkout depth. The same values
go into the deployment record and release notes. Tags are created by the release
pipeline (or `release-please`/`semantic-release`), not by hand, so the version string is
reproducible from Git alone.

## 6. Reproducibility vs timestamps
A build timestamp makes every build unique and breaks bit-for-bit reproducibility
(SLSA/`reproducible-builds.org` goals, Bazel cache hits). Prefer the **commit
timestamp** (`git show -s --format=%ct`) exported as `SOURCE_DATE_EPOCH` and used as the
"build date"; tools (Go, Rust `vergen` with `--idempotent`, Debian, Docker BuildKit
`--build-arg SOURCE_DATE_EPOCH`, `rewrite-timestamp=true` in `--output`) honour it. Then
two builds of the same commit produce identical artifacts *and* still say when the
source was committed. Keep the *pipeline run id* out of the binary if you want
reproducibility; put it in the provenance attestation instead.

## 7. Gotchas
- `--dirty` in CI usually means generated files weren't ignored; fix `.gitignore` rather than dropping the flag.
- Describe matching the wrong tags (`chart-1.0.0`): `--match 'v*'`/`--exclude`.
- Monorepos: per-package tags (`api/v1.4.2`) + `git describe --match 'api/v*'`, or a
  tool like `changesets`/`release-please` with per-package manifests.
- Version in `package.json` vs Git tag drift: make the pipeline the writer.
- Forgetting to stamp sidecars/CLIs/Lambda zips: every deployable artifact, not just the main service.

## Verify
- [ ] `curl /version` on a running instance returns commit + version matching the deployment record and `git describe` of that commit.
- [ ] `go version -m`/`docker image inspect` labels/`jar` manifest show the same commit as the pipeline that built it.
- [ ] Building the same commit twice yields identical artifact hashes (or identical minus a documented timestamp field).
- [ ] Crash reports and metrics carry the version; a version filter in Sentry/Grafana works.
