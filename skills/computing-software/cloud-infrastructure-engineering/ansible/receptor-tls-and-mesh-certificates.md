---
id: computing-software.cloud-infrastructure-engineering.ansible.receptor-tls-and-mesh-certificates
name: receptor-tls-and-mesh-certificates
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, automation-mesh, receptor, receptor-tls, mesh-certificates, work-signing, hop-nodes, execution-nodes, certificate-rotation]
level: sme
status: docs-checked
description: "Understand automation mesh TLS: receptor tls-servers and tls-clients, node ID in certificates, custom mesh CA, pinning, work signing keys, and handshake failures."
sources: ["https://github.com/ansible/receptor/blob/devel/docs/source/user_guide/tls.rst", "https://github.com/ansible/receptor/blob/devel/docs/source/user_guide/workceptor.rst", "https://github.com/ansible/aap-docs/blob/main/downstream/modules/platform/proc-import-mesh-ca.adoc", "https://github.com/ansible/receptor/blob/devel/docs/source/receptorctl/receptorctl_status.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Receptor TLS and mesh certificates

Goal: every receptor peer connection uses mutual TLS, certificates are replaced before they expire, and a TLS failure is diagnosed quickly.

## How receptor TLS is configured
- Receptor supports mutual TLS for connections above and below the mesh. Define `tls-servers` and `tls-clients` blocks and reference them by name: `tls-servers` wherever receptor expects an incoming connection (`*-listeners`, `control-services`), `tls-clients` wherever it makes an outgoing one (`*-peers`, receptorctl).
- Defining a `tls-servers` entry has no effect until something references it.
```yaml
tls-servers:
  - name: myserver
    cert: /full/path/foo.crt
    key: /full/path/foo.key
    requireclientcert: true
    clientcas: /full/path/ca.crt
tcp-listeners:
  - port: 2222
    tls: myserver
---
tls-clients:
  - name: myclient
    rootcas: /full/path/ca.crt
    insecureskipverify: false
    cert: /full/path/bar.crt
    key: /full/path/bar.key
tcp-peers:
  - address: localhost:2222
    tls: myclient
```
(Two separate node files shown in one block; the `---` separates them.)
- Optional pinning: `pinnedclientcert` lists SHA256 or SHA512 fingerprints (SHA1 is not supported). Pinning is an extra requirement on top of CA signing. Get a fingerprint with `openssl x509 -in my-cert.pem -noout -fingerprint -sha256`.

## Node ID in the certificate
For above-the-mesh TLS, certificates carry the receptor node ID in `subjectAltName` `otherName` with OID `1.3.6.1.4.1.2312.19.1`. With TLS authentication in use, that OID is verified against `node.id` in the config and receptor exits if there is no match. `skipreceptornamescheck: true` on the tls-server or tls-client turns this check off (default `false`).

Receptor can generate test certificates itself with `receptor --cert-init`, `--cert-makereq` and `--cert-signreq`.

## Your own CA on a VM install
In the installer inventory set `mesh_ca_keyfile` (full path to the private RSA key) and `mesh_ca_certfile` (full path to the CA certificate), then run the installer. If you supply none, the installer generates a CA. The CA is copied to `/etc/receptor/tls/ca/` on each control and execution node.

## Work signing
Work submissions can be signed so a target node verifies the signature before starting a work unit. One RSA key pair is created offline: the public key (PKIX) goes to nodes that receive work (`work-verification: publickey:` plus `verifysignature: true` on the work type), the private key (PKCS1) to nodes that may submit work (`work-signing: privatekey:` with `tokenexpiration`, for example `30m`).
```bash
openssl genrsa -out signworkprivate.pem 2048
openssl rsa -in signworkprivate.pem -pubout -out signworkpublic.pem
```

## Inspect
```bash
openssl x509 -in /etc/receptor/tls/receptor.crt -noout -subject -enddate -ext subjectAltName
receptorctl --socket <socket_path> status
```
`receptorctl status` shows the state of the receptor network; the socket path is set by the node's control service.

## Gotchas
- A node ID that does not match the certificate makes receptor exit; reissue the certificate for the new ID.

## Verify
- [ ] `receptorctl status` on a control node lists every execution node.
- [ ] `notAfter` of every node certificate is beyond the next maintenance window.

## Checked
2026-11-09. Checked against the receptor docs (TLS support, workceptor work signing, receptorctl status) and ansible/aap-docs module "Importing a Certificate Authority (CA) certificate". Confirmed the tls-servers/tls-clients model, `requireclientcert`, `clientcas`, `rootcas`, `insecureskipverify`, pinning and fingerprint algorithms, the node-ID OID and `skipreceptornamescheck`, `mesh_ca_keyfile`/`mesh_ca_certfile`, `/etc/receptor/tls/ca/`, and the work signing key commands.
Removed as unsupported: install-bundle download path and per-node certificate file names, `mintls13` example value, regenerate-variable and installer rotation procedure, the CA-rotation sequence, port 27199 and `journalctl` advice, "30 days before expiry" alert threshold, `traceroute` example output.
Method: documentation only; no commands were run.
