---
id: natural-sciences.biology.bioconductor.deseq2-differential-expression
name: deseq2-differential-expression
category: natural-sciences
field: biology
product: bioconductor
tags: [bioconductor, r, deseq2, rna-seq, differential-expression, dge, count-matrix, tximport, salmon, featurecounts, design-formula, batch-effect, size-factors, normalisation, vst, rlog, pca, lfcshrink, apeglm, padj, fdr, benjamini-hochberg, independent-filtering, volcano-plot, ma-plot, edger, limma-voom]
level: practitioner
status: docs-checked
description: "Run an RNA-seq differential expression analysis in R with DESeq2: un-normalised counts in, design formula with batch, pre-filtering, results, lfcShrink, and the classic mistakes."
sources: [https://bioconductor.org/packages/devel/bioc/vignettes/DESeq2/inst/doc/DESeq2.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DESeq2 differential expression

**Goal:** a list of differentially expressed genes from bulk RNA-seq counts, from a
model that matches the experimental design, with QC that would catch a sample swap
or batch effect before you interpret anything.

## 1. Inputs
- **Un-normalised counts** (or estimated counts) of sequencing reads, per the DESeq2
  vignette. Transcript-level quantifiers (salmon/kallisto) are imported with
  **tximport** and a `DESeqDataSet` is built from the `txi` object and the sample table.
  Do not feed already-normalised values.
- A sample table (`colData`) whose rows match the count-matrix columns **in the same
  order** (the vignette calls this critical). Check it:
  `all(colnames(cts) == rownames(coldata))`.
- Factor reference levels: by default R chooses the reference level alphabetically, so
  set it explicitly:
  `coldata$condition <- factor(coldata$condition, levels = c("control", "treated"))`.

## 2. Build and run
```r
library(DESeq2)
dds <- DESeqDataSetFromMatrix(countData = cts, colData = coldata,
                              design = ~ batch + condition)
keep <- rowSums(counts(dds) >= 10) >= smallestGroupSize   # vignette's pre-filter example
dds <- dds[keep, ]
dds <- DESeq(dds)
resultsNames(dds)                                  # see available coefficients
res <- results(dds, contrast = c("condition", "treated", "control"), alpha = 0.05)
summary(res)
```
- Put the variable of interest **last** in the design formula; adjust for known nuisance
  variables (batch, donor for paired designs).
- A batch confounded with condition (all controls in one batch, all treated in another)
  cannot be separated by any software.
- Set `alpha` in `results()` to the adjusted-p-value cutoff you will use.

## 3. Shrinkage and replicates
- `lfcShrink` takes the `dds` object and the name or number of the coefficient to shrink;
  the vignette describes apeglm as the adaptive t prior shrinkage estimator. Check the
  vignette for the `type` options in your installed version.
- Technical replicates (same library sequenced twice) are combined into single columns of
  the count matrix with `collapseReplicates()`, not treated as biological replicates.

## 4. Check the vignette for these
Sample QC (variance-stabilising transform, PCA, dispersion plot), how adjusted p-values
and NA values are produced, testing against a fold-change threshold (`lfcThreshold`),
and batch-effect removal for plots. Read the matching vignette sections for your
installed version rather than relying on this summary.

## 5. Report
Keep stable gene IDs (Ensembl) as the key. Record R, Bioconductor and package versions
(`sessionInfo()`).

## Gotchas
- Bioconductor releases are tied to R versions; install with `BiocManager::install()`
  and don't mix release versions.
- Function arguments change between releases; check the vignette for your version.

## Verify
- [ ] Un-normalised counts in; colData order matches count columns.
- [ ] Reference level set; design includes known batches and variable of interest last.
- [ ] Significance judged on adjusted p-values at the chosen `alpha`.
- [ ] sessionInfo saved with results.

## Checked
2026-11-01. Confirmed in the DESeq2 vignette: un-normalised/estimated counts input, colData/column order requirement, variable of interest last, the rowSums(counts >= 10) pre-filter example, alphabetical default reference level, `alpha` in `results()`, tximport-based dataset construction, collapseReplicates for technical replicates, lfcShrink coefficient argument and apeglm description. Removed (not found in the vignette text read): Benjamini–Hochberg and NA-cause statements, apeglm coef-only rule, lfcThreshold/altHypothesis advice, removeBatchEffect advice, QC plot advice, XIST check, replicate-count advice.
Method: documentation only; no commands were run.
