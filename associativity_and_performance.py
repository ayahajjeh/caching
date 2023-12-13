# citation: the main function below is modified directly from class material
#io.py
#
#Tucker L. Ward
#tucker.l.ward.12@dartmouth.edu
#
#created May 2013
#
#A simple program to demonstrate file I/O in Python. Reads in a file
#consisting of a single character, a space, and a 32-bit address in hex.
#File is specified as command-line argument; if argument is '-' reads from
#stdin
#
#CAUTION: minimal checking. onus is on user to provide a properly-formatted
#file...or add those checks yourself.
#
#USAGE: call main with argument of the target filename. or, if stdin is desired,
#call main with argument '-' or "-". exits automatically with file read option;
#to exit from stdin, just type exit

#for stdin
import sys
import numpy as np

def main(filename):
    
    addresses = []
    #stdin or a file?
    if (filename == '-'):
        in_file = sys.stdin
    else:
        try:#ensure the file exists
            with open(filename, "r"):
                in_file = open(filename, "r")
        except IOError: #throw exception if it does not
            print ("ERROR: file \"" + filename + "\" does not exist")
            return
    
    #read in each line of the file
    line = in_file.readline()
    while line:
        
        #strip line
        stripped_line = line.strip()
        
        #should I exit?
        if ( stripped_line == "exit" ):
            if (filename != '-'):
                in_file.close()
            return

        #process line into its components
        args = stripped_line.split(" ")
        
        #assign instr/data and the address
        c = args[0] #holds D or I
        n = int(args[1], 16) #holds an unsigned int of the address (at least 32 bits)
        addresses.append(n)
            
        line = in_file.readline()
        
    #close the input file
    in_file.close()
    return addresses


def print_line():
    print("-----------------------------------------------")

# global variables
# total number of lines in cache
total_number_of_lines = 64
# number of bytes per block
bytes_per_block = 16

class line:
    def __init__(self):
        self.valid = False
        self.tag = 0x000000
        self.last_touched = 0

class cache:
    def __init__(self, mode):
        self.number_of_lines = total_number_of_lines
        self.mode = mode

        if mode == "direct mapped":
            self.tagmask = 0xfffffc00
            self.setmask = 0x000003f0
            self.number_of_blocks = total_number_of_lines
            self.number_of_bytes_per_block = bytes_per_block
            self.number_of_sets = 64
            self.number_of_lines_per_set = 1
        elif mode == "2-way set associative":
            self.tagmask = 0xfffffe00
            self.setmask = 0x000001f0
            self.number_of_blocks = total_number_of_lines
            self.number_of_bytes_per_block = bytes_per_block
            self.number_of_sets = 32
            self.number_of_lines_per_set = 2
        elif mode == "4-way set associative": 
            self.tagmask = 0xffffff00
            self.setmask = 0x000000f0
            self.number_of_blocks = total_number_of_lines
            self.number_of_bytes_per_block = bytes_per_block
            self.number_of_sets = 16
            self.number_of_lines_per_set = 4
        elif mode == "fully associative":
            self.tagmask = 0xfffffff0
            self.setmask = 0x00000000
            self.number_of_blocks = total_number_of_lines
            self.number_of_bytes_per_block = bytes_per_block
            self.number_of_sets = 1
            self.number_of_lines_per_set = 64

        L = line()
        self.set = np.array([[L for i in range(self.number_of_lines_per_set)] for j in range(self.number_of_sets)])


# CPU requesting the byte at a specific address
def request_byte(address, cache, last_used_address):
    address_tag = address & cache.tagmask
    address_set = address & cache.setmask

    hit = 0
    miss = 0
    # trim the extra zeros in the address_tag based on the cache mode
    if cache.mode == "direct mapped":
        address_tag = address_tag >> 10
    elif cache.mode == "2-way set associative":
        address_tag = address_tag >> 9
    elif cache.mode == "4-way set associative":
        address_tag = address_tag >> 8
    elif cache.mode == "fully associative":
        address_tag = address_tag >> 4

    # trim the extra zeros in the address_set based on the cache mode
    if cache.mode == "direct mapped":
        address_set = address_set >> 4
    elif cache.mode == "2-way set associative":
        address_set = address_set >> 4
    elif cache.mode == "4-way set associative":
        address_set = address_set >> 4
    elif cache.mode == "fully associative":
        address_set = address_set >> 0
    
    # If Set[Aset] contains a line L such that L.valid == TRUE AND L.tag == Atag
    found_requested_byte = False
    set = cache.set[address_set]

    line_number = 0
    for L in set:
        if L.valid == True and L.tag == address_tag:
            # then a cache hit!
            hit = 1
            found_requested_byte = True
            # create a new line object to update the last touched meta data
            L = line()
            # first set up the L.valid and L.tag to old values
            # Set L.valid to be TRUE
            L.valid = True
            # Set L.tag to be Atag
            L.tag = address_tag
            # then update last touched meta variable
            L.last_touched = last_used_address
            # update the appropriate line in the appropriate set
            cache.set[address_set][line_number] = L
            break
        line_number += 1
    
    # Else
    if not found_requested_byte:
        # cache miss!
        miss = 1
        # find an empty line  L in Set[Aset]. (If no line is empty, then make one empty by evicting a line from the set)
        line_index = find_empty_line(set)

        # if no empty line
        if line_index == -1:
            # find last touched line
            line_index = find_last_touched_line(set, last_used_address)
        
        L = line()
        # Set L.valid to be TRUE
        L.valid = True
        # Set L.tag to be Atag
        L.tag = address_tag
        # update last touched meta variable
        L.last_touched = last_used_address
        # update the appropriate line in the appropriate set
        cache.set[address_set][line_index] = L

    return cache, hit, miss

def find_empty_line(set):
    empty_line_index = -1
    line_index = -1
    for L in set:
        line_index += 1
        if L.tag == 0x000000 and L.valid == False and L.last_touched == 0:
            empty_line_index = line_index
            break
    return empty_line_index

def find_last_touched_line(set, last_used_address):
    line_index = 0
    last_touched_line_index = 0
    last_touched = last_used_address
    for L in set:
        if L.last_touched <= last_touched:
            last_touched_line_index = line_index
            last_touched = L.last_touched
        line_index += 1
    return last_touched_line_index

def hit_rate(hits, number_of_requests):
    return (hits/number_of_requests)

def miss_rate(misses, number_of_requests):
    return (misses/number_of_requests)

def caching(cache, addresses):
    hits = 0
    misses = 0
    address_number_so_far = 0
    
    # go through the addresses trace file line by line
    for address in addresses:
        address_number_so_far += 1
        cache, hit, miss = request_byte(address, cache, address_number_so_far)
        hits += hit
        misses += miss
    
    print("hits: ", str(hits) + "; misses: " + str(misses) + "; total number of addresses requested: " + str(address_number_so_far))
    print("hits rate: ", str(hit_rate(hits, address_number_so_far)) + "; miss rate: " + str(miss_rate(misses, address_number_so_far)))

# please pass to the main function the path to the long trace text file
addresses = main("/Users/ayahajjeh/Desktop/23F/CS51/hw7/long-trace.txt")
cache1 = cache("direct mapped")
cache2 = cache("2-way set associative")
cache3 = cache("4-way set associative")
cache4 = cache("fully associative")
print_line()

print("cache mode: direct mapped:")
caching(cache1, addresses)
print_line()

print("cache mode: 2-way set associative:")
caching(cache2, addresses)
print_line()

print("cache mode: 4-way set associative:")
caching(cache3, addresses)
print_line()

print("cache mode: fully associative:")
caching(cache4, addresses)
print_line()