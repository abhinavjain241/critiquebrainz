import requests
import urllib
from critiquebrainz.cache import cache, generate_cache_key

DEFAULT_CACHE_EXPIRATION = 12 * 60 * 60  # seconds

BASE_URL = "https://api.spotify.com/v1"


def search(query, type, limit=20, offset=0):
    """Get Spotify catalog information about artists, albums, or tracks that match a keyword string."""
    key = generate_cache_key('search', source='spotify', params=[query, type, limit, offset])
    resp = cache.get(key)
    if not resp:
        resp = requests.get("%s/search?q=%s&type=%s&limit=%s&offset=%s" %
                            (BASE_URL, urllib.quote(query.encode('utf8')), type, str(limit), str(offset))).json()
        cache.set(key, resp, DEFAULT_CACHE_EXPIRATION)
    return resp


def album(spotify_id):
    """Get Spotify catalog information for a single album."""
    key = generate_cache_key('albumz', source='spotify', params=[spotify_id])
    resp = cache.get(key)
    if not resp:
        resp = requests.get("%s/albums/%s" % (BASE_URL, spotify_id)).json()
        cache.set(key, resp, DEFAULT_CACHE_EXPIRATION)
    return resp
