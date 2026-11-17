---
id: computing-software.software-engineering.quarkus.quarkus-event-bus-consume-and-send
name: quarkus-event-bus-consume-and-send
category: computing-software
field: software-engineering
product: quarkus
tags: [quarkus, event-bus, vertx, consume-event, request-reply, messaging]
level: practitioner
status: docs-checked
description: "Use the Quarkus Vert.x event bus: @ConsumeEvent consumers, blocking and Uni replies, EventBus send/publish/request, failures and codecs between local beans."
sources:
  - https://github.com/quarkusio/quarkus/blob/main/docs/src/main/asciidoc/reactive-event-bus.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Quarkus event bus: consume and send

Beans exchange asynchronous events over virtual addresses using the Vert.x EventBus. Add the `vertx` extension (artifact `io.quarkus:quarkus-vertx`). Delivery modes: point-to-point (one consumer, round-robin if several), publish/subscribe (all consumers), request/reply. Limits versus Reactive Messaging: single events only (no streams) and local messages only, but replies are supported.

## Consumer
```java
@ApplicationScoped
public class GreetingService {
    @ConsumeEvent("greeting")      // default address: fully qualified bean name
    public String consume(String name) { return name.toUpperCase(); }
}
```
- The parameter is the message body; a non-void return is the reply; `void` means fire and forget. You may take `Message<String>` to read `address()` and `body()`.
- Return `Uni<T>` or `CompletionStage<T>` for async replies.
- Consumers run on the Vert.x event loop and must be non-blocking. For blocking work use `@ConsumeEvent(value = "x", blocking = true)` or `@io.smallrye.common.annotation.Blocking` (which overrides the `blocking` attribute).

## Failures
If the method throws and a reply handler is set, the sender gets an `io.vertx.core.eventbus.ReplyException` with code `ConsumeEvent#FAILURE_CODE`. Without a reply handler the exception is rethrown (wrapped in `RuntimeException` if needed) for `Vertx#exceptionHandler()`.

## Sender
Inject the Mutiny bus: `@Inject io.vertx.mutiny.core.eventbus.EventBus bus;`
```java
bus.<String>requestAndForget("greeting", name);              // one consumer, no reply
bus.publish("greeting", name);                               // all consumers
Uni<String> r = bus.<String>request("greeting", name)
        .onItem().transform(Message::body);                  // async reply
String s = bus.<String>requestAndAwait("greeting", name).body(); // blocking reply
```

## Codecs
Quarkus supplies a default codec for local delivery, so you can pass your own objects directly. For a specific codec, set it on both ends: sender `new DeliveryOptions().setCodecName(MyNameCodec.class.getName())`, consumer `@ConsumeEvent(value = "greeting", codec = MyNameCodec.class)`.

## Gotcha
A `request` to an address with no listener just waits and times out; the page's HTTP example (`GET /async/Quarkus` returning `Hello Quarkus`) only works once a `@ConsumeEvent("greeting")` bean exists.

Verify: with both the REST resource and the consumer bean present, opening http://localhost:8080/async/Quarkus shows `Hello Quarkus`.

## Checked

2026-11-07. Read in full: reactive-event-bus.adoc. Each command, config key, class, method and default stated above was matched to page text or an embedded example. Removed or reworded: the `quarkus extension add` command form (only shown through an include not in the checked text); the extension and artifact names remain.

Method: documentation only; no commands were run.
