from collections import OrderedDict
from threading import Lock

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = OrderedDict()
    
    def get(self, key):
        if key not in self.cache:
            return None
        self.cache.move_to_end(key)  # Used to mark as recently used
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)  # mark as recently used
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)  # evict the least recently used item

    def display(self):
        print(dict(self.cache))


class LFUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}
        self.freq = {}
    
    def get(self, key):
        if key not in self.cache:
            return None
        self.freq[key] += 1
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            self.cache[key] = value
            self.freq[key] += 1
        else:
            if len(self.cache) >= self.capacity:
                lfu_key = min(self.freq, key=self.freq.get)  # Find the least frequently used item
                self.cache.pop(lfu_key)
                self.freq.pop(lfu_key)
            self.cache[key] = value
            self.freq[key] = 1

    def display(self):
        print(self.cache)


class MultilevelCacheSystem:
    def __init__(self):
        self.caches = []
        self.lock = Lock()  # For thread-safety

    def addCacheLevel(self, size, evictionPolicy):
        if evictionPolicy == 'LRU':
            cache = LRUCache(size)
        elif evictionPolicy == 'LFU':
            cache = LFUCache(size)
        else:
            raise ValueError("Unsupported eviction policy")
        
        with self.lock:
            self.caches.append(cache)
    
    def get(self, key):
        with self.lock:
            for level, cache in enumerate(self.caches):
                value = cache.get(key)
                if value is not None:
                    # Move the data to higher levels
                    for higher_cache in self.caches[:level]:
                        higher_cache.put(key, value)
                    return value
            return None
    
    def put(self, key, value):
        with self.lock:
            if not self.caches:
                return
            # Insert in the first cache level (L1)
            self.caches[0].put(key, value)
            # Propagate to all subsequent cache levels
            for i in range(1, len(self.caches)):
                self.caches[i].put(key, value)

    def removeCacheLevel(self, level):
        with self.lock:
            if 0 <= level < len(self.caches):
                self.caches.pop(level)
            else:
                raise IndexError("Invalid cache level")

    def displayCache(self):
        with self.lock:
            for i, cache in enumerate(self.caches):
                print(f"Cache Level {i+1}:")
                cache.display()


#sample case
cache_system = MultilevelCacheSystem()
cache_system.addCacheLevel(3, 'LRU')  
cache_system.addCacheLevel(2, 'LFU')  

cache_system.put("A", "1")
cache_system.put("B", "2")
cache_system.put("C", "3")

print(cache_system.get("A"))  
cache_system.put("D", "4")  
print(cache_system.get("C")) 

cache_system.displayCache()


#another sample case
cache_system = MultilevelCacheSystem()

cache_system.addCacheLevel(2, 'LRU')  
cache_system.addCacheLevel(2, 'LRU')  

cache_system.put("A", "1")  
cache_system.put("B", "2")  
cache_system.put("C", "3")  
cache_system.put("D", "4")  
print(cache_system.get("A"))  
print(cache_system.get("C"))  

cache_system.displayCache()


#another sample case
cache_system = MultilevelCacheSystem()

cache_system.addCacheLevel(1, 'LRU')  
cache_system.addCacheLevel(2, 'LFU')  

cache_system.put("A", "1")  
cache_system.put("B", "2")  
print(cache_system.get("A"))  
print(cache_system.get("B"))  

cache_system.addCacheLevel(3, 'LRU')  
cache_system.put("C", "3")  
cache_system.put("D", "4")  
print(cache_system.get("C"))  

cache_system.removeCacheLevel(1)  

cache_system.displayCache()
