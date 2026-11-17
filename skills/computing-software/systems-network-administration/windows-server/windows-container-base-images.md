---
id: computing-software.systems-network-administration.windows-server.windows-container-base-images
name: windows-container-base-images
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, windows-containers, windows-container-images, nanoserver-image, servercore-image, server-image, ltsc2022, ltsc2025, version-compatibility, mcr, dockerfile]
level: practitioner
status: docs-checked
description: "Choose Windows container base images (Nano Server, Server Core, Server) and tags, match container OS to host build for process isolation, and keep images patched."
sources:
  - https://learn.microsoft.com/en-us/virtualization/windowscontainers/manage-containers/container-base-images
  - https://learn.microsoft.com/en-us/virtualization/windowscontainers/deploy-containers/version-compatibility
  - https://learn.microsoft.com/en-us/virtualization/windowscontainers/deploy-containers/base-image-lifecycle
  - https://docs.docker.com/reference/dockerfile/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Windows container base images
Microsoft offers four base images, pulled from `mcr.microsoft.com`:

| Image (`mcr.microsoft.com/windows/...`) | Documented use |
|---|---|
| `nanoserver` | ultralight, for new application development on .NET (Core) and other modern frameworks; PowerShell, WMI and the Windows servicing stack are absent |
| `servercore` | medium size; supports traditional .NET Framework applications and lift-and-shift of Windows Server apps |
| `server` | slightly smaller than `windows`; full Windows API set, GPU support, no IIS connection limits |
| `windows` | largest; full Windows API set (for example the graphics device interface library missing from Server Core) |

Guidelines from the docs: full .NET Framework means Server Core; .NET Core means Nano Server; if Server Core is missing a
dependency try `windows`; for GPU acceleration consider the `server` image. Pull with an explicit tag, for example
`docker pull mcr.microsoft.com/windows/servercore:ltsc2025`.

## Version compatibility (the rule that breaks deployments)
- The compatibility tables for a Windows Server 2025 host show process isolation supported for Windows Server 2025 and
  2022 images, and Hyper-V isolation for 2025, 2022, 2019 and 2016 images. A Windows Server 2022 host supports process
  isolation for 2022 images only; a Windows Server 2019 host supports process isolation only for 2019 images.
- For any other mismatch, process isolation is blocked; Hyper-V isolation brings matching kernel binaries and does not
  depend on the host version.
- Windows 11 hosts can run process-isolated Windows Server 2022 containers (documented as a feedback feature).
- Tag explicitly (`:ltsc2022`, `:ltsc2025`); do not rely on `latest`.

## Example Dockerfile
```dockerfile
# escape=`
FROM mcr.microsoft.com/windows/servercore:ltsc2022
SHELL ["powershell", "-Command", "$ErrorActionPreference = 'Stop';"]
RUN Install-WindowsFeature Web-Server
```
The `escape` parser directive sets the character used to escape characters and newlines; the default is the backslash,
and a backtick avoids clashes with Windows paths.

## Updating
To move to a patched or newer base image, edit the Dockerfile to point at the latest base image, rebuild, push to your
registry and redeploy through your orchestrator. See the base image servicing lifecycle page for LTSC and Annual Channel
support periods.

## Verify
- [ ] The image's Windows version is covered by the compatibility table for your host and chosen isolation mode.
- [ ] Your image pipeline rebuilds when the base image is updated.

## Checked

2026-10-26 against the Windows containers docs (Virtualization-Documentation repository, last commit 2026-10-20): the four base images and their descriptions, the choice guidelines, MCR pull example, the host/container compatibility matrices (version-compatibility, updated 2025-01-23), the Windows 11 process-isolation note, and the update procedure. The Dockerfile reference (moby/buildkit) confirms the escape directive. Corrected the old claims that process isolation always needs an exact build match and that only three images exist; removed unconfirmed size figures, the MSI remark, the app-image tags, the docker inspect check and the Patch Tuesday cadence.

Method: documentation only; no commands were run.
