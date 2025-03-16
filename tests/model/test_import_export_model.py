import unittest
from unittest.mock import Mock
from model.import_export_model import ImportExportModel
import os
import tempfile


class TestImportExportModel(unittest.TestCase):
    def setUp(self):
        self.mock_contact_model = Mock()
        self.model = ImportExportModel(self.mock_contact_model)

    def test_export_contacts_success(self):
        # Setup mock contacts
        mock_contact1 = Mock()
        mock_contact1.name = "John Doe"
        mock_contact1.phone = "1234567890"
        mock_contact2 = Mock()
        mock_contact2.name = "Jane Smith"
        mock_contact2.phone = "0987654321"
        self.mock_contact_model.get_all_contacts.return_value = [
            mock_contact1,
            mock_contact2,
        ]

        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            file_path = temp_file.name

        # Test export
        success, message = self.model.export_contacts_to_file(file_path)

        # Verify results
        self.assertTrue(success)
        self.assertIn("successfully exported", message)

        # Verify file content
        with open(file_path, "r") as f:
            content = f.read()
            self.assertIn("John Doe, 1234567890", content)
            self.assertIn("Jane Smith, 0987654321", content)

        # Cleanup
        os.unlink(file_path)

    def test_export_no_contacts(self):
        self.mock_contact_model.get_all_contacts.return_value = []

        success, message = self.model.export_contacts_to_file("dummy.txt")

        self.assertFalse(success)
        self.assertEqual(message, "There are no contacts to export.")

    def test_import_contacts_success(self):
        # Create test file
        test_content = """John Doe, 1234567890 
                          Jane Smith, 0987654321
                        """

        with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
            temp_file.write(test_content)
            file_path = temp_file.name

        # Test import
        success, message = self.model.import_contacts_from_file(file_path)

        # Verify results
        self.assertTrue(success)
        self.assertIn("Successfully imported 2 contact(s)", message)

        # Verify contacts were added
        self.mock_contact_model.add_contact.assert_any_call("John Doe", "1234567890")
        self.mock_contact_model.add_contact.assert_any_call("Jane Smith", "0987654321")

        # Cleanup
        os.unlink(file_path)

    def test_import_invalid_lines(self):
        # Create test file with invalid lines
        test_content = """John Doe, 1234567890
                          Invalid Line
                          Jane Smith, 0987654321
                          Another Invalid Line"""

        with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
            temp_file.write(test_content)
            file_path = temp_file.name

        # Test import
        success, message = self.model.import_contacts_from_file(file_path)

        # Verify results
        self.assertTrue(success)
        self.assertIn("Successfully imported 2 contact(s)", message)
        self.assertIn("Warning: 2 line(s) could not be imported", message)

        # Cleanup
        os.unlink(file_path)

    def test_import_no_valid_contacts(self):
        # Create test file with only invalid lines
        test_content = """Invalid Line 1
                          Invalid Line 2
                        """

        with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
            temp_file.write(test_content)
            file_path = temp_file.name

        # Test import
        success, message = self.model.import_contacts_from_file(file_path)

        # Verify results
        self.assertFalse(success)
        self.assertIn("No contacts were imported", message)

        # Cleanup
        os.unlink(file_path)

    def test_file_errors(self):
        # Test export to invalid path
        success, message = self.model.export_contacts_to_file("/invalid/path/file.txt")
        self.assertFalse(success)
        self.assertIn("Error exporting contacts", message)

        # Test import from non-existent file
        success, message = self.model.import_contacts_from_file("nonexistent.txt")
        self.assertFalse(success)
        self.assertIn("Error importing contacts", message)


if __name__ == "__main__":
    unittest.main()
