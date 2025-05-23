import random
import string
import os

class UniqueIDGenerator:
    def __init__(self, file_path='last_id.txt'):
        """Initialize the ID generator with a file to store the last ID."""
        self.file_path = file_path
        self.generated_ids = set()
        self.load_last_ids()

    def load_last_ids(self):
        """Load previously generated IDs from the file, if it exists."""
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                for line in file:
                    self.generated_ids.add(line.strip())

    def generate_id(self):
        """Generate a unique ID that is not sortable."""
        while True:
            unique_id = self._create_random_id()
            if unique_id not in self.generated_ids:
                self.generated_ids.add(unique_id)
                self.save_last_id(unique_id)
                return unique_id

    def _create_random_id(self):
        """Create a random 10-character long ID using letters and digits."""
        characters = string.ascii_letters + string.digits
        return ''.join(random.choices(characters, k=10))

    def save_last_id(self, unique_id):
        """Save the newly generated ID to the file."""
        with open(self.file_path, 'a') as file:
            file.write(unique_id + '\n')

# Example usage
if __name__ == "__main__":
    id_generator = UniqueIDGenerator()

    # Generate 5 unique IDs
    for _ in range(5):
        print(id_generator.generate_id())

