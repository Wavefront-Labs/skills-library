---
id: computing-software.systems-network-administration.windows-server.gmsa-for-windows-containers
name: gmsa-for-windows-containers
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, windows-containers, credential-spec, container-gmsa, credentialspec-module, new-credentialspec, security-opt, kerberos, integrated-windows-authentication, aks-gmsa]
level: advanced
status: docs-checked
description: "Give Windows containers an AD identity with a gMSA credential spec: host authorisation, New-CredentialSpec, --security-opt, hostname rules, and Kubernetes notes."
sources:
  - https://learn.microsoft.com/en-us/virtualization/windowscontainers/manage-containers/manage-serviceaccounts
  - https://learn.microsoft.com/en-us/virtualization/windowscontainers/manage-containers/gmsa-run-container
  - https://learn.microsoft.com/en-us/virtualization/windowscontainers/manage-containers/gmsa-troubleshooting
  - https://learn.microsoft.com/en-us/virtualization/windowscontainers/manage-containers/gmsa-orchestrate-containers
  - https://github.com/MicrosoftDocs/Virtualization-Documentation/tree/main/windows-server-container-tools/ServiceAccounts
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# gMSA for Windows containers
Windows containers cannot be domain joined, but a container can run with a group Managed Service Account (gMSA) so that
Active Directory authentication works (integrated Windows authentication, Kerberos). The host gives the container the
gMSA identity through a **credential spec** file.

## 1. AD side
Create the gMSA and allow the container hosts (or a security group that contains them) to retrieve its password:
```powershell
New-ADServiceAccount -Name gmsaWebApp -DNSHostName gmsaWebApp.ad.example.com `
  -PrincipalsAllowedToRetrieveManagedPassword 'GG-ContainerHosts' -ServicePrincipalNames 'HTTP/webapp.ad.example.com'
```
Requirements for orchestrated use: container hosts that may run gMSA containers are domain joined (or use the
non-domain-joined option below), they can retrieve the gMSA passwords, and credential specs are available on each host or
uploaded to the orchestrator. The KDS root key must exist (see the gMSA documentation).

Non-domain-joined hosts: starting with Windows Server 2019, `ccg.exe` provides a plug-in mechanism that retrieves gMSA
credentials from AD using a portable user identity instead of the host computer account.

## 2. Credential spec on the host
```powershell
Install-Module CredentialSpec
New-CredentialSpec -AccountName gmsaWebApp
Get-CredentialSpec
```
Credential spec files live in the `CredentialSpecs` subdirectory of the Docker data directory. The CredentialSpec module
is published by Microsoft (aka.ms/credspec).

## 3. Run the container
```powershell
docker run --security-opt "credentialspec=file://gmsaWebApp.json" -it mcr.microsoft.com/windows/server:ltsc2022 powershell
```
Inside the container:
```powershell
nltest /sc_verify:ad.example.com     # Trusted DC Connection Status and Trust Verification Status should be NERR_Success
klist get gmsaWebApp                 # client name should be gmsaWebApp$
```
- On Windows Server 2019 and later the container identifies itself by the gMSA name on the network whatever hostname you
  give it; on Windows Server 2016 versions 1709 and 1803 the hostname had to match the gMSA SAM account name.
- Running several containers with the same gMSA at once can fail intermittently on Windows Server 2019 and later if
  `--hostname` is specified; make the hostname unique per container (or omit it).
- Docker Swarm: `docker service create --credential-spec "file://gmsaWebApp.json" <image>`.

## Kubernetes
Microsoft documents gMSA on AKS and AKS on Azure Stack HCI through its own pages and PowerShell module; for upstream
Kubernetes follow "Configure gMSA for Windows pods and containers" on kubernetes.io.

## Troubleshooting
On a domain-joined host install the AD module and run `Test-ADServiceAccount <gMSA name>`; False means the host cannot
retrieve the password, so check the host's group membership against
`(Get-ADServiceAccount <name> -Properties PrincipalsAllowedToRetrieveManagedPassword).PrincipalsAllowedToRetrieveManagedPassword`.

## Verify
- [ ] `nltest /sc_verify` inside the container succeeds and the app authenticates with the gMSA.
- [ ] A host outside the allowed group fails to start the container (shows the control works).

## Checked

2026-10-26 against the Windows containers gMSA docs (manage service accounts, run a container with a gMSA, orchestrate, troubleshooting; Virtualization-Documentation last commit 2026-10-20), the CredentialSpec module README (Install-Module, New-CredentialSpec -AccountName) and the New-ADServiceAccount reference (Windows Server 2025): credential spec option, docker run and Swarm syntax, hostname behaviour per Windows version, the concurrency warning, ccg.exe non-domain-joined support, CredentialSpecs folder, Test-ADServiceAccount check. Corrected the previous advice to always set --hostname to the gMSA name and that several containers can share a gMSA concurrently without caveat. Removed unconfirmed claims about LocalSystem and NetworkService acting as the gMSA, the webhook and CRD names and the klist krbtgt example.

Method: documentation only; no commands were run.
