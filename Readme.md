# capX-backend-
# Dynamic Multilevel Caching System

## Overview
This is a dynamic multilevel caching system that manages data across multiple cache levels efficiently. The system supports dynamic addition of cache levels, multiple eviction policies, and data retrieval across these levels. It is designed to optimize cache operations, minimize cache misses, and dynamically handle cache level management.

## Key Features
- **Multiple Cache Levels**: Supports multiple cache levels (L1, L2, ..., Ln) with dynamic addition and removal of levels at runtime.
- **Eviction Policies**: Implements two popular eviction policies:
  - **Least Recently Used (LRU)**: Evicts the least recently accessed item.
  - **Least Frequently Used (LFU)**: Evicts the least frequently accessed item.
- **Efficient Data Retrieval and Insertion**: 
  - Data is retrieved from the highest priority cache (L1) first. If not found, it is fetched from lower levels sequentially.
  - When data is found in lower levels, it is promoted to higher levels.
- **Concurrency Support**: Thread-safe design using locks, allowing concurrent read and write operations.
- **Performance Optimizations**: Ensures efficient lookups and minimizes data movement across cache levels.

## Approach

### 1. Cache Level Management
- Each cache level is represented by its own class (`LRUCache` or `LFUCache`), which defines the size, eviction policy, and internal data structure.
- The `MultilevelCacheSystem` class manages a list of cache levels. It provides functions to add and remove cache levels dynamically.

### 2. Eviction Policies
- **LRU (Least Recently Used)**: Implemented using Python's `collections.OrderedDict`. When a key is accessed or inserted, it is moved to the end of the dictionary, ensuring that the least recently used item is at the front.
- **LFU (Least Frequently Used)**: Uses a dictionary to store the frequency of each key. On a cache miss, the item with the lowest frequency is evicted.

### 3. Data Retrieval and Insertion
- **Retrieval (`get(key)`)**:
  - Searches for the data starting from the highest priority cache level (L1) downwards.
  - If found, the data is promoted to higher cache levels, following the eviction policy.
  - If not found, returns a cache miss (`None`).
- **Insertion (`put(key, value)`)**:
  - Always inserts new data into the L1 cache.
  - Handles eviction based on the current policy if the cache is full.

### 4. Concurrency
- The system uses Python's `threading.Lock` to ensure thread safety during read (`get`) and write (`put`) operations.

### 5. Dynamic Cache Level Management
- The `addCacheLevel(size, evictionPolicy)` function adds a new cache level dynamically with the specified size and eviction policy.
- The `removeCacheLevel(level)` function removes a cache level dynamically, specified by its index.


## We ran 3 sample cases for our code
#sample case
- cache_system = MultilevelCacheSystem()
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
- cache_system = MultilevelCacheSystem()

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
- cache_system = MultilevelCacheSystem()

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


## Output for the above sample test cases -
<img width="1148" alt="Screenshot 2024-09-10 at 15 48 33" src="https://github.com/user-attachments/assets/8b702809-5b7d-4b8f-9d89-6852717a1a02">

