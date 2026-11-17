---
id: computing-software.software-engineering.java.dynamic-proxies-with-java-lang-reflect-proxy
name: dynamic-proxies-with-java-lang-reflect-proxy
category: computing-software
field: software-engineering
product: java
tags: [java, java-reflection, dynamic-proxy, invocationhandler, proxy-newproxyinstance, interface-based-proxy]
level: advanced
status: docs-checked
description: "Build interface-based JDK dynamic proxies with InvocationHandler: dispatch rules, default methods, return and exception contracts, and the documented newProxyInstance limits."
sources: ["https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/reflect/Proxy.html", "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/reflect/InvocationHandler.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dynamic proxies

## Create a proxy
```java
InvocationHandler handler = (proxy, method, args) -> {
    if (method.isDefault()) {
        return InvocationHandler.invokeDefault(proxy, method, args);   // Java 16+
    }
    // route other calls, e.g. to a target, a stub or a recorder
    return null;
};
Foo f = (Foo) Proxy.newProxyInstance(Foo.class.getClassLoader(),
                                     new Class<?>[] { Foo.class },
                                     handler);
```

## Rules (from the Proxy and InvocationHandler Javadoc)
1. A proxy class implements exactly the interfaces given, in the order given. `newProxyInstance` requires interfaces that are non-hidden and non-sealed, not classes or primitive types, with no duplicates, all visible by name through the given class loader.
2. A call through a proxy interface is dispatched to the handler's `invoke(proxy, method, args)`. `args` is `null` if the interface method takes no arguments; primitive arguments arrive wrapped.
3. `hashCode`, `equals` and `toString` declared in `Object` are also dispatched to the handler, with `java.lang.Object` as the declaring class of the `Method`. Other public `Object` methods are not overridden.
4. Return value: for a primitive return type the handler must return the matching wrapper; returning `null` for a primitive return type throws `NullPointerException` from the proxy call; an incompatible value throws `ClassCastException`.
5. Exceptions: the thrown type must be assignable to a type in the interface method's `throws` clause, or to `RuntimeException` or `Error`. Any other checked exception reaches the caller wrapped in `UndeclaredThrowableException`.
6. Default methods: call `InvocationHandler.invokeDefault(proxy, method, args)` (since Java 16). It throws `IllegalArgumentException` if the method is not a default method of a proxy interface (or is overridden by the proxy interfaces), or if the args length does not match.
7. If the same method signature appears in several proxy interfaces, the `Method` passed to the handler comes from the foremost interface in the list, regardless of the interface used at the call site. Interfaces with same-signature methods must agree on a primitive or `void` return type, otherwise one return type must be assignable to all the others.
8. `Proxy.isProxyClass(cls)` tests for a proxy class; `Proxy.getInvocationHandler(proxy)` returns the handler. A proxy class is final and extends `java.lang.reflect.Proxy`, so `proxy instanceof Foo` and `(Foo) proxy` work but it is not an instance of any implementation class.
9. Order matters: the same interfaces in a different order give two distinct proxy classes.
10. Non-public interfaces must all be in the same package and module, and then the proxy class is non-public in that package. `getProxyClass` is deprecated; use `newProxyInstance`.

## Self-check
- [ ] A handler that returns `null` for an `int`-returning interface method makes the proxy call throw `NullPointerException`.
- [ ] `toString()` on the proxy reaches the handler with `method.getDeclaringClass() == Object.class`.

## Checked

Confirmed on the JDK 21 Proxy and InvocationHandler Javadoc pages. The dev.java reflection page fetched as a stub and was not relied on. Removed because the pages do not state them: ByteBuddy, CGLIB and Spring `ProxyFactory` advice, `InvocationTargetException` unwrapping, `@Transactional` self-invocation, Retrofit and Spring HTTP interfaces, performance and caching advice, and native-image proxy configuration.

Method: docs-only read of cited pages, 2026-11-08
