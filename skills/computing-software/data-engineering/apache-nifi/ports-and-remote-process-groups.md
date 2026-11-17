---
id: computing-software.data-engineering.apache-nifi.ports-and-remote-process-groups
name: ports-and-remote-process-groups
category: computing-software
field: data-engineering
product: apache-nifi
tags: [data-engineering, apache-nifi, input-port, output-port, remote-process-group, site-to-site, funnel]
level: practitioner
status: docs-checked
description: "Input and output ports, root-level site-to-site ports, Remote Process Group setup with comma-separated URLs, RAW vs HTTP transport, batch defaults and funnels."
sources:
  - https://nifi.apache.org/docs/nifi-docs/html/user-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ports and Remote Process Groups

- Input Port brings data into a group; at root level it receives from remote NiFi instances via Site-to-Site.
- Output Port sends data out; at root level it queues data for remote pulls.
- Remote Process Group: enter the remote URL; multiple URLs can be given comma-separated (for a cluster, the cluster node URLs). Data is automatically load balanced as nodes join, leave or change load; it can take up to one minute for the group to discover the remote ports. Context menu: enable/disable transmission, manage remote ports, refresh remote.
- Transport defaults to RAW (raw socket on a dedicated port); HTTP suits restricted networks and proxies and supports BASIC and DIGEST proxy authentication.
- Port batch settings (Count, Size, Duration): if none is set, the default batch duration is 500 milliseconds for an input port and 5 seconds for an output port.
- Funnels combine connections into one.

Verify: the remote ports list loads and transmission shows the transmitting icon.

## Checked

Confirmed against the NiFi User Guide Site-to-Site and Remote Process Group Transmission sections: root-level input and output ports, "Remote connections (site-to-site)" for child groups, comma-separated URLs, RAW default with HTTP and BASIC/DIGEST proxy auth, batch duration defaults, funnels, enable/disable transmission, Manage remote ports and Refresh remote. Removed the claim that comma-separated URLs are recommended and the periodic re-check wording, which the page does not state.

Method: docs-only read of cited pages, 2026-11-08
