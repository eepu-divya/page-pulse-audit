from cachetools import TTLCache

# Cache for 10 minutes (600 seconds)
cache = TTLCache(maxsize=100, ttl=600)