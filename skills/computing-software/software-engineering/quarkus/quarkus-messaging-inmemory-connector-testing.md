---
id: computing-software.software-engineering.quarkus.quarkus-messaging-inmemory-connector-testing
name: quarkus-messaging-inmemory-connector-testing
category: computing-software
field: software-engineering
product: quarkus
tags: [quarkus, messaging, testing, in-memory-connector, quarkustest, reactive-messaging]
level: practitioner
status: docs-checked
description: "Test Quarkus Messaging apps without a broker: switch channels to the in-memory connector in a test resource, then send to sources and assert on sinks."
sources:
  - https://github.com/quarkusio/quarkus/blob/main/docs/src/main/asciidoc/messaging.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Quarkus Messaging: test with the in-memory connector

Use this to test channel logic without a broker. It works for JVM tests only, not native tests (they do not support injection).

## Steps
1. Add the test dependency `io.smallrye.reactive:smallrye-reactive-messaging-in-memory` (scope `test`; Gradle `testImplementation`).
2. Create a test resource that switches the channels you need:
```java
public class InMemoryConnectorLifecycleManager implements QuarkusTestResourceLifecycleManager {
    @Override public Map<String, String> start() {
        Map<String, String> env = new HashMap<>();
        env.putAll(InMemoryConnector.switchIncomingChannelsToInMemory("words-in"));
        env.putAll(InMemoryConnector.switchOutgoingChannelsToInMemory("uppercase"));
        env.putAll(InMemoryConnector.switchOutgoingChannelsToInMemory("words-out"));
        return env;
    }
    @Override public void stop() { InMemoryConnector.clear(); }
}
```
Every channel you want to drive or inspect must be switched: incoming ones via `switchIncomingChannelsToInMemory`, outgoing ones (including emitter channels) via `switchOutgoingChannelsToInMemory`. `clear()` discards received and sent messages.
3. Write the test with `@QuarkusTest` and `@QuarkusTestResource(InMemoryConnectorLifecycleManager.class)`; inject `@Inject @Connector("smallrye-in-memory") InMemoryConnector connector;` (the `@Any` qualifier also works).
4. Drive and assert:
```java
InMemorySink<String> out = connector.sink("words-out");
InMemorySource<String> in = connector.source("words-in");
InMemorySink<String> up = connector.sink("uppercase");
app.sendMessage("Hello");
assertEquals("Hello", out.received().get(0).getPayload());
in.send("Bonjour");
await().untilAsserted(() -> assertEquals("BONJOUR", up.received().get(0).getPayload()));
```

## Caveats
- Only objects sent via `InMemorySource#send` are transmitted; received messages carry no connector-specific metadata.
- By default in-memory channels dispatch on the caller thread (the main thread in unit tests), whereas other connectors dispatch on separate duplicated Vert.x contexts. If your test depends on context propagation, add `quarkus-test-vertx` and annotate the test method `@io.quarkus.test.vertx.RunOnVertxContext`, set the channel attribute `run-on-vertx-context`, or call `InMemorySource#runOnVertxContext`.
- It is for testing only. For real brokers rely on Dev Services, which start a separate broker instance for tests.

## Checked

2026-11-07. Read in full: messaging.adoc. Each command, config key, class, method and default stated above was matched to page text or an embedded example. Removed or reworded: nothing; no claim failed the check.

Method: documentation only; no commands were run.
