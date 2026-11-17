---
id: computing-software.software-engineering.java.spring-batch-jobs-and-chunk-processing
name: spring-batch-jobs-and-chunk-processing
category: computing-software
field: software-engineering
product: java
tags: [java, spring-tx-security, spring-batch, chunk-processing, itemreader, job-repository, skip-retry]
level: advanced
status: draft
description: "Build Spring Batch 5 jobs: chunk-oriented steps with reader, processor, writer, skip and retry policies, restartability via JobRepository, job parameters and launching."
sources: ["https://docs.spring.io/spring-batch/reference/step/chunk-oriented-processing.html", "https://docs.spring.io/spring-batch/reference/job/running.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Spring Batch jobs and chunks (Batch 5 / Boot 3)

```java
@Bean Job importJob(JobRepository repo, Step load) { return new JobBuilder("importJob", repo).start(load).build(); }

@Bean Step load(JobRepository repo, PlatformTransactionManager tx,
                ItemReader<CsvRow> reader, ItemProcessor<CsvRow, Person> proc, ItemWriter<Person> writer) {
    return new StepBuilder("load", repo)
        .<CsvRow, Person>chunk(500, tx)                       // read/process 500 items, then write and commit once
        .reader(reader).processor(proc).writer(writer)
        .faultTolerant()
        .skip(ParseException.class).skipLimit(50)              // bad rows are skipped and counted
        .retry(DeadlockLoserDataAccessException.class).retryLimit(3)
        .build();
}

@Bean @StepScope FlatFileItemReader<CsvRow> reader(@Value("#{jobParameters['file']}") String file) { ... }
```
Boot 3 / Batch 5 changes: no `@EnableBatchProcessing` needed (and defining it disables Boot autoconfiguration), `JobBuilderFactory`/`StepBuilderFactory` are removed, chunk takes a transaction manager.

## Concepts
- `JobInstance` = job name plus identifying parameters; re-running a **completed** instance fails (`JobInstanceAlreadyCompleteException`); a failed one restarts where it stopped using saved `ExecutionContext` (`saveState`).
- Metadata tables (`BATCH_JOB_EXECUTION`...) live in the DB; initialise with `spring.batch.jdbc.initialize-schema`.
- Launch: `spring.batch.job.enabled=true` runs at startup; otherwise `JobLauncher.run(job, params)`, passing a unique parameter (timestamp or `RunIdIncrementer`) for reruns.
- Scale: multi-threaded step, partitioning, remote chunking.

## Gotchas
- Readers are not thread-safe unless documented (`JdbcPagingItemReader` is, cursor readers are not).
- Large chunk size holds a long transaction; tune with memory and lock time in mind.
- Skip on write causes the chunk to be retried item-by-item (scanning mode), which slows down.
- Keep processors side-effect free, as they may re-run on retry.

## Verify
`JobLauncherTestUtils` with `@SpringBatchTest` runs the job on a test file and asserts `ExitStatus.COMPLETED`, read/write/skip counts from `StepExecution`.
