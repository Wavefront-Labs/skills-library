---
id: computing-software.qa-testing-engineering.jmeter-k6.jmeter-docker-kubernetes
name: jmeter-docker-kubernetes
category: computing-software
field: qa-testing-engineering
product: jmeter-k6
tags: [jmeter-docker, jmeter-kubernetes, distributed-jmeter-containers, load-generator-image]
level: practitioner
status: docs-checked
description: "Run JMeter in Docker and Kubernetes: build a pinned image with plugins, run non-GUI tests with mounted plans, distributed controller/worker pods, RMI ports and results collection."
sources:
  - https://jmeter.apache.org/usermanual/remote-test.html
  - https://jmeter.apache.org/usermanual/get-started.html#non_gui
  - https://jmeter.apache.org/download_jmeter.cgi
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Running JMeter in Docker and Kubernetes

## Image
```dockerfile
FROM <JRE or JDK image, Java 17 or newer>
ARG JMETER_VERSION=5.6.3
# download apache-jmeter-<version>.tgz from the Apache JMeter download page
# (older releases are on the Apache archive) and verify its checksum
ARG JMETER_TGZ_URL
RUN curl -fsSL "$JMETER_TGZ_URL" | tar -xz -C /opt \
 && ln -s /opt/apache-jmeter-${JMETER_VERSION} /opt/jmeter
ENV PATH=/opt/jmeter/bin:$PATH
WORKDIR /tests
ENTRYPOINT ["jmeter"]
```
JMeter requires Java 17 or newer. Pin the JMeter and Java versions; install plugins as described in the plugins manager skill.

## Single container run
```bash
docker run --rm -v "$PWD":/tests -e HEAP="-Xms2g -Xmx2g" my/jmeter:5.6.3 \
  -n -t plan.jmx -l out/run.jtl -e -o out/report -Jhost=staging.example.com
```

## Distributed in Kubernetes
- Worker pods run `jmeter-server` with `-Dserver.rmi.localport=50000 -Dserver_port=1099 -Dserver.rmi.ssl.disable=true` (or set up the RMI keystore); a headless Service exposes them.
- Controller pod runs `jmeter -n -t plan.jmx -R <worker-ip-list> -l run.jtl` (gather pod IPs via the headless service DNS).
- Each worker runs the **full** plan: divide threads by worker count in properties (`-Gthreads=...`).
- Data files are not sent by the controller, so they must exist on every worker (bake into image or mount a ConfigMap/volume).

Simpler alternative: run N independent non-GUI pods (a Job with `parallelism: N`), each writing its own JTL to shared storage, then merge JTLs and generate one dashboard (`jmeter -g merged.jtl -o report`).

## Gotchas
- RMI needs connectivity both ways (the controller also listens on `client.rmi.localport`); NAT or pod networking breaks it unless ports are fixed and reachable.
- Size generator pod CPU and memory requests to the heap (`HEAP` defaults to 1 GB) and thread count.

## Verify
Total throughput across workers equals the target and no pod is CPU-throttled.

## Checked
Checked against the Apache JMeter user manual sources (apache/jmeter, xdocs/usermanual and bin/, master as of 2026-10-01; latest release 5.6.3). Confirmed: Java 17+ requirement, `HEAP` default, full plan per server, data files not sent, RMI properties, `-R`/`-G`. Removed the unconfirmed base image tag, download URL, plugin-install commands and CPU threshold.

Method: documentation only; no commands were run.
