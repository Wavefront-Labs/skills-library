---
id: computing-software.software-engineering.java.spring-application-events-and-listeners
name: spring-application-events-and-listeners
category: computing-software
field: software-engineering
product: java
tags: [java, spring-boot-core, spring-application-events, eventlistener, transactionaleventlistener, applicationeventpublisher]
level: practitioner
status: docs-checked
description: "Publish and consume Spring application events with ApplicationEventPublisher, @EventListener, @TransactionalEventListener phases and async listeners."
sources: ["https://docs.spring.io/spring-framework/reference/core/beans/context-introduction.html#context-functionality-events", "https://docs.spring.io/spring-framework/reference/data-access/transaction/event.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Spring application events

```java
public record OrderPlaced(long orderId) {}          // any object works since Spring 4.2

@Service class OrderService {
    private final ApplicationEventPublisher events;
    OrderService(ApplicationEventPublisher events) { this.events = events; }
    @Transactional public void place(Order o) { repo.save(o); events.publishEvent(new OrderPlaced(o.getId())); }
}

@Component class Notifier {
    @TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)   // bound to the publisher's transaction
    void on(OrderPlaced e) { mail.send(e.orderId()); }

    @Async @EventListener                                               // needs @EnableAsync
    void audit(OrderPlaced e) { ... }
}
```
## Rules
- Plain `@EventListener` is synchronous by default: `publishEvent()` blocks until all listeners finish, and the listener runs inside the publisher's transaction context if one exists.
- `@TransactionalEventListener` `phase` is one of `BEFORE_COMMIT`, `AFTER_COMMIT` (default), `AFTER_ROLLBACK` or `AFTER_COMPLETION`. With no running transaction the listener is not invoked unless `fallbackExecution = true`.
- Order listeners with `@Order`; return a value (or a collection or array of events) from a synchronous listener to publish follow-up events.
- Conditional: `@EventListener(condition = "#e.orderId > 0")` takes a SpEL expression evaluated at runtime.
- `@Async` on a listener runs it in another thread; its exceptions are not propagated to the caller (see `AsyncUncaughtExceptionHandler`), and it cannot publish a follow-up event by returning a value, so inject `ApplicationEventPublisher` instead.

## Gotchas
- ThreadLocals and logging context (for example MDC) are not propagated to async event processing by default.

## Checked

Method: docs-checked 2026-11-09 against the Spring Framework ApplicationContext events section (context-introduction page: listeners, conditions, async, ordering) and the transaction-bound events page. Dropped unconfirmed claims (REQUIRES_NEW in AFTER_COMMIT, outbox advice, self-invocation, test-assertion advice).
