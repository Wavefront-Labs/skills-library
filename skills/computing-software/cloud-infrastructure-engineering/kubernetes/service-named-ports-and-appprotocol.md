---
id: computing-software.cloud-infrastructure-engineering.kubernetes.service-named-ports-and-appprotocol
name: service-named-ports-and-appprotocol
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, service, service-named-ports, appprotocol, targetport]
level: practitioner
status: docs-checked
description: "Use multi-port Services, named targetPorts to decouple Services from container ports, and appProtocol hints for meshes, gateways and load balancers."
sources: ["https://kubernetes.io/docs/concepts/services-networking/service/#multi-port-services", "https://kubernetes.io/docs/concepts/services-networking/service/#application-protocol", "https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Named ports, multi-port Services and appProtocol

## Named targetPort
```yaml
# pod template
ports:
- name: http
  containerPort: 8080
- name: metrics
  containerPort: 9090
---
# Service
spec:
  ports:
  - name: http
    port: 80
    targetPort: http          # resolved per pod
    appProtocol: http
  - name: grpc
    port: 9000
    targetPort: 9000
    appProtocol: kubernetes.io/h2c
```
`targetPort` can be a port name, so the container port number can change without editing the
Service.

## Multi-port rules
- When a Service has more than one port, every port must have a `name`.
- Port names may contain only lowercase alphanumeric characters and `-`, and must start and end
  with an alphanumeric character.
- For named ports, DNS creates SRV records of the form
  `_port-name._port-protocol.my-svc.my-namespace.svc.cluster-domain.example`.

## appProtocol
Stable since Kubernetes 1.20. A hint for implementations; the value is mirrored to Endpoints and
EndpointSlice objects. It follows label syntax. Valid values:
- IANA standard service names (for example `http`, `https`).
- Kubernetes-defined: `kubernetes.io/h2c` (HTTP/2 over cleartext), `kubernetes.io/ws`
  (WebSocket over cleartext), `kubernetes.io/wss` (WebSocket over TLS).
- Implementation-defined prefixed names such as `mycompany.com/my-custom-protocol`.

Whether a mesh, Gateway API implementation or cloud load balancer acts on the value is up to that
implementation; read its documentation.

## Gotchas
- If you use a named `targetPort`, the selected Pods must expose a port with that name.
- Renaming a Service `port` breaks anything that refers to the old name (SRV lookups,
  ServiceMonitor `port:` fields, mesh configuration).

## Verify
```bash
kubectl get endpointslices -l kubernetes.io/service-name=web -o jsonpath='{.items[*].ports}'
```

## Checked

2026-10-23, Kubernetes documentation (kubernetes/website main, v1.36 docs) and kubernetes/kubernetes source. Confirmed against the Service concept page: appProtocol stable in 1.20, accepted value forms and the three kubernetes.io values, multi-port naming rule and port-name character rules; and the DNS page for the SRV record form. Removed unconfirmed claims about mesh port-name prefixes, GKE behaviour and the exact EndpointSlice result of a missing named port.

Method: documentation only; no commands were run.
