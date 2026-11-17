---
id: computing-software.systems-network-administration.windows-server.nps-server-certificate-for-peap-eap-tls
name: nps-server-certificate-for-peap-eap-tls
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, nps, nps-server-certificate, peap, eap-tls, certificate-templates]
level: advanced
status: docs-checked
description: "Choose and deploy the NPS server certificate for PEAP and EAP-TLS: template, EKU and SAN, selecting it in network policy, renewal, and client trust settings."
sources:
  - https://learn.microsoft.com/en-us/windows-server/networking/technologies/nps/nps-manage-cert-requirements
  - https://learn.microsoft.com/en-us/windows-server/networking/technologies/nps/nps-manage-certificates
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NPS server certificate for PEAP and EAP-TLS

Clients authenticate the NPS server by its certificate before sending credentials. Certificates that do not meet the
requirements are not even offered in the NPS certificate drop-down.

## Requirements (server certificate)
- Chains to a trusted root CA, with the `Server Authentication` purpose in the EKU (OID 1.3.6.1.5.5.7.3.1).
- Subject name not blank (a blank-subject certificate is not available for NPS authentication).
- If a Subject Alternative Name is used, it must contain the server's DNS name.
- Key size: the docs give a minimum key size of 2048 as an example setting.
- Private key on the NPS server; clients must trust the issuing root.

## Template
Configure the AD CS certificate template as described in "Configure Certificate Templates for PEAP and EAP requirements": Subject name built from AD with a name format other than None, DNS name in the alternate subject name, Server Authentication purpose. Enable autoenrollment on the NPS servers if you can.

## Select it in NPS
Network Policies > Constraints > Authentication Methods > EAP Types > the EAP type > Edit > **Certificate issued to**. Each policy using certificate-based authentication stores its own selection.

## Expiry
Without autoenrollment, the certificate bound to a policy is not updated automatically when it expires; each affected policy must be edited to select the new certificate, then restart the Network Policy Server (IAS) service:
```cmd
net stop ias && net start ias
```
With autoenrollment, the certificate is renewed before expiry and NPS keeps using the renewed one. Export the NPS configuration and read the thumbprint in the EAP configuration to confirm which certificate a policy uses.

## Clients
Client certificate requirements for EAP-TLS: Client Authentication purpose (1.3.6.1.5.5.7.3.2); user certificates carry the UPN in the SAN, computer certificates the client FQDN (DNS name). Configure clients to validate the server certificate and trusted root.

## Verify
- [ ] A test client authenticates without a trust prompt; the certificate expiry is tracked.

## Checked

2026-10-25, against the MicrosoftDocs/windowsserverdocs repository (main, last commit 2026-10-23), the windows-powershell-docs NPS cmdlet pages and the MicrosoftDocs/entra-docs repository. Confirmed the server certificate requirements (Server Authentication EKU and OID, non-blank subject, DNS name in the SAN, 2048-bit example), client certificate requirements, per-policy certificate selection, the manual renewal procedure with net stop ias and net start ias for non-autoenrolled servers, and that autoenrollment keeps NPS on the renewed certificate. Corrected: the old skill said autoenrollment renewal leaves NPS on the old thumbprint. Removed the unconfirmed template name, validity period and certutil -pulse advice.

Method: documentation only; no commands were run.
