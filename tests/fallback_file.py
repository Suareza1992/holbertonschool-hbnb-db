import unittest
import json
import tempfile
import os
from unittest.mock import mock_open, patch

class TestFileBasedOperations(unittest.TestCase):
    def setUp(self):
        # Setup a temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, mode='w+', suffix='.json')
        self.file_path = self.temp_file.name
        json.dump({"initial": "data"}, self.temp_file)
        self.temp_file.close()

    def test_create_entity_file(self):
        # Test creating an entity in the file
        new_data = {"key": "value"}
        with open(self.file_path, 'w') as f:
            json.dump(new_data, f)
        with open(self.file_path, 'r') as f:
            data = json.load(f)
        self.assertEqual(data, new_data)

    def test_read_entity_file(self):
        # Test reading the initial data
        with open(self.file_path, 'r') as f:
            data = json.load(f)
        self.assertEqual(data, {"initial": "data"})

    def test_update_entity_file(self):
        # Test updating an entity in the file
        update_data = {"key": "updated value"}
        with open(self.file_path, 'w') as f:
            json.dump(update_data, f)
        with open(self.file_path, 'r') as f:
            data = json.load(f)
        self.assertEqual(data, update_data)

    def test_delete_entity_file(self):
        # Test deleting the file
        os.remove(self.file_path)
        self.assertFalse(os.path.exists(self.file_path))

    def test_read_from_nonexistent_file(self):
        # Test error handling for non-existent file
        with self.assertRaises(FileNotFoundError):
            with open('nonexistent.json', 'r') as f:
                json.load(f)

    def test_handle_corrupt_json(self):
        # Test handling of corrupt JSON
        with open(self.file_path, 'w') as f:
            f.write('{"key": "value"')  # intentionally malformed JSON
        with self.assertRaises(json.JSONDecodeError):
            with open(self.file_path, 'r') as f:
                json.load(f)

    def test_create_entity_with_mock(self):
        # Test file operations using mock
        mock_data = {"key": "mocked value"}
        m = mock_open()
        with patch('builtins.open', m):
            with open(self.file_path, 'w') as f:
                json.dump(mock_data, f)
            m.assert_called_once_with(self.file_path, 'w')
            handle = m.return_value
            handle.write.assert_called_once_with(json.dumps(mock_data))

    def tearDown(self):
        # Clean up the temporary file
        if os.path.exists(self.file_path):
            os.unlink(self.file_path)

if __name__ == "__main__":
    unittest.main()

