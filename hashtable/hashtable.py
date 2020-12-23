class HashTableEntry:
    """
    Linked List hash table key/value pair
    """
    # this is like class Node in LinkedLists
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

MIN_CAPACITY = 8

 
class HashTable:
    """
    A hash table that with `capacity` buckets
    that accepts string keys

    Implement this.
    """
    def __init__(self, capacity):
        self.capacity = capacity
        self.items_stored = 0
        self.storage = [None] * capacity


    def get_num_slots(self):
        """
        Return the length of the list you're using to hold the hash
        table data. (Not the number of items stored in the hash table,
        but the number of slots in the main list.)

        One of the tests relies on this.

        Implement this.
        """
        return self.capacity

    def get_load_factor(self):
        """
        Return the load factor for this hash table.

        Implement this.
        """
        return self.items_stored / self.capacity


    def djb2(self, key):
        """
        DJB2 hash, 32-bit

        Implement this, and/or FNV-1.
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
        return self.djb2(key) % self.capacity



    # ===== PUT ===== 
    def put(self, key, value):
        """
        Store the value with the given key.

        Hash collisions should be handled with Linked List Chaining.

        Implement this.
        """
        hash_index = self.hash_index(key)
        
        # insert into an empty spot
        if not self.storage[hash_index]:
            self.storage[hash_index] = HashTableEntry(key, value)
            self.items_stored += 1

        # linked list exists at current location
        # two possibilities: update value for an existing key OR create a new entry for the new key
        else:
            current_node = self.storage[hash_index]

            while current_node.key != key and current_node.next:
                current_node = current_node.next

            # key found. Update current value.
            if current_node.key == key:
                current_node.value = value

            # end of list reached without finding the key. Create a new entry.
            else:
                current_node.next = HashTableEntry(key, value)
                self.items_stored += 1
        
        # resize hash table if load factor is now too large
        if self.get_load_factor() > 0.7:
            self.resize(self.capacity * 2)




    # ===== DELETE ===== 
    def delete(self, key):
        """
        Remove the value stored with the given key.

        Print a warning if the key is not found.

        Implement this.
        """
        index = self.hash_index(key)
        # four possibilities when deleting a value associated with a key:
        # 1. nothing at specified index (nothing to delete)
        # 2. value to delete is at the head of the list
        # 3. value to delete is in the middle or somewhere in the list
        # 4. value to delete is at the end of the list

        # get a reference to the current node
        current_node = self.storage[index]

        # 1. nothing at specified index (nothing to delete)
        if not current_node:
            print("Key not found.")

        # 2. value to delete is at the head of the list
        elif not current_node.next:
            
            self.storage[index] = None
            self.items_stored -= 1
        
        else:

            # store a pointer to the previous node
            previous_node = None

            # move to the next node if the key doesn't match, and if there is a next node
            while current_node.key != key and current_node.next:
                previous_node = current_node
                current_node = current_node.next

            # 4. value to delete is at the end of the list
            # The current element is the one to delete.
            if not current_node.next:
                previous_node.next = None
                self.items_stored -= 1
            
            # 3. value to delete is in the middle of the list
            # Reassign pointers around this node.
            else:
                previous_node.next = current_node.next
                self.items_stored -= 1
        
        # resize hash table if load factor is now too small
        if self.get_load_factor() < 0.2:

            new_capacity = self.capacity // 2

            # don't let smaller size fall below stated minimum
            if new_capacity < MIN_CAPACITY:
                new_capacity = MIN_CAPACITY

            self.resize(new_capacity)



    # ===== GET ===== 
    def get(self, key):
        """
        Retrieve the value stored with the given key.

        Returns None if the key is not found.

        Implement this.
        """
        index = self.hash_index(key)

        if self.storage[index]:
            current_node = self.storage[index]
            
            # move to the next node if the key doesn't match, and if there is a next node
            while current_node.key != key and current_node.next:
                current_node = current_node.next

            # end of list reached without finding a key
            if not current_node.next:
                return current_node.value
            
            # otherwise, stopped at the correct node. Return its value.
            else:
                return current_node.value

        # no linked list at this location. Return None.
        else:
            return None
        


    # ===== RESIZE =====
    def resize(self, new_capacity):
        """
        Changes the capacity of the hash table and
        rehashes all key/value pairs.

        Implement this.
        """
        # Your code here
        old_storage = self.storage

        # create new hash table values
        self.capacity = new_capacity
        self.storage = [None] * new_capacity

        # go through all the data and add to the new hash table
        for item in old_storage:

            # if current item is a linked list, add all nodes to new storage
            if item:

                current_node = item

                while current_node:

                    # insert current key-value pair into new storage
                    self.put(current_node.key, current_node.value)

                    current_node = current_node.next












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

    ht.put("line_13", "13 value")
    ht.put("line_14", "14 value")
    ht.put("line_13", "13 value")
    

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