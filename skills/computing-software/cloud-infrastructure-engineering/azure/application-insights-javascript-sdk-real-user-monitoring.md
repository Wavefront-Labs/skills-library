---
id: computing-software.cloud-infrastructure-engineering.azure.application-insights-javascript-sdk-real-user-monitoring
name: application-insights-javascript-sdk-real-user-monitoring
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, application-insights, javascript-sdk, real-user-monitoring, browser-telemetry, click-analytics, cors]
level: practitioner
status: docs-checked
description: "Add Application Insights JavaScript SDK or loader script for real user monitoring: page views, AJAX correlation, SPA routes, click analytics, sampling and privacy."
sources: ["https://learn.microsoft.com/azure/azure-monitor/app/javascript-sdk", "https://learn.microsoft.com/azure/azure-monitor/app/javascript-sdk-configuration", "https://learn.microsoft.com/azure/azure-monitor/app/javascript-framework-extensions", "https://learn.microsoft.com/azure/azure-monitor/app/javascript-feature-extensions"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# App Insights JavaScript SDK (RUM)

**Goal:** measure what real users experience in the browser and correlate it to backend requests.

## Install
Loader script (SDK Loader Script) in `<head>` before other scripts: copy from the docs, set `cfg: { connectionString: "<conn>" }`. Or npm:
```ts
import { ApplicationInsights } from '@microsoft/applicationinsights-web';
const ai = new ApplicationInsights({ config: {
  connectionString: '<conn>',
  enableAutoRouteTracking: true,           // SPA route changes as page views
  enableCorsCorrelation: true,             // add traceparent/Request-Id to cross-origin AJAX
  correlationHeaderExcludedDomains: ['*.thirdparty.com'],
  disableCookiesUsage: false, samplingPercentage: 50,
} });
ai.loadAppInsights(); ai.trackPageView();
```
Framework plugins: React (`@microsoft/applicationinsights-react-js`), Angular, React Native. Click Analytics plugin (`@microsoft/applicationinsights-clickanalytics-js`) captures clicks with `data-*` attributes.

## Correlation with backend
- Default `distributedTracingMode` is `AI_AND_W3C` (legacy Request-Id plus W3C `traceparent`/`tracestate`); headers are added automatically only when the page and the request share a domain.
- Cross-origin APIs: enable `enableCorsCorrelation` **and** allow the correlation headers (`traceparent`, `tracestate`, `Request-Id`, `Request-Context`) in the API's CORS configuration, or preflights fail.

## Data and queries
Page views, browser timings, AJAX dependencies, JS exceptions and custom events land in the Application Insights tables; look up the current table and column names in the Azure Monitor Logs table reference before writing queries.

## Privacy and cost
- Set `disableCookiesUsage: true` until consent (the SDK then neither stores nor reads cookie data).
- Do not put PII in page names or custom properties; use `addTelemetryInitializer` to scrub URLs (query strings with tokens).
- Sampling percentage in the browser must align with server-side sampling for complete traces.
- Browser extensions that block the SDK CDN or the ingestion endpoint cause undercounting.

## Verify
- [ ] Browser devtools network tab shows telemetry POSTs to the ingestion endpoint returning 200.
- [ ] Transaction search shows a page view with child AJAX dependency linked to the server request.

## Checked
2026-10-28. Confirmed on javascript-sdk-configuration: `distributedTracingMode` values and default AI_AND_W3C, same-domain automatic headers, `Request-Id`/`Request-Context`, `correlationHeaderExcludedDomains`, `disableCookiesUsage` meaning and default false. Removed: Log Analytics table names and KQL, the claim that IDs reset per page load, named ad-blocker domains, the exact track URL.
Method: documentation only; no commands were run.
