---
id: computing-software.software-engineering.java.mocking-with-mockito
name: mocking-with-mockito
category: computing-software
field: software-engineering
product: java
tags: [java, java-testing, mockito, mocks, stubbing, argument-captor, test-doubles]
level: practitioner
status: docs-checked
description: "Use Mockito effectively: mocks vs spies, strict stubbing, argument matchers and captors, verifying interactions, static mocks, and when not to mock."
sources:
  - https://github.com/mockito/mockito/blob/main/mockito-core/src/main/java/org/mockito/Mockito.java
  - https://github.com/mockito/mockito/blob/main/mockito-core/src/main/java/org/mockito/ArgumentMatchers.java
  - https://github.com/mockito/mockito/blob/main/mockito-core/src/main/java/org/mockito/BDDMockito.java
  - https://github.com/mockito/mockito/blob/main/mockito-extensions/mockito-junit-jupiter/src/main/java/org/mockito/junit/jupiter/MockitoExtension.java
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mocking with Mockito

**Goal:** isolate the unit under test from slow or nondeterministic collaborators without writing brittle tests coupled to implementation details.

## 1. Setup
```java
@ExtendWith(MockitoExtension.class)        // strict stubs: unused stubbing fails the test
class CheckoutServiceTest {
    @Mock PaymentGateway gateway;
    @Mock Clock clock;
    @InjectMocks CheckoutService service;    // constructor injection preferred
```

## 2. Stubbing
```java
when(gateway.charge(any(), eq(new BigDecimal("10.00")))).thenReturn(Receipt.ok("r-1"));
when(gateway.charge(any(), any())).thenThrow(new GatewayTimeout());
when(repo.find(42L)).thenReturn(Optional.of(order), Optional.empty());   // consecutive calls
doThrow(new IOException()).when(storage).delete("x");                    // void methods
given(gateway.charge(any(), any())).willReturn(ok);                      // BDDMockito style
```
Matchers: if one argument uses a matcher, all must (`eq(...)` for literals). `argThat(o -> o.total().signum() > 0)` for custom checks.

## 3. Verifying
```java
verify(gateway).charge(argThat(c -> c.currency().equals("EUR")), any());
verify(mailer, never()).send(any());
verify(audit, times(2)).record(any());
ArgumentCaptor<Email> email = ArgumentCaptor.forClass(Email.class);
verify(mailer).send(email.capture());
assertThat(email.getValue().subject()).contains("Order 42");
verifyNoMoreInteractions(gateway);    // use sparingly: brittle
```
Verify **commands** (side effects that matter); for **queries**, assert on the result instead of verifying the call.

## 4. Spies, statics, finals
- `spy(realObject)` calls real methods unless stubbed; stub with `doReturn(x).when(spy).m()` (the `when(spy.m())` form calls the real method).
- Since Mockito 5.0.0 the inline mock maker is the default: final classes and methods are mockable.
- Static mocks are scoped to the `try` block (close the `MockedStatic`): `try (MockedStatic<UUID> u = mockStatic(UUID.class)) { u.when(UUID::randomUUID).thenReturn(fixed); }`. Prefer injecting a `Clock` or ID supplier.

## 5. What not to mock
- Value objects, collections, the class under test.
- Types you do not own with complex contracts (HTTP clients, JDBC, ORMs): wrap them in your own interface, or use a fake / Testcontainers / WireMock.
- Deep stubs (`RETURNS_DEEP_STUBS`) signal a Law of Demeter problem.

## Gotchas
- `UnnecessaryStubbingException` means a stub is unused: delete it or the test is not testing what you think (use `lenient()` only for shared setup).
- `any()` matches anything including null, but `any(Foo.class)` and the `anyInt()` family do a type check and do not match null (since Mockito 2.1.0); `nullable(Foo.class)` matches null or a `Foo`.
- Mocks return defaults (null, 0, empty collections, `Optional.empty()`) for unstubbed calls, which can hide missing stubs.

## Verify
- Break the production code (skip the charge call): the test fails on the `verify`, not on an NPE elsewhere.

## Checked

Date: 2026-10-25. Documentation release: Mockito 5.24.0 (GitHub main source and Javadoc, release of 2026-09-23).

Confirmed: strict stubbing by `MockitoExtension`; `lenient()`; null handling of `any()`, `any(Class)` and `nullable(Class)`; inline mock maker default since 5.0.0; `mockStatic`; `RETURNS_DEEP_STUBS`; BDDMockito `given`.

Method: documentation only; no commands were run.
