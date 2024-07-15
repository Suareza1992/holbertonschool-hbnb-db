import os
import unittest
import ast
import argparse
import pycodestyle
from concurrent.futures import ThreadPoolExecutor

class TestDocumentation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        parser = argparse.ArgumentParser(description="Check Python files for docstrings and PEP8 compliance.")
        parser.add_argument('--path', default='./src', help='Root directory to check for Python files')
        args, unknown = parser.parse_known_args()
        cls.root_dir = args.path

    def test_documentation(self):
        """Check if all modules, classes, functions, and methods have docstrings."""
        with ThreadPoolExecutor() as executor:
            futures = []
            for root, dirs, files in os.walk(self.root_dir):
                for file in files:
                    if file.endswith(".py"):
                        file_path = os.path.join(root, file)
                        futures.append(executor.submit(self.process_file, file_path))
            for future in futures:
                future.result()

    def process_file(self, file_path):
        """Read and parse a Python file, checking for docstrings."""
        with open(file_path, "r", encoding="utf-8") as f:
            file_content = f.read()
        tree = ast.parse(file_content, filename=file_path)
        self.check_docstrings(tree, file_path)

    def check_docstrings(self, node, file_path):
        """Recursively check if all relevant Python structures have docstrings."""
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            self.assertIsNotNone(
                ast.get_docstring(node),
                f"No docstring in {node.__class__.__name__} '{getattr(node, 'name', 'module')}' in file {file_path}"
            )
        for child in ast.iter_child_nodes(node):
            self.check_docstrings(child, file_path)

    def test_pep8_compliance(self):
        """Check the root directory for PEP8 compliance using pycodestyle."""
        style_guide = pycodestyle.StyleGuide(quiet=False)
        report = style_guide.check_files([self.root_dir])
        if report.total_errors > 0:
            for error in report.messages:
                print(f"PEP8 violation: {error}")
        self.assertEqual(report.total_errors, 0, "PEP8 violations detected.")

    def tearDown(self):
        """Cleanup actions (if any needed post-tests)."""
        pass

if __name__ == "__main__":
    unittest.main()

