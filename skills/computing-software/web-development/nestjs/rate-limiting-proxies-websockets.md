---
id: computing-software.web-development.nestjs.rate-limiting-proxies-websockets
name: rate-limiting-proxies-websockets
category: computing-software
field: web-development
product: nestjs
tags: [nestjs, rate-limiting, throttler, proxy, trust-proxy, websockets]
level: advanced
status: docs-checked
description: "Make NestJS ThrottlerGuard see real client IPs behind a proxy and apply it to WebSocket gateways with a custom handleRequest."
sources:
  - https://github.com/nestjs/docs.nestjs.com/blob/master/content/security/rate-limiting.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Behind a proxy, tell the adapter to trust it or every client shares one IP.

Express:

```typescript
const app = await NestFactory.create<NestExpressApplication>(AppModule);
app.set('trust proxy', 'loopback');
```

Fastify: `new FastifyAdapter({ trustProxy: 'loopback' })`. Node adapter: `new NodeAdapter({ trustProxy: 'loopback' })`.

To key on the forwarded client address on Express or the Node adapter, override `getTracker()`:

```typescript
@Injectable()
export class ThrottlerBehindProxyGuard extends ThrottlerGuard {
  protected async getTracker(req: Record<string, any>): Promise<string> {
    return req.ips.length ? req.ips[0] : req.ip;
  }
}
```

WebSockets: extend `ThrottlerGuard` and override `handleRequest(requestProps: ThrottlerRequest)`. Destructure `context, limit, ttl, throttler, blockDuration, generateKey`, take the client address from `context.switchToWs().getClient()._socket.remoteAddress` (`client.conn` for socket.io), build `key = generateKey(context, tracker, throttler.name)`, call `this.storageService.increment(key, ttl, limit, blockDuration, throttler.name)`, and if `isBlocked` call `this.throwThrottlingException(context, {...})`; then `return true`.

Gotchas:
- On Fastify v5.12.1+ (installed by `@nestjs/platform-fastify` v12) a numeric `trustProxy` such as `1` trusts no proxy at all, so `request.ip` is the proxy. Pass an address or range.
- On Fastify `request.ips` is ordered nearest first, so the guard above would key everyone to the proxy; keep the default tracker there.
- Do not register the WebSocket guard through `APP_GUARD` or `useGlobalGuards()`, because it would also run on HTTP routes. A reached limit emits an `exception` event on the socket.
- With several named throttlers pass `throttler.name` into the key and `increment()`.

## Checked

2026-11-04. Confirmed against the official NestJS docs source: trust proxy options, getTracker override, WebSocket handleRequest example, Fastify numeric trustProxy warning, ips ordering, APP_GUARD warning (rate-limiting page). Removed: left-most wording (page only shows req.ips[0]); invented Verify step.

Method: documentation only; no commands were run.
