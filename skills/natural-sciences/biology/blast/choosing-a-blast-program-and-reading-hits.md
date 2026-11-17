---
id: natural-sciences.biology.blast.choosing-a-blast-program-and-reading-hits
name: choosing-a-blast-program-and-reading-hits
category: natural-sciences
field: biology
product: blast
tags: [blast, ncbi-blast, blast-plus, blastn, blastp, blastx, tblastn, tblastx, megablast, e-value, bit-score, percent-identity, query-coverage, nr, nt, refseq, core-nt, makeblastdb, custom-database, low-complexity-filter, sequence-similarity, homology-search, species-identification, primer-blast, outfmt-6, diamond]
level: practitioner
status: verified
description: "Pick the right BLAST program and database, then read hits correctly: E-value vs bit score, identity vs coverage, low-complexity masking, and running BLAST+ locally on a custom database."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choosing a BLAST program and reading the hits

**Goal:** search a sequence against the right database with the right program, and
decide from the numbers whether a hit means homology, identity, or nothing.

## 1. Pick the program by query and database type
| Query | Database | Program | Typical use |
|---|---|---|---|
| Nucleotide | Nucleotide | **blastn** (task `megablast` for near-identical, `blastn`/`dc-megablast` for divergent) | Species ID from a barcode, checking a PCR product |
| Protein | Protein | **blastp** | Finding homologs/function of a protein |
| Nucleotide (translated 6 frames) | Protein | **blastx** | What protein does this read/contig encode? |
| Protein | Nucleotide (translated) | **tblastn** | Find unannotated genes in a genome |
| Translated | Translated | **tblastx** | Divergent coding regions; slow |

Rule of thumb: **protein searches detect much more distant homology** than nucleotide
searches, because amino-acid conservation outlasts DNA conservation. For "is this the
same species/sequence?" use megablast; for "is this related at all?" go to protein.

On the NCBI web form, megablast is the default for blastn; switch to "Somewhat similar
sequences (blastn)" for cross-species searches — a frequent cause of "no hits".

## 2. Pick the database
- **nt / core_nt** (nucleotide) and **nr** (protein): broad, redundant, include
  unverified submissions. NCBI made the smaller *core_nt* the web default in August 2024 (announced on blast-announce 13 Aug 2024); it is nt without most eukaryotic chromosome sequences
  and under half the size, so a eukaryotic genomic hit may need the full nt or the Genome resource. Check which one the form is using.
- **RefSeq** (refseq_rna, refseq_protein): curated, non-redundant — better for annotation.
- **Organism filter** box: restrict to a taxon to speed up and sharpen results, or
  exclude one (e.g. exclude your own organism to find homologs elsewhere).
- Specialised: 16S rRNA database for bacteria; SwissProt for reviewed proteins.

## 3. Read the hit table
- **E-value:** expected number of hits this good by chance in a database this size.
  Lower is better. Very rough guide: < 1e-5 suggests homology for proteins; E-values
  depend on database size and query length, so they are **not comparable across searches**.
- **Bit score:** normalised score, independent of database size — use it to rank hits
  across searches.
- **Percent identity** only over the aligned region; always read it with **query
  coverage**. 100 % identity over 15 % of the query is a short local match, not the same
  sequence.
- For species identification by barcode, ~98–99 %+ identity across nearly full coverage is
  commonly used, but thresholds are taxon-dependent and a top hit is only as good as the
  submitter's identification.

## 4. Running BLAST+ locally
```
makeblastdb -in genome.fasta -dbtype nucl -out mydb -parse_seqids
blastn -query q.fa -db mydb -evalue 1e-10 -outfmt "6 qseqid sseqid pident length qcovs evalue bitscore" -max_target_seqs 5 -num_threads 8 > hits.tsv
```
- `-outfmt 6` (tabular) is easy to parse; add the columns you need explicitly.
- Caution: `-max_target_seqs` affects which hits are found, not only how many are
  printed — it is not guaranteed to return the best N (Shah et al. 2018/2019; NCBI patched part of the problem in BLAST+ 2.8.1). Use a generous value and filter
  afterwards.
- For very large protein searches, DIAMOND is a much faster BLASTP/BLASTX-like alternative.

## Gotchas
- **Low-complexity filtering** (DUST/SEG) is on by default and masks repeats; turning it
  off produces spurious hits, but short or repetitive queries may get no hits with it on.
- Short queries (primers, < ~30 nt) need `blastn-short` (task) or **Primer-BLAST**, which
  also checks primer pair specificity.
- A top hit labelled "uncultured bacterium" or "predicted protein" tells you little;
  scroll to well-annotated hits.
- Contamination in public databases is real (e.g. human or vector sequence in microbial
  assemblies). Check with VecScreen for vector contamination of your own sequences.

Checked 2026-10-19 with BLAST+ 2.17.0 (Windows build) on a random 20 kb genome: the `makeblastdb` and `blastn -outfmt "6 qseqid sseqid pident length qcovs evalue bitscore"` commands ran; `megablast` is the default task; a 400 nt exact query hit at 100% and a 300 nt query with 12% substitutions hit at 91% in megablast, blastn and dc-megablast; a 25 nt query found no hit with default megablast but did with `-task blastn-short`. Permitted tasks: blastn, blastn-short, dc-megablast, megablast, rmblastn.

Uncertain here: database names on the NCBI web form change periodically; option names
above are from BLAST+ 2.1x.

## Verify
- [ ] Program matches query/database types and the question (identity vs homology).
- [ ] Database and any organism filter recorded with the date of the search.
- [ ] Hits judged on coverage + identity + E-value, not identity alone.
- [ ] Local runs record the BLAST+ version, database build date and exact command.
