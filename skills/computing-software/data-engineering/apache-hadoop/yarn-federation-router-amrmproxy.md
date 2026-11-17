---
id: computing-software.data-engineering.apache-hadoop.yarn-federation-router-amrmproxy
name: yarn-federation-router-amrmproxy
category: computing-software
field: data-engineering
product: apache-hadoop
tags: [data-engineering, apache-hadoop, yarn, federation, router, amrmproxy, sub-clusters]
level: sme
status: docs-checked
description: "YARN Federation Router and AMRMProxy setup: router interceptor pipeline and ports, NodeManager amrmproxy keys, and client yarn.resourcemanager.address pointing at the Router."
sources:
  - https://hadoop.apache.org/docs/stable/hadoop-yarn/hadoop-yarn-site/Federation.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Federation: Router and AMRMProxy

Components: sub-clusters (each a full YARN RM with work-preserving HA plus its nodes), Router (accepts submissions, applies a routing policy from the Policy Store, looks up the sub-cluster in the State Store, redirects the submission to that home sub-cluster RM, and persists the application-to-home mapping so Routers are soft-state), AMRMProxy on each NodeManager (implements ApplicationMasterProtocol; AMs are forced to talk only to it), Global Policy Generator (in this version a manual tuning process exposed via a CLI, YARN-3657), State Store and Policy Store.

Router yarn-site.xml (values below are the page's examples):
- `yarn.router.bind-host` = `0.0.0.0`
- `yarn.router.clientrm.interceptor-class.pipeline`: last step must be `org.apache.hadoop.yarn.server.router.clientrm.FederationClientInterceptor`
- `yarn.router.webapp.interceptor-class.pipeline`: last step must be `org.apache.hadoop.yarn.server.router.webapp.FederationInterceptorREST`
- Optional, example values: `yarn.router.hostname` 0.0.0.0; `yarn.router.clientrm.address` 0.0.0.0:8050; `yarn.router.admin.address` 0.0.0.0:8052; `yarn.router.webapp.address` 0.0.0.0:8089; `yarn.router.webapp.https.address` 0.0.0.0:8091; `yarn.router.submit.retry` 3; `yarn.federation.statestore.max-connections` 10; `yarn.federation.cache-ttl.secs` 60

NodeManagers:
- `yarn.nodemanager.amrmproxy.enabled` = true
- `yarn.nodemanager.amrmproxy.interceptor-class.pipeline`: for federation the last step is `org.apache.hadoop.yarn.server.nodemanager.amrmproxy.FederationInterceptor`
- Optional: `yarn.nodemanager.amrmproxy.ha.enable` (supports multiple application attempts); `yarn.federation.statestore.max-connections` example 1 and `yarn.federation.cache-ttl.secs` example 300 (kept higher or lower than the Router's because there are many AMRMProxies and the central state store must be protected)

Clients: use a separate client config set with `yarn.resourcemanager.address` = `<router_host>:8050` and `yarn.resourcemanager.scheduler.address` = `localhost:8049` (the AMRMProxy port).

Start: `$HADOOP_HOME/bin/yarn --daemon start router`, after starting the sub-clusters. Track jobs on the Router web UI (example port 8089). The AMRMProxy can throttle or kill AMs that ask for too many resources and enforce application quotas.

Verify: a job submitted with the client config appears in the Router web UI.

## Checked
2026-11-08. Read in full: the YARN Federation page (the stable URL served Hadoop 3.3.5, published 2023-03-15). Confirmed: component roles, property names and example values, pipeline last-step rules, client settings, start command. Changed: ports are examples in the property tables, not stated defaults. Removed: the sub-cluster RM appearing in the home RM as a verification claim.
Method: documentation only; no commands were run.
