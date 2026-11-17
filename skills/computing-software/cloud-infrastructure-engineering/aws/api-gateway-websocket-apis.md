---
id: computing-software.cloud-infrastructure-engineering.aws.api-gateway-websocket-apis
name: api-gateway-websocket-apis
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, api-gateway, websocket-api, connection-management, route-selection, realtime, lambda, dynamodb]
level: practitioner
status: docs-checked
description: "Build API Gateway WebSocket APIs: $connect/$disconnect/$default routes, route selection, storing connection IDs, pushing via @connections, auth, limits and stale connections."
sources: ["https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-websocket-api-route-keys-connect-disconnect.html", "https://docs.aws.amazon.com/apigateway/latest/developerguide/websocket-api-develop-routes.html", "https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-how-to-call-websocket-api-connections.html", "https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-websocket-api-route-response.html", "https://docs.aws.amazon.com/apigateway/latest/developerguide/limits.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# API Gateway WebSocket APIs

**Goal:** server-to-client push (chat, notifications, live dashboards) with connection state
in a table and no servers to babysit.

## 1. Routes
- `$connect` — runs on handshake; authorise here (Lambda REQUEST authorizer or IAM; authorization can be configured on
  `$connect` only, so it is performed at connection time). Query strings and headers are passed to the integration;
  clients can also specify subprotocols with `Sec-WebSocket-Protocol`.
- `$disconnect` — best effort; API Gateway cannot guarantee delivery.
- `$default` — used when the route selection expression cannot be evaluated or no route matches (non-JSON messages also go here).
- Custom routes chosen by `RouteSelectionExpression`, e.g. `$request.body.action`
  (`{"action":"sendMessage", ...}` → route `sendMessage`).

## 2. Store connections
```python
# $connect handler
table.put_item(Item={"pk": f"user#{user_id}", "sk": f"conn#{event['requestContext']['connectionId']}",
                     "ttl": int(time.time()) + 7200})
```
Add a GSI on connectionId or key by it for `$disconnect` deletes. TTL cleans up connections
whose `$disconnect` never ran.

## 3. Push to clients
```python
api = boto3.client("apigatewaymanagementapi",
    endpoint_url=f"https://{domain}/{stage}")      # from requestContext.domainName/stage
try:
    api.post_to_connection(ConnectionId=cid, Data=json.dumps(msg).encode())
except api.exceptions.GoneException:
    delete_connection(cid)                          # stale: remove and move on
```
IAM: the `execute-api:ManageConnections` action controls access to the `@connections` API
(`POST` to send, `GET` for connection info, `DELETE` to disconnect: `https://{api-id}.execute-api.<REGION>.amazonaws.com/{stage}/@connections/{connection_id}`).

## 4. Limits to design around
- Idle connection timeout 10 minutes, maximum connection duration 2 hours — clients should send periodic messages
  (e.g. `{"action":"ping"}`) and reconnect with backoff.
- Message payload 128 KB with a 32 KB frame size (larger frames close the connection with code 1009); new connections
  per second per account default quota 500 (increasable).
- Fan-out to many connections is N `PostToConnection` calls — parallelise, batch via SQS
  workers for large rooms.

## Gotchas
- API Gateway does not pass the backend response to the client unless you set up a route response (only `$default` can be defined for WebSocket APIs).
- The management API calls return `GoneException` (410) for a closed connection, `PayloadTooLargeException` (413) and `LimitExceededException` (429).

## Verify
- [ ] `wscat -c "wss://<API_ID>.execute-api.<REGION>.amazonaws.com/prod?token=..."` connects; invalid token is rejected at handshake.
- [ ] Sending `{"action":"sendMessage"}` reaches the custom route; server push arrives on another connected client.
- [ ] Killing a client without close → next push gets `GoneException` and the row is deleted.

## Checked
Date: 2026-10-24. Documentation release: Amazon API Gateway Developer Guide (awsdocs source, June 2023 snapshot) plus the current botocore `apigatewaymanagementapi` model.
Confirmed: predefined routes and `$default` fallback; authorization on `$connect` only; `$disconnect` best effort; route selection expression `$request.body.action`; `@connections` POST, GET and DELETE; `execute-api:ManageConnections`; 10-minute idle timeout, 2-hour duration, 128 KB message and 32 KB frame limits, 500 new connections per second; route responses; `GoneException` (410), `PayloadTooLargeException` (413), `LimitExceededException` (429).
Removed as unconfirmed: the claim that browsers cannot set headers, the ManageConnections resource ARN pattern, the `ForbiddenException` cause and the custom-domain remark.

Method: documentation only; no commands were run.
