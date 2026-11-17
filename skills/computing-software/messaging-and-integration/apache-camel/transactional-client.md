---
id: computing-software.messaging-and-integration.apache-camel.transactional-client
name: transactional-client
category: computing-software
field: messaging-and-integration
product: apache-camel
tags: [apache-camel, eip, transacted, spring-transaction, jta, propagation]
level: advanced
status: docs-checked
description: "Camel transacted routes: transacted() right after from, transaction manager lookup, SpringTransactionPolicy propagation names, local vs JTA global transactions."
sources:
  - https://camel.apache.org/components/next/eips/transactional-client.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Transactional client

Enable with `transacted()` right after `from` (XML `<transacted/>`, YAML `transacted: {}`). There are no begin or commit calls; Camel uses the Spring or JTA transaction manager. With a single manager Camel finds it automatically; multiple managers or custom propagation need explicit config. The scope covers that route and other routes the message passes through.

Propagation: a route has only one policy; to change it use a new route. Define `SpringTransactionPolicy` beans with a `transactionManager` and optional `propagationBehaviorName`:
- `PROPAGATION_REQUIRED` (the page's `txRequired` bean sets no `propagationBehaviorName`; with a single manager no policy bean is needed)
- `PROPAGATION_REQUIRES_NEW` (independent transaction)
- `PROPAGATION_MANDATORY` (needs an existing one)

Select with `transacted("txRequired")` or `<transacted ref="..."/>`. On completion the manager commits or rolls back each leg; legs can differ. Keep the number of behaviours low.

Flow: begin, work, commit; an exception rolls back.

Resources:
- Local (one resource): `DataSourceTransactionManager` for JDBC, `JmsTransactionManager` for JMS.
- Global (e.g. JMS plus JDBC): `JtaTransactionManager` with Atomikos, Narayana or an application server.
- Supporting components: ActiveMQ, JMS, SJMS, SJMS2, JDBC, JPA, SQL, MyBatis.

JMS: configure the `activemq` component with `transacted` true and a `transactionManager` reference; without one Camel uses a `JmsTransactionManager`.

Verify: the page's database example has one route for success and one for a forced rollback, both marked `transacted`, with a `DataSourceTransactionManager` as the transaction manager.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Compared against the Camel Transactional Client EIP page: transacted() placement right after from, single-manager convention, one policy per route, the three SpringTransactionPolicy propagation names and txRequired, txRequiresNew, txMandatory bean ids, local versus global transaction managers, JTA providers, the supported component list, the keep-it-simple advice and the activemq transacted and JmsTransactionManager fallback match. The old claim that PROPAGATION_REQUIRED is the default was reworded to what the page shows. No commands were run.
