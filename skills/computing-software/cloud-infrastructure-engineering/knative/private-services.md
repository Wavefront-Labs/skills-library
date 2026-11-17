---
id: computing-software.cloud-infrastructure-engineering.knative.private-services
name: private-services
category: computing-software
field: cloud-infrastructure-engineering
product: knative
tags: [private-services, cluster-local, visibility, networking-knative-dev-visibility]
level: practitioner
status: docs-checked
description: "Keep a Service, Route or Kubernetes Service cluster-local with the visibility label."
sources:
  - https://knative.dev/docs/serving/services/private-services/
  - https://knative.dev/docs/serving/services/custom-domains/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: expose a Knative Service only inside the cluster.

By default Services use the `.svc.cluster.local` domain, so they are private: no public IP address and no public URL. To make Services public by default, configure a domain name, for a single Service or for all Services on a cluster.

To make an individual Service private, label the Service or Route with `networking.knative.dev/visibility=cluster-local` so it is not published to the external gateway.

Knative Service:

```bash
kubectl label kservice ${KSVC_NAME} networking.knative.dev/visibility=cluster-local
```

Route used directly without a Knative Service:

```bash
kubectl label route ${ROUTE_NAME} networking.knative.dev/visibility=cluster-local
```

Kubernetes Service:

```bash
kubectl label service ${SERVICE_NAME} networking.knative.dev/visibility=cluster-local
```

Labelling the Kubernetes Service restricts visibility more finely, for example for tagged routes; see traffic management.

Verify by running `kubectl get kservice helloworld-go` after labelling the sample Service and checking that the URL now shows the cluster-local domain.

Caution: if you create a domain mapping to a private Knative Service, that Service becomes reachable from the public internet through the mapped custom domain.

## Checked

2026-11-04. Confirmed against the Configuring private Services page (knative/docs source): the default `.svc.cluster.local` domain, configuring a domain to make Services public, the `networking.knative.dev/visibility=cluster-local` label on a Knative Service, a Route used directly and a Kubernetes Service, the finer-grained visibility note pointing to traffic management, and the helloworld-go verification showing the cluster-local URL. The domain mapping caution is confirmed by the Custom domains page (a mapping to a private Service makes it reachable from the public internet), which is now listed as a source. Nothing removed.

Method: documentation only; no commands were run.
