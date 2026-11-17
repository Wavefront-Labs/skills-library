---
id: computing-software.cloud-infrastructure-engineering.apache-apisix.apisix-variables
name: apisix-variables
category: computing-software
field: cloud-infrastructure-engineering
product: apache-apisix
tags: [apache-apisix, apisix, variables, consumer-name, route-id, balancer-ip, log-format]
level: practitioner
status: docs-checked
description: "The APISIX-specific variables usable in plugins and log formats: consumer_name, route_id, service_id, balancer_ip, graphql_*, mqtt_client_id, resp_body and more."
sources:
  - https://raw.githubusercontent.com/apache/apisix/master/docs/en/latest/apisix-variable.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# APISIX variables

APISIX provides these in addition to NGINX variables:

- `consumer_name`: username of the consumer.
- `consumer_group_id`: ID of the consumer's group.
- `route_id`, `route_name`: the matched route.
- `service_id`, `service_name`: the bound service.
- `balancer_ip`, `balancer_port`: the selected upstream server.
- `upstream_unresolved_host`: configured upstream domain or IP before DNS resolution.
- `graphql_name`: GraphQL operation name.
- `graphql_operation`: operation type, such as `mutation`.
- `graphql_root_fields`: top-level GraphQL fields.
- `mqtt_client_id`: client ID in an MQTT connection (mqtt-proxy).
- `redis_cmd_line`: content of a Redis command.
- `resp_body`: response body for logger formats when body logging is enabled (for example `include_resp_body: true`).
- `rpc_time`: time spent on an RPC request (xRPC).

Custom variables can also be registered (see plugin-develop, "register custom variable").

## Checked

2026-11-04: read the APISIX variable page; every variable and its description matches its table. Removed the unstated usage examples (log_format, vars, header values); the page only says the log-format use for resp_body.

Method: documentation only; no commands were run.
