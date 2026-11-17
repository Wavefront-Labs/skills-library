---
id: computing-software.systems-network-administration.windows-server.windows-container-runtime-install
name: windows-container-runtime-install
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, windows-containers, containerd-windows, docker-windows-server, mirantis-container-runtime, docker-ce, nerdctl, containers-feature, install-docker-ce-ps1]
level: practitioner
status: docs-checked
description: "Install a container runtime on Windows Server: Containers feature, Docker CE/Moby via Microsoft's script or Mirantis, containerd plus nerdctl, and smoke tests."
sources:
  - https://learn.microsoft.com/en-us/virtualization/windowscontainers/quick-start/set-up-environment
  - https://learn.microsoft.com/en-us/virtualization/windowscontainers/deploy-containers/containerd
  - https://learn.microsoft.com/en-us/virtualization/windowscontainers/deploy-containers/system-requirements
  - https://github.com/microsoft/Windows-Containers/tree/Main/helpful_tools
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Install a container runtime on Windows Server
The runtimes currently supported on Windows are Moby (Docker CE), Mirantis Container Runtime and containerd.

| Runtime | When |
|---|---|
| **Docker CE / Moby** | Microsoft provides an install script; Docker CLI workflows |
| **Mirantis Container Runtime** | formerly Docker Enterprise Edition; same functionality as Docker CE plus enterprise features |
| **containerd** (+ nerdctl) | Kubernetes nodes and a Docker-compatible CLI through nerdctl |

## Docker CE via Microsoft's script
```powershell
Invoke-WebRequest -UseBasicParsing "https://raw.githubusercontent.com/microsoft/Windows-Containers/Main/helpful_tools/Install-DockerCE/install-docker-ce.ps1" -o install-docker-ce.ps1
.\install-docker-ce.ps1
docker version
```
The script configures the machine for containers (it installs the Containers feature) and installs Docker; it also has
parameters for the Docker version and a Hyper-V containers option. Read scripts before running them.

## containerd
```powershell
Invoke-WebRequest -UseBasicParsing "https://raw.githubusercontent.com/microsoft/Windows-Containers/Main/helpful_tools/Install-ContainerdRuntime/install-containerd-runtime.ps1" -o install-containerd-runtime.ps1
.\install-containerd-runtime.ps1
```
Installs containerd, nerdctl, the container OS features and the Windows CNI plug-ins; you still configure ctr and nerdctl
to use the CNI configuration that suits you. The script has `-ContainerDVersion`, `-NerdCTLVersion` and `-WinCNIVersion`
parameters.

## Operational notes
- Image layers default to the `ProgramData\docker` folder on the system drive for Docker; the daemon configuration file has a `data-root` setting to
  move it (see Docker Engine on Windows).
- Hyper-V isolation needs the Hyper-V role, and nested virtualization when the host is a VM.
- Windows Admin Center's Containers extension can install Docker on a Windows Server machine.

## Verify
- [ ] `docker version` (or `nerdctl version`) shows a working engine.
- [ ] A test container from a matching Windows base image runs.

## Checked

2026-10-26 against the Windows containers docs (set up the environment, containerd, system requirements, container storage, Docker daemon configuration) and the Windows-Containers repository helpful_tools folder (last commit 2026-10-23): supported runtimes, script URLs and file names, script parameters, Containers feature installation by the Docker script, data-root setting and the default layer folder, Hyper-V and nested virtualization requirements, Windows Admin Center install path. Corrected the containerd script name (install-containerd-runtime.ps1). Removed unconfirmed claims about DockerMsftProvider deprecation, manual Install-WindowsFeature steps, the sample hello-world commands and LCOW support.

Method: documentation only; no commands were run.
