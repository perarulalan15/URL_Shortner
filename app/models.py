# TODO: Implement your data models here
# Consider what data structures you'll need for:
# - Storing URL mappings
# - Tracking click counts
# - Managing URL metadata


from datetime import datetime

# In-memory database simulation
url_db = {}  # short_code -> {url, created_at, clicks}
