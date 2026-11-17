---
id: computing-software.data-science-and-analytics.apache-superset.ssh-tunneling
name: ssh-tunneling
category: computing-software
field: data-science-and-analytics
product: apache-superset
tags: [ssh-tunneling, bind-address, private-database, bastion, feature-flag]
level: advanced
status: docs-checked
description: "Reach private databases from Superset over SSH: the SSH_TUNNELING feature flag, SSH_TUNNEL_LOCAL_BIND_ADDRESS and the database connection toggle."
sources:
  - https://github.com/apache/superset/blob/master/docs/admin_docs/configuration/networking-settings.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: connect to a database that is only reachable through an SSH host.

1. Turn on the feature flag in `superset_config.py`:

```python
FEATURE_FLAGS = {"SSH_TUNNELING": True}
```

2. Optional hardening and placement:
- `SSH_TUNNEL_LOCAL_BIND_ADDRESS` is the host address where the tunnel will be accessible on your VPC.
- To add security when establishing the tunnel, you can overwrite the `SSHTunnelManager` class.

3. Create the database with the SSH tunnel enabled: with the flag on, the connection form shows an SSH tunnel toggle. Enable it and add credentials. Two authentication types are supported, Basic and Private Key; the credentials come from your service provider.

4. Verify data is flowing by running a query in SQL Lab.

## Checked

2026-11-08. Confirmed against the "SSH Tunneling" section of the Network and Security Settings page (page read in full). Removed: the sample `127.0.0.1` bind value and loopback advice, bastion account and key-only advice, claims about Celery workers needing bastion access, tunnel secrets being encrypted with `SECRET_KEY`, and the description of how the local forwarded port is wired (none are stated there).
Method: documentation only; no commands were run.
