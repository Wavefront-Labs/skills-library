---
id: computing-software.cloud-infrastructure-engineering.garage.gateway-nodes
name: gateway-nodes
category: computing-software
field: cloud-infrastructure-engineering
product: garage
tags: [gateway-node, layout-assign-gateway, localhost-endpoint, table-resync]
level: practitioner
status: docs-checked
description: "Add stateless gateway nodes that expose the S3 API and websites locally without storing data."
sources:
  - https://garagehq.deuxfleurs.fr/documentation/cookbook/gateways/
  - https://garagehq.deuxfleurs.fr/documentation/operations/layout/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A gateway node exposes Garage endpoints (S3 API and websites) but stores no data. Running one on each machine that consumes S3 gives three benefits:

- It removes one or two network round trips, since the gateway knows which nodes hold the data rather than a random node forwarding.
- It eases management: the gateway is part of the cluster, so software always uses `http://localhost:3900` and you need not track node lists in a reverse proxy or DNS.
- It simplifies security: no TLS certificate to renew, because the S3 traffic stays in plain text on the local machine while node traffic uses the cluster's Secret Handshake protocol.

Create it like a normal node but assign the gateway role:

`garage layout assign --gateway --tag gw1 -z dc1 <node_id>`
`garage layout show`
`garage layout apply --version <new_version_number>`

Then use `aws --endpoint-url http://127.0.0.1:3900 s3 ls`. If a new gateway seems broken, force bucket and key lists to propagate with `garage repair -a --yes tables`.

## Checked

2026-11-04. Read the Configuring a gateway node and Cluster layout management pages in full. Confirmed the three benefits, the assign command, the localhost endpoint, the aws example and the table resync advice. Corrected the apply line to include the --version flag that the layout page requires.
Method: documentation only; no commands were run.
