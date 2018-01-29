from datetime import datetime

class Cache:
    def __init__(self):
        self.storage = {}

    def get(self, key, expiry):
        try:
            data = self.storage[key]
            data['expired'] = self.checkExpiry(data, expiry)
            data['cached_data'] = True

            return data
        except KeyError:
            return False

    def set(self, key, data):
        data = data.copy()
        data['cached_at'] = datetime.now()
        data['cached_data'] = True

        self.storage[key] = data

    def checkExpiry(self, data, expiry):
        if data['cached_at']:
            time_change_seconds = (datetime.now() - data['cached_at']).total_seconds()
            return expiry < time_change_seconds
        else:
            return True