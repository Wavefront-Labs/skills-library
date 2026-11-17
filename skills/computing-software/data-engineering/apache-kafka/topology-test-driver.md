---
id: computing-software.data-engineering.apache-kafka.topology-test-driver
name: topology-test-driver
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka, kafka-streams, topologytestdriver, kafka-streams-test-utils, testinputtopic, testoutputtopic, unit-tests, wall-clock-time, embedded-kafka, testcontainers]
level: advanced
status: docs-checked
description: "Unit test Kafka Streams topologies without a broker using TopologyTestDriver: input/output test topics, controlling record and wall-clock time, reading state stores."
sources:
  - https://kafka.apache.org/documentation/streams/developer-guide/testing.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Testing Kafka Streams with TopologyTestDriver

**Goal:** fast, deterministic tests of topology logic (including windows, joins, punctuations) in plain JUnit.

## Dependency
```xml
<dependency>
  <groupId>org.apache.kafka</groupId><artifactId>kafka-streams-test-utils</artifactId>
  <version>${kafka.version}</version><scope>test</scope>
</dependency>
```

## Test
```java
class ClickCountTopologyTest {
  TopologyTestDriver driver;
  TestInputTopic<String, String> in;
  TestOutputTopic<String, Long> out;

  @BeforeEach void setup() {
    Properties p = new Properties();
    p.put(StreamsConfig.APPLICATION_ID_CONFIG, "test");
    p.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "dummy:1234");
    driver = new TopologyTestDriver(ClickCounts.build(), p);
    in  = driver.createInputTopic("clicks", new StringSerializer(), new StringSerializer());
    out = driver.createOutputTopic("click-counts", new StringDeserializer(), new LongDeserializer());
  }
  @AfterEach void tearDown() { driver.close(); }       // always close

  @Test void lateRecordBeyondGraceIsDropped() {
    Instant t0 = Instant.parse("2026-10-16T10:00:00Z");
    in.pipeInput("home", "c1", t0);
    in.pipeInput("home", "c2", t0.plusSeconds(60));
    in.pipeInput("other", "x", t0.plus(Duration.ofMinutes(20)));    // advances stream time past window+grace
    in.pipeInput("home", "late", t0.plusSeconds(30));               // too late now
    KeyValueStore<String, Long> store = driver.getKeyValueStore("totals");
    assertThat(store.get("home")).isEqualTo(2L);
  }
}
```

## Controlling time
- **Record time:** pass timestamps to `pipeInput`; event-time punctuations fire automatically from the processed records' timestamps.
- **Wall-clock time** (for `PunctuationType.WALL_CLOCK_TIME` punctuators): the driver mocks wall-clock time, so call `driver.advanceWallClockTime(Duration.ofSeconds(20))` to trigger them.
- Stream time advances only when you pipe records; to close windows, pipe a later record.

## What it does not cover
- It runs the topology in-process without a broker, so real partitioning, rebalancing and multiple instances need an integration test against a real cluster.
- For a single `Processor` in isolation, `test-utils` also provides `MockProcessorContext`, which does not run punctuators automatically and does not manage changelogs or state directories.

## Verify
- [ ] Tests run in under a second each, no broker needed.
- [ ] Windowing, late data, and join-miss cases each have a test.
- [ ] `driver.close()` in teardown.

## Checked
Date 2026-11-01. Documentation release: Apache Kafka 3.9 Streams developer guide, Testing a Streams Application (kafka-site source).
Confirmed: kafka-streams-test-utils dependency, TopologyTestDriver, createInputTopic, wall-clock mocking and advanceWallClockTime, close(), event-time punctuation, MockProcessorContext behaviour. Removed unconfirmed claims: the autoAdvance overload, state-directory lock errors, mock schema registry and Testcontainers/Spring suggestions. Replaced the unconfirmed driver constructor with the Instant argument and readKeyValuesToMap with calls shown on the page.
Method: documentation only; no commands were run.
