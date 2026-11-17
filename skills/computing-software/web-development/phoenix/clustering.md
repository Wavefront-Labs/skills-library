---
id: computing-software.web-development.phoenix.clustering
name: clustering
category: computing-software
field: web-development
product: phoenix
tags: [phoenix, dnscluster, epmd, clustering, libcluster, pubsub, long-polling, releases]
level: sme
status: docs-checked
description: "Cluster Phoenix nodes: DNS discovery in rel/env.sh.eex, libcluster alternatives, epmd-less setup, and long-polling caveats."
sources:
  - https://github.com/phoenixframework/phoenix/blob/main/guides/deployment/clustering.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: connect several instances of a Phoenix app so they pass messages between nodes.

Clustering needs two things: node connection (an Erlang VM feature) and service discovery (finding all instances' IPs). Phoenix ships `dns_cluster` for DNS-based discovery.

## DNS discovery
Put the config in `rel/env.sh.eex`, which runs before the release starts:

```sh
# Uncomment if IPv6 is required
# export ECTO_IPV6="true"
# export ERL_AFLAGS="-proto_dist inet6_tcp"

# Erlang uses a port mapper daemon on each node,
# it by default runs on port 4369
export ERL_EPMD_PORT=4369

# Use the ports 4370-4372 for nodes to communicate.
export ERL_AFLAGS="-kernel inet_dist_listen_min 4370 inet_dist_listen_max 4372"

export RELEASE_DISTRIBUTION="name"
export RELEASE_NODE="app-${PLATFORM_DEPLOYMENT_SHA}@${PLATFORM_DEPLOYMENT_IP}"
export DNS_CLUSTER_QUERY="your-app.internal"
```

- Ports 4369-4372 are used; you may need to expose them as internal TCP ports on your platform, besides the HTTP port.
- Fully qualified node names include the deployment sha (so each deployment forms its own cluster) and the IP. The variable names `PLATFORM_DEPLOYMENT_SHA` and `PLATFORM_DEPLOYMENT_IP` are platform specific. If no IP is available, it may be computed as `NODE_IP=hostname | tr -d ' '`.
- `DNS_CLUSTER_QUERY` is the DNS query used to find the other instances.

Fly.io, Railway and Render provide private networks with DNS querying; adapt `DNS_CLUSTER_QUERY`. Digital Ocean App Platform and Northflank let nodes connect directly but have no DNS discovery.

## Alternatives to DNS
- `libcluster`: strategies using gossip protocols, kubernetes, ec2 and others.
- `libcluster_postgres`: a libcluster plugin using PostgreSQL for discovery, no extra setup if you already use Postgres.

With these you can likely remove `dns_query` from your dependencies.

## epmd-less deployment
To use a single fixed distribution port, remove these two lines from `rel/env.sh.eex`:
```sh
export ERL_EPMD_PORT=4369
export ERL_AFLAGS="-kernel inet_dist_listen_min 4370 inet_dist_listen_max 4372"
```
Add `rel/vm.args.eex`:
```
-start_epmd false -erl_epmd_port 6789
```
Add `rel/remote.vm.args.eex`:
```
-start_epmd false -erl_epmd_port 6789 -dist_listen false
```
Now only port 6789 (plus HTTP) must be exposed between instances.

## Long-polling with multiple machines
The generated endpoint offers WebSocket and Long-Polling (`longpoll: [connect_info: [session: @session_options]]`), and the client falls back after `longPollFallbackMs: 2500` set in `app.js`. With more than one machine, long-polling works only if at least one holds:
1. you use Erlang clustering so the default `Phoenix.PubSub` adapter broadcasts across nodes;
2. you pick another `Phoenix.PubSub` adapter such as `Phoenix.PubSub.Redis`;
3. your deployment uses sticky sessions.

Reason: each long-poll request looks for the user's stateful process; if unreachable, every request creates a new process and state, breaking the socket's long-lived behaviour.

## Checked

Date: 2026-11-07

Confirmed: read each cited page in full, including embedded code snippets and command output, and matched every claim, command, option, function name and default line by line against the page text. Where a source is a repository guide, the guide markdown on the main branch was read.

Removed or changed: Source switched to the guide in the Phoenix repository because the guide is not published on hexdocs.

Method: documentation only; no commands were run.
