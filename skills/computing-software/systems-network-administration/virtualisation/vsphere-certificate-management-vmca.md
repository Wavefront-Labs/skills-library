---
id: computing-software.systems-network-administration.virtualisation.vsphere-certificate-management-vmca
name: vsphere-certificate-management-vmca
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vmca, vsphere-certificates, machine-ssl-certificate, sts-certificate, certificate-manager, subordinate-ca, custom-certificates, vsphere-security, vmware, vcenter, vsphere]
level: advanced
status: docs-checked
description: "Manage vSphere certificates: VMCA modes (default, subordinate CA, custom machine SSL), replacing via client or certificate-manager, STS expiry, ESXi certs and expiry monitoring."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-authentication-8-0/vsphere-security-certificates.html
  - https://knowledge.broadcom.com/external/article?legacyId=79248
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# vSphere certificate management (VMCA)

**Goal:** browsers trust vCenter, hosts trust each other, and no certificate expiry takes
the platform down.

## Modes
| Mode | What happens | Use |
|---|---|---|
| VMCA default | VMCA (self-signed root) issues all certs | Labs; download and trust VMCA root on admin PCs |
| **Hybrid (VMCA default with external SSL certificates)** | Custom CA-signed **machine SSL** cert for vCenter; VMCA keeps issuing other certs | Most enterprises |
| VMCA as subordinate CA | Your enterprise CA signs VMCA; all certs chain to your root | Strict PKI shops; more work at renewal |
| Full custom | Every cert from your CA, VMCA unused | Rare, high effort |

## Replace the machine SSL certificate (hybrid)
1. Client → Administration → Certificates → Certificate Management → Machine SSL →
   Actions → Generate CSR (CN and SAN = VCSA FQDN; add short name and IP if used).
2. Sign with your CA (web server template).
3. Import and replace: leaf + full chain; also add the root/intermediates to Trusted
   Root Certificates. Services restart (expect a maintenance window).
CLI fallback on the VCSA: the certificate-manager utility (see the vSphere Certificates
and Services CLI Command Reference).

## Certificates that bite
- **STS signing certificate**: expiry means nobody can log in, and the certificate expiry
  alarm does not cover the STS certificate (KB 79248). Check it with current Broadcom
  certificate tooling and renew per KB 79248 (the old `checksts.py` script is deprecated
  in favour of the vCert tool; certificate-manager option 8 manages STS signing
  certificates).
- **ESXi host certs** (VMCA-issued): renew from the host's certificate management in
  vCenter.
- Solution user certs and the VMCA root itself expire too.

## Monitor
- vCenter raises alarms ahead of certificate expiry (the STS certificate is not covered;
  see KB 79248).
- Use VDT or a script against the VCSA certificate stores (VECS) to list expiry dates;
  put them in your monitoring.

## Gotchas
- Replacing certs breaks integrations that pinned the old thumbprint (backup software,
  SRM, NSX, Aria): re-register or accept new thumbprints.
- ELM: replace on each node; trust chains must be present on all.

## Verify
Browser shows a trusted chain to your CA; VDT certificate checks pass; integrations
reconnect; expiry dates are tracked in monitoring.

## Checked
2026-10-31: VMCA modes (VMCA default, hybrid mode with external SSL certificates, manual replacement via CLI) confirmed on the vSphere Security Certificates page; the STS certificate behaviour, the deprecated checksts.py/vCert tooling, certificate-manager option 8 and the STS alarm gap confirmed in KB 79248. Removed unconfirmed figures and paths: the 5/10-year validity periods, the 30-day alarm window, `vpxd.cert.threshold`, the exact certificate-manager path and the vecs-cli command line.
Method: documentation only; no commands were run.
