---
id: computing-software.cloud-infrastructure-engineering.datadog.rum-browser
name: rum-browser
category: computing-software
field: cloud-infrastructure-engineering
product: datadog
tags: [datadog, rum, real-user-monitoring, browser-sdk, session-replay]
level: practitioner
status: draft
description: "Instrument a web app with the Datadog RUM Browser SDK to capture sessions, views, resources and errors."
sources: ["https://docs.datadoghq.com/", "https://docs.datadoghq.com/agent/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Real User Monitoring
Goal: measure real user performance.

```html
<script src="https://www.datadoghq-browser-agent.com/us1/v5/datadog-rum.js"></script>
<script>
  window.DD_RUM && window.DD_RUM.init({
    applicationId: '<RUM_APPLICATION_ID>',
    clientToken: '<RUM_CLIENT_TOKEN>',
    site: 'datadoghq.com',
    service: 'shop-web',
    env: 'prod',
    version: '1.4.2',
    sessionSampleRate: 100,
    sessionReplaySampleRate: 20,
    trackUserInteractions: true,
    defaultPrivacyLevel: 'mask-user-input'
  });
</script>
```

- The client token is public by design (it is shipped to browsers); never use your API key there.
- Link RUM to APM by `allowedTracingUrls` for end-to-end traces (confirm field name in your SDK version).
- Core Web Vitals appear on the Performance page.

Gotcha: Session Replay can capture sensitive input; keep a strict privacy level and mask fields. Check the SDK CDN URL version in the docs.

Configure sampling for cost, tag releases with the `version` field, and verify that the privacy settings meet your legal requirements before enabling Session Replay in production. Use `beforeSend` to drop or redact URLs and fields that contain personal data before events leave the browser.

## Verify
- Sessions appear in RUM Explorer; a view has loading times and resources.
