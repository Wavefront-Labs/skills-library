---
id: computing-software.qa-testing-engineering.jest-pytest.mockito-stubbing-verification-captors
name: mockito-stubbing-verification-captors
category: computing-software
field: qa-testing-engineering
product: jest-pytest
tags: [mockito-verify, argumentcaptor, mockito, junit5, test-doubles]
level: practitioner
status: docs-checked
description: "Use Mockito well with JUnit 5: @Mock and @InjectMocks, when/thenReturn and doThrow stubs, verify with times and argument matchers, ArgumentCaptor, strict stubs, and spies."
sources:
  - https://github.com/mockito/mockito/blob/main/mockito-core/src/main/java/org/mockito/Mockito.java
  - https://github.com/mockito/mockito/blob/main/mockito-core/src/main/java/org/mockito/ArgumentMatchers.java
  - https://github.com/mockito/mockito/blob/main/mockito-extensions/mockito-junit-jupiter/src/main/java/org/mockito/junit/jupiter/MockitoExtension.java
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mockito stubbing, verification and captors

## Setup
```java
@ExtendWith(MockitoExtension.class)        // strict stubs by default: unused stubs fail the test
class CheckoutServiceTest {
  @Mock PaymentGateway gateway;
  @Mock EmailSender email;
  @InjectMocks CheckoutService service;     // constructor injection preferred
  @Captor ArgumentCaptor<Email> emailCaptor;
```

## Stubbing
```java
when(gateway.charge(any(Card.class), eq(new BigDecimal("36.00")))).thenReturn(ChargeResult.ok("ch_1"));
when(gateway.charge(any(), any())).thenThrow(new GatewayTimeout());       // last stub wins
when(rates.get("EUR")).thenReturn(1.17, 1.18);                            // consecutive calls
doThrow(new SmtpException()).when(email).send(any());                     // void methods
doAnswer(inv -> inv.getArgument(0)).when(repo).save(any(Order.class));    // echo argument
```

## Verification
```java
verify(gateway).charge(any(), eq(new BigDecimal("36.00")));
verify(email, times(1)).send(emailCaptor.capture());
Email sent = emailCaptor.getValue();
assertThat(sent.template()).isEqualTo("order-confirmation");
assertThat(sent.to()).isEqualTo("ada@example.test");
verify(gateway, never()).refund(any());
verifyNoMoreInteractions(gateway);          // use sparingly
InOrder inOrder = inOrder(gateway, email);
inOrder.verify(gateway).charge(any(), any());
inOrder.verify(email).send(any());
```
Matchers rule: if one argument uses a matcher, all must (`eq(...)` for literal values). Custom: `argThat(o -> o.total().signum() > 0)`.

## Spies and static mocks
```java
List<String> spy = spy(new ArrayList<>());
doReturn(100).when(spy).size();                   // doReturn avoids calling the real method
try (MockedStatic<Clock> clock = mockStatic(Clock.class)) { ... }   // needs the inline mock maker (the default since Mockito 5.0.0); scoped to the try block
```
Prefer injecting a `Clock` over static mocks.

## Guidance
- Verify outcomes and important interactions (payment charged once), not every call.
- Stub only what the test needs; strict stubs flag leftovers (`UnnecessaryStubbingException`).
- Don't mock types you don't own if a fake or real instance is easy (value objects, collections).

## Gotchas
- `when(spy.method())` calls the real method during stubbing; use `doReturn`.
- `any()` matches anything including null; since Mockito 2.1.0 `any(Class)` performs a type check and does not match null (use `nullable(Class)` to allow null).

## Verify
Tests fail when the interaction under test is removed, and no unnecessary-stubbing warnings remain.

## Checked

Date: 2026-10-25. Documentation release: Mockito 5.24.0 (GitHub main source and Javadoc, release of 2026-09-23).

Confirmed: `MockitoExtension` defaults to `Strictness.STRICT_STUBS`; inline mock maker default since 5.0.0 and `mockStatic` / `MockedStatic`; `any()` versus `any(Class)` null handling since 2.1.0 and `nullable(Class)`; `lenient()` since 2.20.0; `RETURNS_DEEP_STUBS`; `UnnecessaryStubbingException`.

Method: documentation only; no commands were run.
