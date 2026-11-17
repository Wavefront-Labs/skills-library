---
id: computing-software.systems-network-administration.windows-server.windows-container-dockerfiles
name: windows-container-dockerfiles
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-containers, windows-dockerfile, windows-container-images, servercore-image, docker-windows-server]
level: practitioner
status: docs-checked
description: "Write Dockerfiles for Windows images: base image tags matching the host, SHELL for PowerShell, layer cleanup, escape character, installing MSIs and features."
sources:
  - https://learn.microsoft.com/en-us/virtualization/windowscontainers/manage-docker/manage-windows-dockerfile
  - https://learn.microsoft.com/en-us/virtualization/windowscontainers/manage-docker/optimize-windows-dockerfile
  - https://learn.microsoft.com/en-us/virtualization/windowscontainers/manage-containers/container-security
  - https://docs.docker.com/reference/dockerfile/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dockerfiles for Windows containers

## Skeleton
```dockerfile
# escape=`
FROM mcr.microsoft.com/windows/servercore:ltsc2022
SHELL ["powershell", "-NoProfile", "-Command", "$ErrorActionPreference = 'Stop'; $ProgressPreference = 'SilentlyContinue';"]
RUN Install-WindowsFeature Web-Server
COPY site/ /inetpub/wwwroot/
EXPOSE 80
```
- `# escape=` followed by a backtick makes backtick the escape and line-continuation character (default is backslash), so
  Windows paths are not mangled.
- `SHELL` changes the shell used by the shell form of `RUN`; `$ErrorActionPreference = 'Stop'` makes PowerShell errors
  fail the build.
- Setting `$ProgressPreference` to `SilentlyContinue` gives faster downloads (documented for `Invoke-WebRequest`).
- Exec-form instructions on Windows need escaped backslashes: `RUN ["powershell", "New-Item", "<CTR>:\\test"]`.
- The destination in `COPY` and `ADD` must use forward slashes on Windows; a backslash destination does not work.

## Base image tag and host
Process isolation depends on the host/container Windows versions: check the compatibility matrix (for example a Server
2022 host runs 2022 images but not 2019 images in process isolation). Use `--isolation=hyperv` when versions do not match
and Hyper-V isolation supports them.

## Layers and size
- Each `RUN` creates a new layer; group download, install and cleanup in one `RUN` so installers are not left in a
  layer.
- Nano Server images lack PowerShell and the .NET Framework; build on Server Core and copy output into Nano Server with a
  multi-stage build.
- Install packages with `Start-Process <installer> -ArgumentList '<silent switches>' -Wait` inside PowerShell.

## Long-running services
Containers need a foreground process. The IIS and ASP.NET images use `ServiceMonitor.exe` (for example
`ServiceMonitor.exe w3svc`) as the entrypoint, which configures IIS and monitors the service; LogMonitor can wrap
another process to relay logs.

## Gotchas
- Name the file `Dockerfile` with no extension.

## Verify
- [ ] `docker build` succeeds; `docker image history` shows no leftover installer layers.

## Checked

2026-10-26 against the Windows containers docs (Dockerfile on Windows, optimize Dockerfile, container security and troubleshooting pages; Virtualization-Documentation last commit 2026-10-20) and the Dockerfile reference in moby/buildkit (escape directive, SHELL): COPY and ADD forward-slash rule, escaped backslashes in exec form, one layer per RUN, ProgressPreference tip, ServiceMonitor.exe entrypoint, Nano Server contents. Corrected the old statement that COPY accepts escaped backslashes. Removed unconfirmed claims about .dockerignore behaviour, `setx PATH`, msiexec switches and the ServiceMonitor ENTRYPOINT literal.

Method: documentation only; no commands were run.
