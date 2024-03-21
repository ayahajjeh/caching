# Caching
`This was one of my coding projects for CS51 Computer Architecture class at Dartmouth College.`

In this project, I gain a deeper understanding of caching by exploring and analyzing how it works for real 32-bit X86-family address traces. I use the following four approaches to caching, with 64 lines total in the cache:

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

Additionally, in my program, a tagmask is a 32-bit field that, when bitwise-AND'd against the address, leaves just the tag bits and zeros everything else out.
A setmask is a 32-bit field that, when bitwise-AND'd against the address, leaves just the set bits and zeros everything else out.

## Cache Parameters
In this project, each cache line can hold a 16-byte block. And, each cache is unified.

Where appropriate, I use LRU ("least recently used") for eviction. Of the candidate lines for eviction, I get rid of the one whose most recent use---read or write---was the longest in the past. (I can do this because I keep track of a line's last use in the line's metadata.)

- "Line's last use?" I track (as a regular integer) the sequence number of that use.  E.g., for the block touched in the 3rd address in the sequence, I store "3."   For this assignment, I do not worry about overflow (as the numbers should easily fit inside a regular integer).
I assume that the caches are all initially empty. For purposes of this project, I consider a "miss" to be a memory touch (read or write) that did not find that byte in the cache---I then load that missed block into the cache and update it.

Again, when simulating caches, I don't keep track of the value of each byte. Rather, for a cache line, I only need to keep track of the metadata: whether the line's valid and, if so, the tag of the block that lives there and when that block was last touched.

## Simulation Output
I structure my simulation to take an option to be "verbose" or not. When verbose, for each address, the program prints out

- what set it would be in
- what tag it would have
- the state of that set at that point
- what then happens: hit, miss, eviction, etc.  

## Diminishing Returns?
The conventional wisdom says that although increases in associativity improves performance, the amount of improvement drops off rather quickly. I test this convention in our case through the following.

Using the simulation, I determine the hit rate and miss rate on long-trace.txt for these approaches (with 64 lines total in the cache):
- direct-mapped
- 2-way set-associative  
- 4-way set-associative
- fully associative

### Conclusions for the Diminishing Returns Question
The hit and miss rates I got using long-trace.txt file for
- The direct mapped mode are
  - Hit rate = 0.9575564624323873
- Miss rate = 0.04244353756761263
- The 2-way set associative mode are
- Hit rate = 0.9747503891379842
- Miss rate = 0.025249610862015878
- The 4-way set associative mode are
- Hit rate = 0.9793254983629259
- Miss rate = 0.02067450163707411
- The fully associative mode are
- Hit rate = 0.9801349747040613
- Miss rate = 0.019865025295938688
- Conclusion
- According to the hit and miss rates we got for these four modes of
caching, the conventional wisdom is right for this case.
- The difference in performance between direct mapped and 2-way
set associative is 0.01719392671
- The difference in performance between 2-way set associative and
4-way set associative is 0.004575109225
- The difference in performance between 4-way set associative and
fully associative is 0.000809476341
- Thus, although increases in associativity improves performance,
the amount of improvement drops off rather quickly.
