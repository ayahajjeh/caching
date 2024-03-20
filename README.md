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
I write a program that reads these trace files and simulate appropriate caching strategy, and collect statistics. That is:

- my simulation keeps track of the lines and sets
- and in each line, my simulation tracks the tag and valid bits, so it knows what addresses are currently cached
- with each new address request, it needs to determine if that request is a hit or a miss---and if a miss, update the cache meta-data appropriately.

I use C as a language to write this program and one reason is because it lets me manipulate the 32-bit addresses to extract things like tags and set indices.

## Cache Parameters
In this project, each cache line can hold a 16-byte block. And, each cache is unified.

Where appropriate, I use LRU ("least recently used") for eviction. Of the candidate lines for eviction, I get rid of the one whose most recent use---read or write---was the longest in the past. (I can do this because I keep track of a line's last use in the line's metadata.)

- "Line's last use?" I track (as a regular integer) the sequence number of that use.  E.g., for the block touched in the 3rd address in the sequence, I store "3."   For this assignment, I do not worry about overflow (as the numbers should easily fit inside a regular integer).
I assume that the caches are all initially empty. For purposes of this project, I consider a "miss" to be a memory touch (read or write) that did not find that byte in the cache---I then load that missed block into the cache and update it.

Again, when simulating caches, I don't keep track of the value of each byte. Rather, for a cache line, I only need to keep track of the metadata: whether the line's valid and, if so, the tag of the block that lives there and when that block was last touched.

## Simulation Output

## Diminishing Returns?
