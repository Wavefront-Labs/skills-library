---
id: computing-software.systems-network-administration.glusterfs.ssl-enable-tls
name: ssl-enable-tls
category: computing-software
field: systems-network-administration
product: glusterfs
tags: [glusterfs, ssl, tls, auth-ssl-allow, certificates]
level: advanced
status: docs-checked
description: "Enable TLS for GlusterFS I/O and management traffic: certificate files, client.ssl and server.ssl, auth.ssl-allow, certificate depth, ciphers and the secure-access file."
sources:
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Administrator-Guide/SSL.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enable TLS

Each machine needs (default names):

- `/etc/ssl/glusterfs.pem`: its own certificate
- `/etc/ssl/glusterfs.key`: its private key
- `/etc/ssl/glusterfs.ca`: concatenated certificates of the peers' signers

Mutual authentication is always performed: each side's certificate (or its signer) must be in the other's CA file.

I/O path (`client.ssl` and `server.ssl` are both required):

```
gluster volume set MYVOLUME client.ssl on
gluster volume set MYVOLUME server.ssl on
gluster volume set MYVOLUME auth.ssl-allow Zaphod
gluster volume set MYVOLUME ssl.certificate-depth 2
gluster volume set MYVOLUME ssl.cipher-list 'HIGH:!SSLv2'
```

Management path (glusterd): create the touch file on servers and on clients before mounting:

```
echo "option transport.socket.ssl-cert-depth 3" > /var/lib/glusterd/secure-access
```

Notes:

- Certificate depth defaults to 0 (only certificates directly in the CA file); raise it only with intermediate CAs.
- Clocks must be in sync or verification fails.
- No mixed mode: the TLS side rejects non-TLS connections.
- `auth.ssl-allow` names cannot contain spaces.
- The default cipher list excludes CBC modes (POODLE mitigation).
- `client.ssl` and `server.ssl` do not cover NFS or SMB client connections.

## Checked

2026-11-04: the three certificate files, mutual authentication, the no-mixed-mode rule, the clock-sync note, the I/O path options, auth.ssl-allow and its no-spaces limit, certificate depth default of zero, the cipher list and CBC exclusion, and the secure-access file for the management path were read against the glusterdocs page SSL. Nothing removed.

Method: documentation only; no commands were run.
