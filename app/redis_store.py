import time


class RedisStore:
    def __init__(self) -> None:
        self.store = {}
        self.expiry = {}

    def get(self, key: str):
        if self.expiry.get(key, None) is not None and self._is_expired(key):
            return None
        return self.store.get(key, None)

    def set(self, key: str, value: any, *args) -> str:
        return_message = "OK" if key not in self.store else self.store.get(key)
        self.store[key] = value
        self.expiry[key] = None
        if len(args) > 0:
            if args[0] == "PX":
                self.expiry[key] = int(time.time() + int(args[1]) * 0.001)
        return return_message

    def _is_expired(self, key) -> bool:
        return self.expiry.get(key) < time.time()
