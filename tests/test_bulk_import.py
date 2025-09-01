"""
Test cases for bulk data import functionality
"""
import unittest
import sys
import os
import pandas as pd
from datetime import date, datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_import import (
    create_sample_students_file,
    create_sample_subjects_file,
    create_sample_marks_file,
    get_file_requirements,
    validate_dataframe_structure,
    format_import_results
)

class TestBulkImport(unittest.TestCase):
    """Test cases for bulk import functionality"""

    def test_create_sample_students_file(self):
        """Test sample students file creation"""
        df = create_sample_students_file()
        
        # Check structure
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 5)
        self.assertListEqual(list(df.columns), ['Name', 'Class', 'Section', 'DOB'])
        
        # Check data types
        self.assertTrue(all(df['Class'].isin(['10', '11', '12'])))
        self.assertTrue(all(df['Section'].isin(['A', 'B', 'C'])))

    def test_create_sample_subjects_file(self):
        """Test sample subjects file creation"""
        df = create_sample_subjects_file()
        
        # Check structure
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 7)
        self.assertListEqual(list(df.columns), ['Subject Name'])
        
        # Check data
        self.assertIn('Mathematics', df['Subject Name'].values)

    def test_create_sample_marks_file(self):
        """Test sample marks file creation"""
        df = create_sample_marks_file()
        
        # Check structure
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 9)
        expected_columns = ['Student ID', 'Subject ID', 'Marks Obtained', 'Max Marks', 'Assessment Date', 'Assessment Type']
        self.assertListEqual(list(df.columns), expected_columns)
        
        # Check data types
        self.assertTrue(all(df['Marks Obtained'] >= 0))
        self.assertTrue(all(df['Max Marks'] > 0))

    def test_get_file_requirements(self):
        """Test file requirements retrieval"""
        # Test students requirements
        students_req = get_file_requirements('Students')
        self.assertIn('required_columns', students_req)
        self.assertIn('Name', students_req['required_columns'])
        self.assertIn('Class', students_req['required_columns'])
        self.assertIn('Section', students_req['required_columns'])
        
        # Test subjects requirements
        subjects_req = get_file_requirements('Subjects')
        self.assertIn('required_columns', subjects_req)
        self.assertIn('Subject Name', subjects_req['required_columns'])
        
        # Test marks requirements
        marks_req = get_file_requirements('Marks')
        self.assertIn('required_columns', marks_req)
        self.assertIn('Student ID', marks_req['required_columns'])
        self.assertIn('Subject ID', marks_req['required_columns'])
        
        # Test unknown type
        unknown_req = get_file_requirements('Unknown')
        self.assertEqual(unknown_req, {})

    def test_validate_dataframe_structure(self):
        """Test DataFrame structure validation"""
        # Test valid students data
        valid_students = pd.DataFrame({
            'Name': ['John Doe', 'Jane Smith'],
            'Class': ['10', '11'],
            'Section': ['A', 'B'],
            'DOB': ['2008-05-15', '2007-03-20']
        })
        is_valid, errors, warnings = validate_dataframe_structure(valid_students, 'Students')
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)
        
        # Test missing required columns
        invalid_students = pd.DataFrame({
            'Name': ['John Doe'],
            'Class': ['10']
            # Missing Section column
        })
        is_valid, errors, warnings = validate_dataframe_structure(invalid_students, 'Students')
        self.assertFalse(is_valid)
        self.assertIn('Section', errors[0])
        
        # Test extra columns (should be warning, not error)
        extra_columns_students = pd.DataFrame({
            'Name': ['John Doe'],
            'Class': ['10'],
            'Section': ['A'],
            'Extra Column': ['Extra Data']
        })
        is_valid, errors, warnings = validate_dataframe_structure(extra_columns_students, 'Students')
        self.assertTrue(is_valid)
        self.assertIn('Extra Column', warnings[0])

    def test_format_import_results(self):
        """Test import results formatting"""
        results = format_import_results(8, 2, 10, ['Error 1', 'Error 2'])
        
        self.assertEqual(results['success_count'], 8)
        self.assertEqual(results['error_count'], 2)
        self.assertEqual(results['total_count'], 10)
        self.assertEqual(results['success_rate'], 80.0)
        self.assertEqual(len(results['errors']), 2)
        self.assertIn('80.0% success rate', results['summary'])

    def test_sample_data_integrity(self):
        """Test that sample data meets validation requirements"""
        # Test students sample data
        students_df = create_sample_students_file()
        is_valid, errors, warnings = validate_dataframe_structure(students_df, 'Students')
        self.assertTrue(is_valid, f"Students sample data validation failed: {errors}")
        
        # Test subjects sample data
        subjects_df = create_sample_subjects_file()
        is_valid, errors, warnings = validate_dataframe_structure(subjects_df, 'Subjects')
        self.assertTrue(is_valid, f"Subjects sample data validation failed: {errors}")
        
        # Test marks sample data
        marks_df = create_sample_marks_file()
        is_valid, errors, warnings = validate_dataframe_structure(marks_df, 'Marks')
        self.assertTrue(is_valid, f"Marks sample data validation failed: {errors}")

def run_bulk_import_tests():
    """Run all bulk import tests"""
    test_suite = unittest.TestSuite()
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestBulkImport))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    return result

if __name__ == "__main__":
    print("🧪 Testing Bulk Import Functionality")
    print("=" * 50)
    
    result = run_bulk_import_tests()
    
    print(f"\n📊 Test Results:")
    print(f"   Tests Run: {result.testsRun}")
    print(f"   Failures: {len(result.failures)}")
    print(f"   Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n🎉 All bulk import tests passed!")
    else:
        print("\n❌ Some tests failed. Check the output above for details.")

