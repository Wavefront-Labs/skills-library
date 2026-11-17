---
id: computing-software.systems-network-administration.patch-management.artifactory-and-nexus-os-repo-proxies
name: artifactory-and-nexus-os-repo-proxies
category: computing-software
field: systems-network-administration
product: patch-management
tags: [artifactory, nexus-repository, remote-repository, proxy-repository, patch-acquisition, patch-management]
level: practitioner
status: docs-checked
description: "Serve OS updates through Artifactory or Nexus proxy repositories for yum/dnf and apt: remote, virtual and group repos, metadata caching, re-signing and client config."
sources:
  - https://jfrog.com/help/r/jfrog-artifactory-documentation/rpm-repositories
  - https://jfrog.com/help/r/jfrog-artifactory-documentation/debian-repositories
  - https://help.sonatype.com/en/apt-repositories.html
  - https://help.sonatype.com/en/yum-repositories.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Artifactory and Nexus proxies for OS repositories

If the organisation already runs Artifactory or Nexus for build artifacts, they can proxy
distro repositories too: one egress point and a cache of what was downloaded.

## Artifactory
- Repository types: **local** (your own packages), **remote** (downloads from an external
  registry or another Artifactory), **virtual** (aggregates remote and local behind one
  URL). Creating one needs Admin or Project Admin permission: Administration >
  Repositories > Create a Repository, then choose the RPM or Debian package type.
- For a remote repository, verify the Repository URL (the upstream distro mirror).
- JFrog recommends a virtual repository as the default client setting for DNF.
- **RPM caveat:** `yum`/`dnf` commands that use `updateinfo.xml` are not supported for
  virtual RPM repositories, so security-advisory queries (`dnf updateinfo`) will not work
  through a virtual repo; point such clients at the remote repository directly.
- Supported RPM clients: YUM 4.18.2 and above, DNF 4.19.2 and above. DNF uses the same
  `/etc/yum.repos.d/` directory as YUM.
- Debian: client lines take the form `deb https://<JFrogPlatformURL>/artifactory/<REPO_NAME>
  <DISTRIBUTION> <COMPONENT>`. Index files of remote Debian repositories (including
  sources) are stored and renewed according to the repository's **Retrieval Cache Period**
  setting. From Artifactory 7.164.0 new Debian repositories index only amd64 by default.
- Package authenticity uses GPG signatures; Debian metadata signing and InRelease files are
  documented under "Sign Debian Metadata" and "Use Debian InRelease Metadata Files".

## Nexus Repository
- Create `yum (proxy)` with the remote URL and a blob store (there is no default Yum
  proxy). Nexus does not support new Yum v4 features.
- A `yum (group)` exposes several proxy and hosted repositories behind one URL; members are
  ordered.
- `apt (proxy)`: the **Distribution** field is optional unless **Enforce Distribution** is
  enabled, which restricts clients to one distribution (others return HTTP 404). Leaving it
  blank gives multi-distribution mode.
- **Signing Configuration** on an apt proxy: not configured, Nexus serves upstream metadata
  and caches packages; configured, Nexus generates and signs its own metadata, so clients
  must import the Nexus public key. Metadata may be missing right after configuring, and
  during a rebuild requests may return HTTP 503.

## Notes
- A proxy is not a snapshot: clients get what upstream has now. Use a snapshot or
  promotion mechanism if you need ring staging.
- A cache period that is too long delays new updates reaching clients; check the repository
  setting against how quickly you need to see new advisories.

## Verify
`dnf makecache` or `apt-get update` shows the proxy URLs; the proxy's request logs show
hits.

## Checked
2026-11-08. Confirmed against the JFrog RPM and Debian repository pages and the Sonatype
Nexus apt and yum pages: repository types, virtual-repo `updateinfo.xml` limitation, client
versions, Debian line format, Retrieval Cache Period, 7.164.0 amd64 default, Nexus
distribution enforcement, signing modes, 404 and 503 behaviour. Removed: the 600 s cache
figure, `Store Artifacts Locally`, Xray/curation, pre-warming advice, the claim that Nexus
apt proxies are per-suite only (multi-distribution mode exists), and the example client
files that depended on unverified Rocky and Ubuntu URLs.
Method: documentation only; no commands were run.
