---
id: computing-software.cloud-infrastructure-engineering.contour.contour-xds-grpc-tls-certificates
name: contour-xds-grpc-tls-certificates
category: computing-software
field: cloud-infrastructure-engineering
product: contour
tags: [grpc-tls, certgen, contourcert, envoycert, certificate-rotation, resources-dir, sni-contour]
level: advanced
status: docs-checked
description: "Securing Contour to Envoy xDS gRPC with mutual TLS: contourcert and envoycert Secrets, required SAN contour, certgen options, manual openssl steps, rotation requirements."
sources: ["https://github.com/projectcontour/contour/blob/main/site/content/docs/main/grpc-tls-howto.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Contour to Envoy gRPC TLS

Two Secrets in `projectcontour`:
- `contourcert`: Contour's keypair for serving gRPC, plus `ca.crt` to validate Envoy's client cert. The certificate must be valid for the name `contour` (hard-coded; `contour bootstrap` passes it as the SNI server name).
- `envoycert`: Envoy's client keypair plus `ca.crt` to validate Contour. No special names required.

Obtaining them: deploy the certgen Job (`contour certgen --kube --secrets-format=compact`), run `contour certgen --kube` locally, or generate manually:

```
openssl req -x509 -new -nodes -keyout certs/cakey.pem -sha256 -days 1825 -out certs/cacert.pem -subj "/O=Project Contour/CN=Contour CA"
openssl genrsa -out certs/contourkey.pem 2048
openssl req -new -key certs/contourkey.pem -out certs/contour.csr -subj "/O=Project Contour/CN=contour"
openssl x509 -req -in certs/contour.csr -CA certs/cacert.pem -CAkey certs/cakey.pem -CAcreateserial -out certs/contourcert.pem -days 1825 -sha256 -extfile certs/cert-contour.ext
kubectl create secret -n projectcontour generic contourcert --from-file=tls.key=./certs/contourkey.pem --from-file=tls.crt=./certs/contourcert.pem --from-file=ca.crt=./certs/cacert.pem
```
(repeat for `envoycert` with `CN=envoy`). Never put the CA key in the cluster.

Rotation: generate new keypairs, update both Secrets in place (`kubectl create secret ... --dry-run -o json | kubectl apply -f -`), and the kubelet remount triggers automatic reload. Preconditions: Envoy v1.14.1 or later, and the bootstrap generated with `contour bootstrap --resources-dir` (see `03-envoy.yaml`). With the built-in job: delete job `contour-certgen`, then reapply it.

## Checked

2026-11-04. Confirmed against the Contour gRPC TLS howto (grpc-tls-howto.md): the fields, defaults, flags and behaviours stated above. Removed: nothing.

Method: documentation only; no commands were run.
