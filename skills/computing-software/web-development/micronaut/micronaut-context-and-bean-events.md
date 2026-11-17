---
id: computing-software.web-development.micronaut.micronaut-context-and-bean-events
name: micronaut-context-and-bean-events
category: computing-software
field: web-development
product: micronaut
tags: [micronaut, context-events, bean-events, applicationeventpublisher, eventlistener, async, beaninitializedeventlistener, beancreatedeventlistener]
level: practitioner
status: docs-checked
description: "Publish and listen to Micronaut application events (sync or @Async), and hook bean creation with BeanInitializedEventListener and BeanCreatedEventListener."
sources:
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/ioc/contextEvents.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/ioc/events.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: decouple code with context events, or intercept bean creation.

## Context events

Needs the `micronaut-context` dependency (transitive via `micronaut-http`, so HTTP runtime projects already have it). Events can be any type; those published by Micronaut extend `ApplicationEvent`.

Publish: inject `ApplicationEventPublisher<EventType>` and call `publishEvent`.

```java
@Singleton
public class SampleEventEmitterBean {
    @Inject
    ApplicationEventPublisher<SampleEvent> eventPublisher;

    public void publishSampleEvent() {
        eventPublisher.publishEvent(new SampleEvent());
    }
}
```

Warning: publishing is synchronous by default; `publishEvent` returns only after all listeners ran. Move slow work to a thread pool.

Listen, option 1: implement `ApplicationEventListener` (override `supports` to filter events):

```java
@Singleton
public class SampleEventListener implements ApplicationEventListener<SampleEvent> {
    @Override
    public void onApplicationEvent(SampleEvent event) { /* ... */ }
}
```

Option 2: `@EventListener` (io.micronaut.runtime.event.annotation) on any method, also for built-ins such as `StartupEvent` and `ShutdownEvent`:

```java
@EventListener
public void onSampleEvent(SampleEvent event) { ... }
@EventListener
public void onStartupEvent(StartupEvent event) { ... }
```

Asynchronous listener: add `@Async` (io.micronaut.scheduling.annotation) to the `@EventListener` method. It runs on the `scheduled` executor by default; configure that pool:

```yaml
micronaut:
  executors:
    scheduled:
      type: scheduled
      core-pool-size: 30
```

## Bean events

- `BeanInitializedEventListener`: modify or replace a bean after properties are set, before `@PostConstruct` hooks. Commonly used with `@Factory` beans.
- `BeanCreatedEventListener`: after the bean is fully initialised and `@PostConstruct` ran; typically to decorate or proxy it.

```java
@Singleton
public class EngineInitializer implements BeanInitializedEventListener<EngineFactory> {
    @Override
    public EngineFactory onInitialized(BeanInitializingEvent<EngineFactory> event) {
        EngineFactory engineFactory = event.getBean();
        engineFactory.setRodLength(6.6);   // before the factory builds the engine
        return engineFactory;
    }
}
```

Important: bean event listeners are initialised before type converters. If a listener relies on type conversion (e.g. via a configuration properties bean), you may see type conversion errors.

## Checked
2026-11-07. Every claim, parameter, default, config key, class, method and code block was compared with the cited pages and their included snippets; nothing needed changing.

Method: documentation only; no commands were run.
