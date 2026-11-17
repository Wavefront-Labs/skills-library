---
id: computing-software.cloud-infrastructure-engineering.azure.azure-artifacts-feeds-and-upstream-sources
name: azure-artifacts-feeds-and-upstream-sources
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-devops, azure-artifacts, package-feeds, upstream-sources, nuget-feeds, npm-feeds, maven-feeds, python-feeds, pypi-feeds, cargo-feeds, universal-packages, feed-views, release-views, package-promotion, retention-policies, feed-permissions, project-scoped-feeds, organization-scoped-feeds, package-versioning, semver, immutable-packages, dependency-confusion, artifact-storage-billing, pipeline-authentication, credential-provider]
level: practitioner
status: docs-checked
description: "Run Azure Artifacts as the single package source: feeds, upstream sources (dependency-confusion rule), views and promotion, retention, permissions, pipeline auth."
sources: ["https://learn.microsoft.com/azure/devops/artifacts/concepts/upstream-sources", "https://learn.microsoft.com/azure/devops/artifacts/reference/limits", "https://learn.microsoft.com/azure/devops/artifacts/concepts/views", "https://learn.microsoft.com/azure/devops/pipelines/tasks/reference/pip-authenticate-v1", "https://learn.microsoft.com/azure/devops/pipelines/tasks/reference/npm-authenticate-v0", "https://learn.microsoft.com/azure/devops/pipelines/tasks/reference/nuget-authenticate-v1"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Azure Artifacts — one feed per audience, upstreams on, public registries off

**Goal:** builds pull every dependency through a feed you control (cached, scanned,
immutable), internal packages are versioned and promoted through views, and no
build can be hijacked by a public package with your internal name.

## 1. Feeds
```text
Feed administration is portal/REST; the CLI covers `az artifacts universal publish/download`.
Portal: Artifacts → Create feed → name, visibility (members of org/project | specific people), scope (project recommended), upstream sources (on).
```
- **Project-scoped** feeds (recommended; inherit project permissions, show in the project) vs **organization-scoped** (legacy, cross-project convenience). One feed per *audience/trust level*, not per team: `platform-internal` (your packages), `approved-public` (upstream cache of nuget.org/npmjs/PyPI/Maven Central with saved versions), maybe `experimental`.
- Protocols in one feed: NuGet, npm, Maven, Python, **Cargo**, Universal Packages (any files, versioned, `az artifacts universal publish --feed f --name tool --version 1.2.0 --path ./dist`).
- Visibility ≠ permissions: *Reader* (consume), *Collaborator* (save upstream packages), *Contributor* (push), *Owner*. The project **Build Service** identity needs Contributor to publish from pipelines; consumers' build services need Reader (grant at feed → Permissions, or tick *Allow project-scoped builds*).

## 2. Upstream sources and dependency confusion
- Upstreams (`nuget.org`, `npmjs.com`, `pypi.org`, Maven Central, other Azure feeds, crates.io): first request fetches and **saves** the exact version into the feed; subsequent builds get it from the feed even if the upstream deletes/unpublishes. Pin versions; builds become reproducible and offline-tolerant.
- **Rule**: clients configure **only** the Azure feed (`nuget.config` with `<clear/>` then the single source; `.npmrc` `registry=` only; `pip.conf`/`PIP_INDEX_URL` only — no `--extra-index-url`). Mixing public + private indexes is the dependency-confusion vector (an attacker publishes `your-internal-lib 99.0.0` on PyPI).
- Search order for a package name: packages published directly to the feed → packages saved from an upstream → upstream sources in the order listed in the feed's configuration. For internal names: publish them to the feed *before* anyone asks, and claim the names on public registries or use scoped/prefixed names. You can't publish a version that already exists in an enabled upstream; to override one, disable the upstream, publish, then re-enable it.
- Upstream order: Microsoft recommends public registries first; put an upstream holding your rebuilt/patched OSS packages before the public ones.
- Allow-list upstream packages? Not native — use a *vetted* feed with upstreams **off** that only contains promoted packages (see views) if policy requires approval per package, fed from a *staging* feed with upstreams on.
- Custom upstream sources (other than Azure Artifacts feeds and the public registries) are supported for npm packages only.

## 3. Versioning, views, promotion, retention
- Package versions are **immutable**: a version can't be overwritten. Use SemVer: `1.4.0-ci.20261014.3` prerelease from CI, `1.4.0` on release.
- **Views**: new feeds use `@Local` by default (packages published to the feed plus those saved from upstreams); you can promote packages to `@Release` and other views. **Promote** a tested version to `@Release`; consumers of `https://pkgs.dev.azure.com/<org>/<project>/_packaging/<feed>@Release/nuget/v3/index.json` only ever see promoted versions. Promotion = your "approved packages" mechanism, including for upstream-cached packages.
- **Retention policies** automatically delete older package versions to manage storage; each organization gets 2 GiB of free storage, and at that limit you can't publish new packages until you delete packages or set up billing.

## 4. Pipelines: publish and consume
```yaml
- task: NuGetAuthenticate@1            # sets credential provider env for dotnet/nuget; works with the feed URL in nuget.config
- script: dotnet restore --configfile nuget.config && dotnet pack -c Release -o $(Build.ArtifactStagingDirectory) /p:Version=$(semver)
- task: NuGetCommand@2
  inputs: { command: push, packagesToPush: '$(Build.ArtifactStagingDirectory)/*.nupkg', nuGetFeedType: internal, publishVstsFeed: 'Platform/platform-internal' }
- task: npmAuthenticate@0
  inputs: { workingFile: .npmrc }       # then npm ci / npm publish
- task: PipAuthenticate@1
  inputs: { artifactFeeds: 'Platform/platform-internal', onlyAddExtraIndex: false }   # sets PIP_INDEX_URL; keep onlyAddExtraIndex false
- task: MavenAuthenticate@0
  inputs: { artifactsFeeds: platform-internal }
- task: UniversalPackages@0
  inputs: { command: download, vstsFeed: 'Platform/platform-internal', vstsFeedPackage: tool, vstsPackageVersion: '1.*', downloadDirectory: $(Pipeline.Workspace)/tool }
```
- Authentication tasks use the build's `System.AccessToken`; the build service needs feed permission (the classic 401/403 on push). Outside pipelines use each protocol's credential provider or a PAT with a Packaging scope and short expiry — PATs expire; prefer pipelines for publishing and developers only read.
- Publish once per version: pipelines that rerun and try to push the same version fail — version from the run (`$(Build.BuildNumber)` or GitVersion) and treat "version exists" as a stop, not a retry.
- Caching tasks (`Cache@2`) still help; the feed is network, the cache is disk.

## 5. Operate
- Storage: retention policies and deleting old prereleases are the levers; see the billing settings and the limits page for storage and per-package size limits.
- Audit: review feed permission changes and package deletes in the org audit log.
- Secure the chain: Advanced Security dependency scanning reads the restored graph (see devsecops skill); Defender/third-party scanners can pull from the feed as Reader; block a known-bad version by **deprecating**/unlisting it in the feed (consumers get warnings) or deleting it (builds fail — intended).
- Mirror strategy for air-gapped: Universal Packages of vendor drops; `nuget.exe`/`npm pack` + push into the feed from a connected agent.

## Gotchas
- A public package first requested through an upstream becomes *your* saved copy; later upstream version yanks don't propagate — good for reproducibility, bad if the yank was for malware: subscribe to advisories and deprecate locally.
- `onlyAddExtraIndex: true` on `PipAuthenticate` re-introduces dependency confusion for Python (public PyPI remains the primary index).
- Feed `@Release` view URLs are per-protocol; a `nuget.config` pointing at `@Local` in dev and `@Release` in prod builds yields "works on my machine".
- Deleting a feed breaks every pipeline that uses it immediately.
- Build Service identity differs per project (`<Project> Build Service (<org>)`); cross-project consumption needs that project's build service added as Reader on the feed.

## Verify
- [ ] Every repo's `nuget.config`/`.npmrc`/`pip.conf`/`settings.xml` references only the Azure feed (`<clear/>`); a grep for `nuget.org`/`registry.npmjs.org`/`pypi.org` in repos returns nothing.
- [ ] Publishing `platform-internal` package `1.4.0` twice fails the second time (immutability); promoting it to `@Release` makes it visible on the Release view URL and invisible before.
- [ ] A restore on a clean agent with the public internet blocked (firewall rule) succeeds for all cached packages.
- [ ] Retention policy set on every feed; storage trend flat month over month; feed permissions list has no individual users (groups + build services only).

## Checked

2026-10-28. Confirmed against Microsoft Learn pages: upstream search order, saved packages and immutability, override-by-disable workflow, @Local and @Release views, custom upstreams for npm only, 2 GiB free storage, auth task input names.

Removed because not confirmed: the 30-day recycle bin, retention example figures, REST promotion call, Packaging audit events, npm always-auth and Maven repository claims, and credential tool names.

Method: documentation only; no commands were run.
