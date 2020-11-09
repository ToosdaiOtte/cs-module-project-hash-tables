class HashTableEntry:
    """
    Linked List hash table key/value pair
    """
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


# Hash table can't have fewer than this many slots
MIN_CAPACITY = 8


class HashTable:
    """
    A hash table that with `capacity` buckets
    that accepts string keys

    Implement this.
    """

    def __init__(self, capacity):
        self.capacity = capacity
        self.table = [None] * self.capacity
        self.load = 0


    def get_num_slots(self):
        """
        Return the length of the list you're using to hold the hash
        table data. (Not the number of items stored in the hash table,
        but the number of slots in the main list.)

        One of the tests relies on this.

        Implement this.
        """
        return self.table

    def get_load_factor(self):
        """
        Return the load factor for this hash table.

        Implement this.
        """
        return self.load / self.capacity
       


    def fnv1(self, key):
        """
        FNV-1 Hash, 64-bit

        Implement this, and/or DJB2.
        """
        """
        https://github.com/sup/pyhash/blob/master/pyhash/pyhash.py
	    Returns: The FNV-1 hash of a given string. 
	    """

        # Set the offset basis
        hash = 0x811c9dc5

        # For each character
        for character in key:
            # Xor with the current character
            hash ^= ord(character)

            # Multiply by prime
            hash *= 0x01000193

            # Clamp
            hash &= 0xffffffff
        
        # Return the final hash as a number
        return hash

        # FNV_offset_basis = 14695981039346656037
        # FNV_prime = 1099511628211
        # hashed = FNV_offset_basis

        # bytes_to_hash = key.encode()

        # for byte in bytes_to_hash:
        #     hashed = hashed * FNV_prime
        #     hashed = hashed ^ byte

        # return hashed 

    def djb2(self, key):
        """
        DJB2 hash, 32-bit

        Implement this, and/or FNV-1.

        https://gist.github.com/mengzhuo/180cd6be8ba9e2743753
        """
        hash = 5381
        for x in key:
            hash = (( hash << 5) + hash) + ord(x)
        return hash & 0xFFFFFFFF


    def hash_index(self, key):
        """
        Take an arbitrary key and return a valid integer index
        between within the storage capacity of the hash table.
        """
        #return self.fnv1(key) % self.capacity
        return self.djb2(key) % self.capacity

    def put(self, key, value):
        """
        Store the value with the given key.

        Hash collisions should be handled with Linked List Chaining.

        Implement this.
        """
        # hashed_key = self.djb2(key)
        # idx = hashed_key % len(self.table)
        # self.table[idx] = value

        idx = self.hash_index(key)
        node = self.table[idx]
        new_node = HashTableEntry(key, value)

        # non empty table
        if self.table[idx] != None:

            # find key, set value
            if node.key == key:
                node.value = value
            # search/set next
            else:
                if node.next.key == key:
                    node.next.value = value
        # empty table
        else:
            self.table[idx] = new_node

        self.load += 1

    def delete(self, key):
        """
        Remove the value stored with the given key.

        Print a warning if the key is not found.

        Implement this.
        """
        idx = self.hash_index(key)
        node = self.table[idx]

        # node is empty
        if node == None:
            print(f"{key} does not exist")
        
        # node key found
        else: 
            node.key = None
            self.load -= 1

    def get(self, key):
        """
        Retrieve the value stored with the given key.

        Returns None if the key is not found.

        Implement this.
        """
        # hashed_key = self.djb2(key)
        # idx = hashed_key % len(self.table)
        # # value = self.table[idx]

        # # return value

        idx = self.hash_index(key)
        node = self.table[idx]

        if node == None:
            print(f"{key} does not exist")
        else:
            if node.key == key:
                print(f"{node.key}, {node.value}")
                return node.value
            # move to next node  
            else:
                node = node.next


    def resize(self, new_capacity):
        """
        Changes the capacity of the hash table and
        rehashes all key/value pairs.

        Implement this.
        """
        # Your code here
        pass


if __name__ == "__main__":
    ht = HashTable(8)

    ht.put("line_1", "'Twas brillig, and the slithy toves")
    ht.put("line_2", "Did gyre and gimble in the wabe:")
    ht.put("line_3", "All mimsy were the borogoves,")
    ht.put("line_4", "And the mome raths outgrabe.")
    ht.put("line_5", '"Beware the Jabberwock, my son!')
    ht.put("line_6", "The jaws that bite, the claws that catch!")
    ht.put("line_7", "Beware the Jubjub bird, and shun")
    ht.put("line_8", 'The frumious Bandersnatch!"')
    ht.put("line_9", "He took his vorpal sword in hand;")
    ht.put("line_10", "Long time the manxome foe he sought--")
    ht.put("line_11", "So rested he by the Tumtum tree")
    ht.put("line_12", "And stood awhile in thought.")

    print("")

    # Test storing beyond capacity
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    # Test resizing
    old_capacity = ht.get_num_slots()
    ht.resize(ht.capacity * 2)
    new_capacity = ht.get_num_slots()

    print(f"\nResized from {old_capacity} to {new_capacity}.\n")

    # Test if data intact after resizing
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    print("")
