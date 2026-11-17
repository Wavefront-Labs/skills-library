---
id: computing-software.software-engineering.java.spring-aop-proxies-and-aspects
name: spring-aop-proxies-and-aspects
category: computing-software
field: software-engineering
product: java
tags: [java, spring-framework-core, spring-aop-proxies, aspectj, around-advice, pointcut, self-invocation, cglib-proxy]
level: advanced
status: docs-checked
description: "Write Spring AOP aspects with @Around and pointcut expressions, understand JDK vs CGLIB proxies and self-invocation, and avoid advice on final or private methods."
sources: ["https://docs.spring.io/spring-framework/reference/core/aop.html", "https://docs.spring.io/spring-framework/reference/core/aop/proxying.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Spring AOP proxies and aspects

Spring AOP is **proxy based**: a bean is wrapped, and advice runs when callers go through the proxy.

## An aspect
```java
@Aspect @Component
public class TimingAspect {
    private static final Logger log = LoggerFactory.getLogger(TimingAspect.class);

    @Around("@annotation(com.acme.Timed) || execution(public * com.acme.service..*(..))")
    public Object time(ProceedingJoinPoint pjp) throws Throwable {
        long t0 = System.nanoTime();
        try { return pjp.proceed(); }
        finally { log.debug("{} took {} ms", pjp.getSignature().toShortString(), (System.nanoTime() - t0) / 1_000_000); }
    }
}
```
Around advice takes `ProceedingJoinPoint` as its first parameter and calls `proceed()`. Pointcut expressions use designators such as `execution(...)`, `within(...)` and `@annotation(...)`, combined with `&&`, `||` and `!`; a reusable `@Pointcut` method can be referenced by name.

## Proxy types
- If the target implements at least one interface, Spring uses a JDK dynamic proxy and proxies all of the interfaces the target type implements.
- If the target implements no interfaces, Spring creates a CGLIB proxy, a runtime-generated subclass of the target type.
- Forcing CGLIB (`proxyTargetClass`) proxies every method, not only interface methods. `final` classes cannot be proxied, and `final` and `private` methods (and package-private methods of a parent class in another package) cannot be advised. The proxy instance is created through Objenesis, so the constructor is not called twice unless the JVM disallows constructor bypassing.

## What advice does NOT see
1. **Self-invocation:** `this.bar()` inside the bean is a direct call on the target and bypasses the proxy, so no advice runs. Move the method to another bean, or use AspectJ compile-time or load-time weaving, which apply advice in bytecode and have no such issue.
2. `private` and `final` methods when proxying by CGLIB (see above).

## Verify
Test that calling through the injected bean triggers advice, and that an internal `this.method()` call does not (a regression test documenting the limitation).

## Checked

Method: docs-checked 2026-11-09 against the Spring Framework proxying mechanisms page (JDK vs CGLIB rules, final and private limits, Objenesis, self-invocation note), the advice page (around advice and ProceedingJoinPoint) and the pointcuts page (designators and combining). The aop.html landing page was read but is an index. Dropped unconfirmed claims (Boot starter and default proxy mode, circular dependency raw instances, aspect ordering, AOT).
