---
id: computing-software.firmware-embedded-development.iot-protocols.hivemq-extensions
name: hivemq-extensions
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [hivemq-extensions, hivemq-broker, hivemq, extension-sdk, authenticator, iot-protocols]
level: practitioner
status: docs-checked
description: "HiveMQ extensions: Extend HiveMQ with the Extension SDK instead of forking."
sources:
  - https://docs.hivemq.com/hivemq/latest/extensions/index.html
  - https://github.com/hivemq/hivemq-extension-sdk
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HiveMQ extensions

**Goal:** Extend HiveMQ with the Extension SDK instead of forking.

## Steps
1. Extensions are Java projects (the docs list OpenJDK 21 or higher, plus Gradle or Maven) whose entry point implements `ExtensionMain` with `extensionStart` and `extensionStop`
2. In extensionStart register callbacks through `Services`: `Services.initializerRegistry()` for client initializers, `Services.securityRegistry()` for authenticator and authorizer providers, and `Services.extensionExecutorService()` for the managed thread pool
3. Intercept packets with an interceptor such as `PublishInboundInterceptor` (method `onInboundPublish`); interceptors, authorizers and authenticators of an extension are deregistered automatically when it stops
4. HiveMQ calls extensionStart at startup or when the extension is enabled at runtime, and extensionStop at shutdown or when it is disabled at runtime
5. The Community Extension SDK is open source; the Enterprise Extension SDK adds features for the professional and enterprise editions, and some of its services are deprecated from HiveMQ 4.53

## Gotcha
Since HiveMQ 4.4.1 extensionStart blocks HiveMQ startup, so it must always return; do slow work on the managed extension executor. Interceptors are called by the same thread for all messages of a client, so keep their work short.

## Verify
- [ ] Extension starts and extensionStart returns
- [ ] Intercepted publish visible
- [ ] Disabling the extension at runtime calls extensionStop

## Checked

2026-11-03. Confirmed in the HiveMQ Extension Development page and the hivemq-extension-sdk source (ExtensionMain, Services, PublishInboundInterceptor javadoc): lifecycle methods and blocking caution, Services accessors, automatic deregistration, interceptor threading, JDK requirement, SDK editions and 4.53 deprecation note. Removed: the zip packaging, enabled and DISABLED marker file names, hot reload claim, enterprise extension list, and the outbound interceptor class name (not confirmed).
Method: documentation only; no commands were run.
