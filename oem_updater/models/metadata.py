from oem_core import models
from oem_framework.core.helpers import timestamp_utc


class Metadata(models.Metadata):
    def update(self, item, hash_key, hash):
        if not self.storage.format.to_path(item, self.storage.path):
            # Unable to write item to disk
            return False

        # Update metadata
        if not self.hashes or hash_key in self.hashes:
            now = timestamp_utc()

            # Update timestamps
            if self.created_at is None:
                # Set initial timestamps
                self.created_at = now
                self.updated_at = now
            else:
                self.updated_at = now

        # Store hash
        self.hashes[hash_key] = hash

        # Remove duplicate hashes
        for k in list(self.hashes.keys()):
            if self.hashes[k] == hash and k != hash_key:
                del self.hashes[k]

        # Update attributes
        self.media = item.media
        return True
