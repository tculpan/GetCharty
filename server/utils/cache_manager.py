# utils/cache_manager.py
# 4. Cache Management for Filtered Data
import redis
import json

class DataCache:
    def __init__(self):
        self.redis_client = redis.Redis()
    
    def cache_filtered_data(self, file_id, filter_params, data):
        cache_key = f"filtered_{file_id}_{hash(json.dumps(filter_params))}"
        self.redis_client.setex(
            cache_key, 
            3600,  # 1 hour TTL
            data.to_json()
        )
        return cache_key
    
    def get_filtered_data(self, file_id, filter_params):
        cache_key = f"filtered_{file_id}_{hash(json.dumps(filter_params))}"
        cached = self.redis_client.get(cache_key)
        if cached:
            return pd.read_json(cached)
        return None