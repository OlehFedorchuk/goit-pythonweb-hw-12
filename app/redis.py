"""
Redis client configuration module.

This module initializes and configures the Redis client for caching
user data and password reset tokens. It supports async operations
for handling high-performance requests.

Environment Variables:
    REDIS_HOST (str): Redis server hostname. Defaults to 'localhost'.

Features:
    - Connection pooling for efficient resource usage.
    - Response decoding for automatic string conversion.
    - Used for caching authenticated user data (get_current_user).
    - Used for password reset token management.

Security Considerations:
    - Tokens stored in Redis have automatic expiration.
    - User data cache is invalidated after 30 minutes.
"""

import os
import redis

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=6379,
    decode_responses=True
)
