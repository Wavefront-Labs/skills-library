---
id: computing-software.web-development.nestjs.serverless-deployment-lambda
name: serverless-deployment-lambda
category: computing-software
field: web-development
product: nestjs
tags: [nestjs, serverless, aws-lambda, webpack, cold-start]
level: advanced
status: docs-checked
description: "Deploy NestJS to AWS Lambda with serverless-express, cache the bootstrapped handler, bundle with webpack, or use createApplicationContext for lightweight functions."
sources:
  - https://github.com/nestjs/docs.nestjs.com/blob/master/content/faq/serverless.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Cold start dominates serverless latency. The docs' benchmarks (tsc, unbundled): Express 7.9ms, Nest with platform-express 197.4ms, standalone Nest 111.7ms. With webpack bundling: 6.8ms, 81.5ms and 31.9ms. Bundling matters a lot (`nest build --webpack`).

Handler with the Serverless framework (`npm i @codegenie/serverless-express`, `npm i -D @types/aws-lambda serverless-offline`):

```typescript
let server: Handler;

async function bootstrap(): Promise<Handler> {
  const app = await NestFactory.create(AppModule);
  await app.init();
  const expressApp = app.getHttpAdapter().getInstance();
  return serverlessExpress({ app: expressApp });
}

export const handler: Handler = async (event: any, context: Context, callback: Callback) => {
  server = server ?? (await bootstrap());
  return server(event, context, callback);
};
```

`serverless.yml` points `handler: dist/main.handler` with events `ANY /` and `ANY {proxy+}`. Run `npm run build` then `npx serverless offline` and open `http://localhost:3000/dev/<route>`. Enable `esModuleInterop` in `tsconfig.json`.

Webpack config: set `externals: []` and ignore lazy microservice and websocket imports. The bundle must export `handler`: from `@nestjs/cli` v12.0.8 the default config sets `output.library.type` to `commonjs2` if your config keeps `...options.output`; otherwise set `output.libraryTarget: 'commonjs2'`. Optionally keep class names when minifying (`terserOptions: { keep_classnames: true }`) or `class-validator` may misbehave.

Lightweight alternative: `NestFactory.createApplicationContext(AppModule)` then `appContext.get(EventsService).process(event)`. It does not apply guards, interceptors and the like.

Gotchas:
- Swagger UI behind API Gateway can loop endlessly; add middleware that rewrites `/swagger` to `/swagger/` before `SwaggerModule.setup()`.
- Do not model rarely used resources (like Redis) as async providers; use lazy loading.

## Checked

2026-11-04. Confirmed against the official NestJS docs source: benchmark figures, handler code, serverless.yml routes, esModuleInterop, offline URL, webpack and commonjs2 notes, keep_classnames, standalone alternative, Swagger redirect and async provider notes (serverless page). Removed: invented Verify step.

Method: documentation only; no commands were run.
