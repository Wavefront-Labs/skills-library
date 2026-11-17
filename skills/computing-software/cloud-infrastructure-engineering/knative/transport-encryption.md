---
id: computing-software.cloud-infrastructure-engineering.knative.transport-encryption
name: transport-encryption
category: computing-software
field: cloud-infrastructure-engineering
product: knative
tags: [transport-encryption, cert-manager, clusterissuer, selfsigned, https-endpoints]
level: advanced
status: docs-checked
description: "Enable HTTPS endpoints for Brokers and Channels using a cert-manager ClusterIssuer."
sources:
  - https://knative.dev/docs/eventing/features/transport-encryption/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: encrypt event delivery inside the cluster without relying on a mesh.

By default, event delivery within the cluster is unencrypted. That limits events to low compliance value or forces administrators onto a service mesh or encrypted CNI. The `transport-encryption` feature flag (Beta, disabled by default) makes Knative Brokers and Channels provide HTTPS endpoints to receive events.

Because those endpoints usually lack public DNS names, such as names under `svc.cluster.local`, their certificates must be signed by a non-public CA specific to the cluster or organization. Event producers must be able to connect to HTTPS endpoints using that cluster-internal CA.

Prerequisites: the cert-manager operator installed, and Knative Eventing installed.

Setup:
1. Create a `SelfSigned` `ClusterIssuer` (`spec.selfSigned: {}`), then a root `Certificate` with `isCA: true` that uses it and writes a secret (the page uses `knative-eventing-ca`) in the cert-manager namespace. The guide uses self-signed for simplicity and points to cert-manager's docs for its limits; with a company PKI it recommends the CA issuer instead.
2. Create a second `ClusterIssuer` of type `ca` that reads that secret. Its name must be exactly `knative-eventing-ca-issuer`; every Eventing component uses it to issue server certificates.
3. Install the Eventing server certificates from the release assets: the `eventing-tls-networking.yaml` file attached to the knative/eventing release (and `eventing-kafka-tls-networking.yaml` from eventing-kafka-broker if you use Kafka components).
4. Check readiness with `kubectl get certificates.cert-manager.io -n knative-eventing`; entries such as `imc-dispatcher-server-tls` and `mt-broker-ingress-server-tls` should be READY.

Modes of the `transport-encryption` flag, set in the `config-features` ConfigMap in `knative-eventing`:
- `disabled`: current behaviour; addressables may accept events on HTTPS endpoints and producers may send to them.
- `permissive`: addressables accept and advertise both HTTP and HTTPS, and producers should prefer HTTPS when available.
- `strict`: addressables must not accept non-HTTPS and must advertise only HTTPS. This is enforced only on the Broker and Channel receiver/ingress; a broker or channel can still deliver over HTTP to a subscriber that only has an HTTP address.

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: config-features
  namespace: knative-eventing
data:
  transport-encryption: "strict"
```

Extra CA trust:
- By default Eventing clients trust the system root CAs. To add CAs, create ConfigMaps in `knative-eventing` labelled `networking.knative.dev/trust-bundle: "true"`; every data key holding a valid PEM bundle is trusted, and clients pick up changes when a new connection is made. Use a name unlikely to clash with Eventing-provided ConfigMaps. trust-manager can distribute bundles but is not required.
- To trust a CA for one sender, set `CACerts` (PEM, correctly indented multi-line string) next to the `uri` of a Trigger or Subscription subscriber, or of a source sink.
- Custom event sources built with SinkBinding get the trust bundles as a projected volume under `/knative-custom-certs`, one file per ConfigMap data key. Configure your HTTP client to use those files; how depends on the runtime.

Verify: create a Broker and read `.status.address`; it should show an `https` address with its `CACerts`. Save those certs to a file and post a CloudEvent with `curl --cacert` to the broker-ingress HTTPS URL; an HTTP 202 means accepted.

## Checked

Method: docs-checked 2026-11-09 against https://knative.dev/docs/eventing/features/transport-encryption/ (read in full). Dropped the earlier claim that the authorization page recommends `authentication-oidc`, which is not on this page.
