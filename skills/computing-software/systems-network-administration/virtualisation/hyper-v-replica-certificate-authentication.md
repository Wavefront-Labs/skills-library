---
id: computing-software.systems-network-administration.virtualisation.hyper-v-replica-certificate-authentication
name: hyper-v-replica-certificate-authentication
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [replica-certificate-auth, hyper-v-replica, enable-vmreplication, replica-broker, certificates, hyper-v]
level: advanced
status: docs-checked
description: "Set up Hyper-V Replica with certificate (HTTPS) authentication for non-domain or cross-forest sites: certificate requirements, listener, firewall, revocation checks and renewal."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/set-vmreplicationserver
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/enable-vmreplication
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/configure-replication-single-host
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/configure-replication-failover-cluster
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hyper-V Replica with certificate authentication

Kerberos (HTTP, port 80, payload unencrypted on the wire) works only within trusted
domains. Use certificates (HTTPS, port 443, encrypted) for workgroup hosts, separate
forests, or WAN links.

## Certificate requirements (on primary and replica servers)
- Enhanced Key Usage: **Client Authentication and Server Authentication**.
- Subject or SAN = the server's FQDN; for clusters the **Replica Broker** client access
  point FQDN (plus node names in SAN).
- An associated private key; the certificate must not be expired.
- The chain must terminate at a valid root certificate trusted on both ends.

## Configure replica server
```powershell
$thumb = (Get-ChildItem Cert:\LocalMachine\My | ? Subject -like "*hv-dr01.dr.example*").Thumbprint
Set-VMReplicationServer -ReplicationEnabled $true -AllowedAuthenticationType Certificate `
  -CertificateAuthenticationPort 443 -CertificateThumbprint $thumb `
  -ReplicationAllowedFromAnyServer $true -DefaultStorageLocation "<REPLICA_DIR>"
Enable-NetFirewallRule -DisplayName "Hyper-V Replica HTTPS Listener (TCP-In)"
```
Cluster: configure on the Hyper-V Replica Broker role, and certificates on every node.

## Enable on primary
```powershell
Enable-VMReplication -VMName app01 -ReplicaServerName hv-dr01.dr.example -ReplicaServerPort 443 `
  -AuthenticationType Certificate -CertificateThumbprint $primaryThumb -CompressionEnabled $true -ReplicationFrequencySec 300
Start-VMInitialReplication -VMName app01
Test-VMReplicationConnection -ReplicaServerName hv-dr01.dr.example -ReplicaServerPort 443 -AuthenticationType Certificate -CertificateThumbprint $primaryThumb   # optional pre-check
```

## Renewal
An expired certificate stops certificate authentication. Before expiry: enrol the new
certificate, update `Set-VMReplicationServer -CertificateThumbprint` on the replica and
`Set-VMReplication -CertificateThumbprint` on each primary VM.

## Verify
`Measure-VMReplication` shows Health Normal; `Get-VMReplicationServer` shows certificate
authentication on port 443.

## Checked
Checked 2026-10-25 against Microsoft Learn Hyper-V documentation (MicrosoftDocs/windowsserverdocs, latest commit 2026-10-23) and the Windows Server 2025 PowerShell reference (MicrosoftDocs/windows-powershell-docs, latest commit 2026-10-23). Confirmed: certificate requirements (Client and Server Authentication EKU, private key, not expired, terminates at a valid root, CN or SAN matching the host or Replica Broker FQDN), HTTPS on port 443 versus HTTP on port 80, encryption only with certificates, the firewall rule names, Set-VMReplicationServer and Enable-VMReplication certificate parameters, and Test-VMReplicationConnection. Removed because no documentation page confirmed them: the RSA 2048 minimum, the CRL requirement and the DisableCertRevocationCheck registry value, which no checked page documents.
Method: documentation only; no commands were run.
