---
id: computing-software.systems-network-administration.windows-server.windows-container-volumes-and-bind-mounts
name: windows-container-volumes-and-bind-mounts
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, windows-containers, windows-container-volumes, bind-mounts, docker, smb-global-mapping]
level: practitioner
status: docs-checked
description: "Persist data from Windows containers with named volumes, bind mounts and SMB global mappings: path syntax, permissions for ContainerUser, and isolation limits."
sources:
  - https://learn.microsoft.com/en-us/virtualization/windowscontainers/manage-containers/persistent-storage
  - https://learn.microsoft.com/en-us/virtualization/windowscontainers/manage-containers/container-storage
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Windows container volumes and bind mounts
`<CTR>:` stands for the container's system drive letter.

Containers use ephemeral scratch space by default; file writes are captured in the scratch space and do not reach the
host, and are lost when the container is removed. Persist data with a bind mount or a named volume.

## Named volumes
```powershell
docker volume create appdata
docker run -v appdata:<CTR>:\data <image>
```
The Docker engine on Windows has a built-in named volume plugin for local volumes. Windows converts the in-container
target path to lower case (a target of `<CTR>:\MyData` becomes `<CTR>:\mydata`).

## Bind mounts
```powershell
docker run -v <host dir>:<CTR>:\data:RO <image>      # read-only
docker run -v <host dir>:<CTR>:\data:RW <image>      # read-write (default)
```
- Bind-mounting directly on cluster shared volumes (CSV) is not supported.
- Symlinks are resolved in the container; a bind-mounted path that is or contains symlinks is not accessible.
- Do not bind-mount sensitive directories such as the system drive root into an untrusted container.

## Permissions
- Hyper-V isolation: the host files are accessed as `LocalSystem`; if access is denied, make sure `LocalSystem` has access
  to the host directory. With the read-only flag, changes are not visible or persisted.
- Process isolation: file ACLs are honoured using the identity of the container process (`ContainerAdministrator` on Server
  Core, `ContainerUser` on Nano Server by default). These identities exist only inside the container, so grant a
  well-known group such as `Authenticated Users` on the host folder.

## SMB global mapping (Windows Server 1709 and later)
```powershell
$creds = Get-Credential
New-SmbGlobalMapping -RemotePath \\fs01\share1 -Credential $creds -LocalPath <MAP>:
docker run -it --name demo -v <MAP>:\ContainerData:<CTR>:\AppData1 <image> cmd.exe
```
The container needs no server, share or credentials; the host handles them. All users and applications on the container
host can access the mapped share. It works with any compatible SMB server (Scale-Out File Server, Azure Files, traditional
file servers, NAS appliances). DFS Namespace folders are not supported.

## Verify
- [ ] Data written in the container survives `docker rm -f`, and a new container on the same volume sees it.

## Checked

2026-10-26 against the Windows containers persistent storage and container storage pages (Virtualization-Documentation, last commit 2026-10-20): ephemeral scratch behaviour, named volume and bind mount syntax with :RO and :RW, the CSV and symlink limitations, LocalSystem and ContainerAdministrator or ContainerUser permission model, lower-casing of target paths, SMB global mapping steps, exposure to all host users and DFSN limitation. Removed unconfirmed claims about single-file bind mounts, container paths needing the C: drive, drive-letter targets, the Mountpoint output and Kubernetes CSI SMB advice.

Method: documentation only; no commands were run.
