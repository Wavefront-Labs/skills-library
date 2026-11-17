---
id: computing-software.cloud-infrastructure-engineering.kubernetes.openssl-certificate-inspection
name: openssl-certificate-inspection
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, certificates, openssl-x509, pki, tls-troubleshooting]
level: practitioner
status: docs-checked
description: "Inspect Kubernetes certificates with openssl: subject, SANs, expiry, issuer chain, key match, and the live cert a server presents on 6443 or 10250."
sources: ["https://kubernetes.io/docs/tasks/administer-cluster/certificates/", "https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-certs/", "https://docs.openssl.org/master/man1/openssl-x509/", "https://docs.openssl.org/master/man1/openssl-s_client/", "https://docs.openssl.org/master/man1/openssl-verify/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Inspecting certificates with openssl

## File on disk
```bash
openssl x509 -in /etc/kubernetes/pki/apiserver.crt -noout -subject -issuer -dates
openssl x509 -in /etc/kubernetes/pki/apiserver.crt -noout -ext subjectAltName
openssl x509 -in cert.crt -noout -text | less          # everything, incl. key usage
openssl x509 -in cert.crt -noout -checkend 2592000     # exit 1 if it expires within 30 days
```

## Embedded in a kubeconfig
```bash
kubectl config view --raw -o jsonpath='{.users[0].user.client-certificate-data}' | base64 -d \
  | openssl x509 -noout -subject -enddate
```
Subject `O=` values are groups, `CN=` is the username.

## Live certificate presented by a server
```bash
openssl s_client -connect 10.0.0.11:6443 -servername kubernetes </dev/null 2>/dev/null \
  | openssl x509 -noout -subject -dates -ext subjectAltName
openssl s_client -connect <node>:10250 </dev/null 2>/dev/null | openssl x509 -noout -issuer -dates   # kubelet serving
```
If the live cert differs from the file, the process has not reloaded since renewal (restart the
static pod).

## Chain and key checks
```bash
openssl verify -CAfile /etc/kubernetes/pki/ca.crt /etc/kubernetes/pki/apiserver.crt
diff <(openssl x509 -in tls.crt -noout -pubkey) <(openssl pkey -in tls.key -pubout) && echo key matches
```

## From a Secret
```bash
kubectl get secret web-tls -o jsonpath='{.data.tls\.crt}' | base64 -d | openssl x509 -noout -subject -enddate -ext subjectAltName
```

## Gotchas
- `-ext` is documented in the current OpenSSL x509 manual; if your build lacks it, grep the `-text` output for "Subject Alternative Name".
- To inspect every certificate in a PEM bundle, the current OpenSSL x509 manual documents `-multi` (prints information about all certificates in the input); check your OpenSSL version's manual before relying on it.

## Checked

2026-10-27. Release: OpenSSL manual (master), Kubernetes v1.37 docs, October 2026
- Confirmed in the OpenSSL x509 manual the options `-subject`, `-issuer`, `-dates`, `-enddate`, `-ext`, `-pubkey`, `-multi` and `-checkend` (exits nonzero if the certificate expires within the given seconds); confirmed `-servername` in the s_client manual, `-pubout` in the pkey manual and `-CAfile` in the verify manual.
- Confirmed in the Kubernetes docs that the API server listens on 6443 and the kubelet API on 10250, that the certificate common name is the user name and organization fields are groups, and that control-plane static pods must be restarted after renewal because dynamic certificate reload is not supported for all components.
- Removed the unverified OpenSSL 1.1.1 version claim, the unconfirmed 'reads only the first certificate' statement and the `crl2pkcs7` pipeline.

Method: documentation only; no commands were run.
