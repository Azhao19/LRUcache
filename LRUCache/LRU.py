# Base code for LRUCache courtesy of Jerry An on levelup.gitconnected.com.

class LinkedNode(object):          # Doubly linked list struct
    
    def __init__(self, val, key): 
        self.val = val     
        self.key = key     
        self.next = None
        self.prev = None
    
    
class LRUCache:

    
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.lookup = {}     # Python infers this as hashmap based on how it is used later on
        self.dummy = LinkedNode(0,0)
        self.head = self.dummy.next # dummy node to help in deletion
        self.tail = self.dummy.next
             
    def remove_head_node(self):
        if not self.head:
            return
        prev = self.head
        self.head = self.head.next
        if self.head:
            self.head.prev = None
        del prev  # come back to this line
        
    def append_new_node(self, new_node):
        """  add the new node to the tail end 
        """
        if not self.tail:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = self.tail.next
        
            
    def unlink_cur_node(self, node):
        """ unlink current linked node
        """
        if self.head is node:
            self.head = node.next
            if node.next:
                node.next.prev = None
            return

        # removing the node from somewhere in the middle; update pointers
        prev, nex = node.prev, node.next
        prev.next = nex    
        nex.prev = prev
        

        
    def get(self, key: int):  # "touch"
        if key not in self.lookup:
            return -1
        
        node = self.lookup[key] 
        
        if node is not self.tail:
            self.unlink_cur_node(node)
            self.append_new_node(node)
        return node.val
    
    
    def put(self, key: int, value: int) -> None:
        if key in self.lookup:
            self.lookup[key].val = value
            self.get(key)
            return
        
                
       # if len(self.lookup) == self.capacity:
            # remove head node and correspond key
        #    self.lookup.pop(self.head.key)
         #   self.remove_head_node()
        
        # add new node and hash key
        new_node = LinkedNode(val=value, key=key)
        self.lookup[key] = new_node
        self.append_new_node(new_node)
