---
id: computing-software.cloud-infrastructure-engineering.aws.appsync-graphql-and-amplify
name: appsync-graphql-and-amplify
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, appsync, graphql, amplify, amplify-gen2, resolvers, pipeline-resolvers, js-resolvers, vtl, subscriptions, data-sources, dynamodb-resolver, appsync-events, caching, authorization-modes, api-key, amplify-hosting, amplify-data]
level: practitioner
status: draft
description: "Build AppSync GraphQL APIs (schema, JS pipeline resolvers, DynamoDB/Lambda data sources, multi-auth, subscriptions, caching) and ship front ends with Amplify Gen 2 hosting and data."
sources: ["AWS AppSync Developer Guide - JavaScript resolvers overview", "AWS AppSync Developer Guide - Authorization and authentication", "AWS AppSync Developer Guide - Real-time data (subscriptions)", "AWS Amplify Gen 2 documentation - Data and Hosting"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# AppSync and Amplify — a managed GraphQL back end and a front-end pipeline that deploys it

**Goal:** a GraphQL API where resolvers talk straight to DynamoDB (no Lambda in the hot path),
authorisation is enforced per field, clients get live updates, and the front end deploys
per-branch with Amplify.

## 1. Schema and resolvers
- Define `type Query/Mutation/Subscription` in SDL. Each field that needs data gets a
  **resolver** bound to a **data source**: DynamoDB, Lambda, Aurora (Data API), OpenSearch,
  EventBridge, HTTP, or `NONE` (local pass-through for subscriptions).
- Write resolvers in **JavaScript (APPSYNC_JS runtime)**, not VTL: `request(ctx)` returns the
  data-source request, `response(ctx)` shapes the result. Helpers in `@aws-appsync/utils`
  (`util.dynamodb.toMapValues`, `util.autoId()`, `util.error()`).
  ```js
  import { util } from '@aws-appsync/utils';
  export function request(ctx) {
    return { operation: 'GetItem', key: util.dynamodb.toMapValues({ id: ctx.args.id }) };
  }
  export function response(ctx) {
    if (ctx.error) util.error(ctx.error.message, ctx.error.type);
    return ctx.result;
  }
  ```
- **Pipeline resolvers** chain functions (auth check → fetch → transform) with shared
  `ctx.stash`; max 10 functions. Prefer `BatchGetItem`/`Query` functions over N+1 field resolvers.
- Validate resolver code locally: `aws appsync evaluate-code --runtime name=APPSYNC_JS,runtimeVersion=1.0.0 --code file://r.js --function request --context file://ctx.json`.
- Limits to design around: 30 s request timeout, 1 MiB response, Lambda data-source payload
  limits; batch resolvers (`BatchInvoke`) up to 2 000 items.

## 2. Authorisation (multi-auth)
| Mode | Use |
|---|---|
| `AMAZON_COGNITO_USER_POOLS` | Signed-in users; `@aws_auth(cognito_groups: ["admin"])` per field |
| `AWS_IAM` | Server-to-server, identity-pool guests |
| `OPENID_CONNECT` | External IdP |
| `AWS_LAMBDA` | Custom token logic (returns `isAuthorized`, `deniedFields`, `resolverContext`) |
| `API_KEY` | Public read-only; max 365-day expiry |
Set one default + additional modes; directives (`@aws_cognito_user_pools`, `@aws_api_key`)
mark which types/fields each mode may touch. Fine-grained row ownership is done in the
resolver (`ctx.identity.sub` vs item owner) or via Amplify's `allow.owner()` rules.

## 3. Subscriptions
- A `Subscription` field uses `@aws_subscribe(mutations: ["createPost"])`; AppSync fans out the
  mutation's **returned selection set** over WebSocket (MQTT over WSS). The client only
  receives fields the mutation returned — return the full object.
- Filter server-side with **enhanced subscription filters** (`extensions.setSubscriptionFilter`)
  so clients cannot subscribe to everyone's data; invalidate with `setSubscriptionInvalidationFilter`.
- For pub/sub without GraphQL, use **AppSync Events** (WebSocket channels, namespaces) instead.

## 4. Performance and cost
- **Server-side caching** (per-resolver or full-request) on a dedicated cache instance;
  caching keys from `ctx.args`/`ctx.identity`. Cache misses still hit the data source.
- Direct DynamoDB resolvers cost one request unit each; a Lambda data source adds cold start
  and duration charges — reserve it for logic the JS runtime cannot do (no network calls,
  no `Math.random`, limited libs).
- Turn on **field-level logging** (`ALL` in dev, `ERROR` in prod) and X-Ray; the slow
  resolver list in CloudWatch Logs Insights (`fields duration | sort duration desc`) is the
  profiling tool.
- Private APIs via VPC endpoint (`com.amazonaws.<region>.appsync-api`) for internal-only.

## 5. Amplify Gen 2
- Code-first back end in TypeScript: `amplify/data/resource.ts` defines the schema with
  `a.model({...}).authorization(allow => [allow.owner(), allow.group('admin')])`; `npx ampx sandbox`
  deploys a per-developer stack (CDK underneath), `npx ampx generate outputs` writes
  `amplify_outputs.json` for the client.
- `allow.owner()` stores the owner in an `owner` field = `sub::username`; `allow.publicApiKey()`
  needs the API key auth mode with an expiry you will have to rotate.
- **Amplify Hosting**: connect the Git repo; each branch gets a URL and (optionally) its own
  back-end stack; `amplify.yml` controls build; SSR frameworks (Next.js) run on Lambda@Edge/compute.
  Set env vars/secrets in the console (`npx ampx sandbox secret set`), not in the repo.
- Client: `generateClient<Schema>()` gives typed `client.models.Post.list()` /
  `.observeQuery()` for live lists.

## Gotchas
- A subscription without a filter + a mutation returning only `id` = clients get `{id}` and
  nothing else; that is by design.
- Changing an `@model`'s primary key in Amplify replaces the table — data loss unless you
  export first.
- API keys expire silently; alarm on `4XXError` spikes or set a calendar reminder.
- JS resolvers: no `async`, no `fetch`; `util.time.nowISO8601()` instead of `Date`.
- Unconfirmed: current AppSync Events feature set and Amplify Hosting compute limits — check docs.

## Verify
- [ ] `evaluate-code` returns the expected request for each resolver with sample context.
- [ ] A user in group `viewer` is denied a mutation marked `@aws_auth(cognito_groups:["admin"])`.
- [ ] Subscription delivers an event within ~1 s of the mutation and only to matching filters.
- [ ] Logs Insights shows no resolver > 500 ms p95 under load.
- [ ] Amplify branch preview deploys from a PR and tears down on close.
