from django.core.cache import cache
from .models import Property
import logging
from django_redis import get_redis_connection

logger = logging.getLogger(__name__)

def get_all_properties():
    properties = cache.get('all_properties')
    if properties is None:
        properties = list(Property.objects.all())  # Evaluate queryset to list before caching
        cache.set('all_properties', properties, 3600)  # Cache for 1 hour (3600 seconds)
    return properties

def get_redis_cache_metrics():
    redis_client = get_redis_connection("default")
    info = redis_client.info('stats')
    hits = info.get('keyspace_hits', 0)
    misses = info.get('keyspace_misses', 0)
    total_requests = hits + misses
    hit_ratio = (hits / total_requests) if total_requests > 0 else 0

    if total_requests == 0:
        logger.error('No cache requests to calculate metrics.')

    logger.info(f"Redis cache hits: {hits}, misses: {misses}, hit ratio: {hit_ratio:.2f}")

    return {
        'hits': hits,
        'misses': misses,
        'hit_ratio': hit_ratio,
    }