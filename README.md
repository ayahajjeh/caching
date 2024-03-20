# Caching
`This was one of my coding projects for CS51 Computer Architecture class at Dartmouth College.`

In this project, I gain a deeper understanding of caching by exploring and analyzing how it works for real 32-bit X86-family address traces. I use the following four different implementations:

- direct-mapped
- 2-way set-associative
- 4-way set-associative
- fully associative

Read below for more details about the trace files used, code samples, cache parameters, the simulation output, and my conclusions about the diminishing returns in the relation between associativity increases and performance improvements.

## Trace Files
I use two trace files:

- sample.txt containing just a few entries.
- long-trace.txt with millions of entries.

Each trace contains a list of byte-by-byte memory accesses: a "D" or "I" (indicating "data" or "instruction fetch") followed by the address in hex. In this project, I ignore the D/I (but in theory, we could use it to simulate a split cache).

FYI: long-trace was generated using valgrind to monitor actual C code running on x86, in 32-bit mode.

## Code Samples

## Cache Parameters

## Simulation Output

## Diminishing Returns?
