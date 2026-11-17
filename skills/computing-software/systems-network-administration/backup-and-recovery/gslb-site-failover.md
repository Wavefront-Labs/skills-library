---
id: computing-software.systems-network-administration.backup-and-recovery.gslb-site-failover
name: gslb-site-failover
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [gslb, global-server-load-balancing, dns-failover, health-checks, ttl, site-failover]
level: advanced
status: docs-checked
description: "Use DNS-based failover for site failover: health checks, failover records, Traffic Manager endpoints, and negative caching limits."
sources:
  - https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover.html
  - https://learn.microsoft.com/en-us/azure/traffic-manager/traffic-manager-overview
  - https://datatracker.ietf.org/doc/html/rfc2308
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DNS-based failover for site failover

DNS-based global load balancing answers queries with a healthy site, so clients move without anyone editing records during the incident.

## What the cloud services document
- **Route 53 health checks** can monitor the health of a resource such as a web server, the status of other health checks, or the status of a CloudWatch alarm. With multiple resources that perform the same function, DNS failover makes Route 53 route traffic from an unhealthy resource to a healthy one. A CloudWatch alarm per health check can notify you when its status changes. Route 53 can also use Application Recovery Controller routing control health checks with failover records.
- **Azure Traffic Manager** is a DNS-based traffic load balancer across global Azure regions. It monitors every endpoint and fails over automatically when one goes down. Endpoints can be any internet-facing service, inside or outside Azure, including on-premises (failover-to-cloud). Routing methods include lowest latency, and nested profiles combine methods.

## Design
1. **Policy**: failover (active-passive) for apps with one writable database; spread traffic across sites only if the data layer supports it.
2. **Health monitors**: monitor a real application signal, not just reachability, and decide how many failures mark a site down.
3. **TTL**: choose it deliberately; clients can only follow a change after cached answers expire. Look up the TTL and health-check interval settings of your DNS service and add them when estimating failover time.
4. The load-balancing layer itself must survive the loss of a site (a managed cloud service or redundant across sites).

## Negative caching
RFC 2308 describes negative caching: a resolver may cache an NXDOMAIN or "no data" answer for as long as the TTL on the SOA record in the response (the lower of the SOA MINIMUM field and the SOA's own TTL). So never delete records during failover; change their answers.

## Gotchas
- Split brain: both sites healthy but data diverged; active-passive needs a fenced promotion step for the database.
- Sessions break on failover unless state is shared.

## Verify
Planned test: make the primary health check fail, confirm that name lookups from several networks return the DR address, and measure user-visible downtime.

## Checked

2026-11-09. Read Route 53 "Creating health checks" page, Azure "What is Azure Traffic Manager?" and RFC 2308 (sections 1-3 on negative caching). Removed: appliance GSLB product list, Cloudflare, NS1, anycast, 30-60 second TTL figure, Java DNS cache and resolver-ignoring-TTL claims, fail-open fallback advice, the dig test command (none stated on the pages).

Method: documentation only; no commands were run.
