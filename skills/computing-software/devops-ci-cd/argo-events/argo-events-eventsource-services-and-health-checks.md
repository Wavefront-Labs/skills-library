---
id: computing-software.devops-ci-cd.argo-events.argo-events-eventsource-services-and-health-checks
name: argo-events-eventsource-services-and-health-checks
category: computing-software
field: devops-ci-cd
product: argo-events
tags: [argo-events, service, clusterip, webhook, nodeport, health-check, ingress]
level: practitioner
status: docs-checked
description: "Expose HTTP-based EventSources properly: use the service field only for testing and front them with your own Service or Ingress."
sources: ["https://github.com/argoproj/argo-events/blob/master/docs/eventsources/services.md", "https://github.com/argoproj/argo-events/blob/master/docs/eventsources/webhook-health-check.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Argo events eventsource services and health checks

Webhook, GitHub, GitLab, SNS, Slack, StorageGRID and Stripe EventSources start an HTTP service to receive events. The `spec.service` field creates a `ClusterIP` Service for convenience:

```yaml
spec:
  service:
    ports:
      - port: 12000
        targetPort: 12000
  webhook:
    example:
      port: "12000"
      endpoint: /example
      method: POST
```

That generated Service is only for testing. For external access, remove `service` from the EventSource and manage exposure with native Kubernetes objects, such as a LoadBalancer Service or an Ingress. Select the EventSource pods with the label `eventsource-name: <name>`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: webhook-eventsource
spec:
  ports:
    - port: 12000
      protocol: TCP
      targetPort: 12000
  selector:
    eventsource-name: webhook
  type: NodePort
```

If your load balancer or Ingress needs a health check endpoint, webhook EventSources (and the extended types such as GitHub, GitLab, SNS, Slack, StorageGRID and Stripe) also create `:${port}/health` for each configured port. An HTTP GET to it returns the text `OK` with status 200.

## Checked

2026-11-04. Confirmed against the EventSource Services page (affected types, `spec.service` for a ClusterIP Service for testing only, both YAML examples, the `eventsource-name` selector, LoadBalancer Service or Ingress for external access) and the Webhook Health Check page (`:${port}/health`, `OK`, 200). Removed the claim that `service` "only accepts ports", which the page does not state.
Method: documentation only; no commands were run.
