"""
Bulk Import Demo Script
Demonstrates how to use the bulk import functionality
"""
import pandas as pd
import sys
import os
from datetime import date

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.data_import import (
    create_sample_students_file,
    create_sample_subjects_file,
    create_sample_marks_file,
    get_file_requirements,
    validate_dataframe_structure,
    format_import_results
)

def demo_students_import():
    """Demonstrate students import functionality"""
    print("📚 Students Import Demo")
    print("=" * 40)
    
    # Create sample data
    students_df = create_sample_students_file()
    print(f"Created sample students data with {len(students_df)} records")
    print("\nSample data:")
    print(students_df.head())
    
    # Get requirements
    requirements = get_file_requirements('Students')
    print(f"\nRequired columns: {requirements['required_columns']}")
    print(f"Optional columns: {requirements.get('optional_columns', [])}")
    
    # Validate structure
    is_valid, errors, warnings = validate_dataframe_structure(students_df, 'Students')
    print(f"\nValidation results:")
    print(f"  Valid: {is_valid}")
    print(f"  Errors: {len(errors)}")
    print(f"  Warnings: {len(warnings)}")
    
    if errors:
        print("  Error details:")
        for error in errors:
            print(f"    - {error}")
    
    if warnings:
        print("  Warning details:")
        for warning in warnings:
            print(f"    - {warning}")
    
    print("\n" + "-" * 40)

def demo_subjects_import():
    """Demonstrate subjects import functionality"""
    print("📖 Subjects Import Demo")
    print("=" * 40)
    
    # Create sample data
    subjects_df = create_sample_subjects_file()
    print(f"Created sample subjects data with {len(subjects_df)} records")
    print("\nSample data:")
    print(subjects_df.head())
    
    # Get requirements
    requirements = get_file_requirements('Subjects')
    print(f"\nRequired columns: {requirements['required_columns']}")
    
    # Validate structure
    is_valid, errors, warnings = validate_dataframe_structure(subjects_df, 'Subjects')
    print(f"\nValidation results:")
    print(f"  Valid: {is_valid}")
    print(f"  Errors: {len(errors)}")
    print(f"  Warnings: {len(warnings)}")
    
    print("\n" + "-" * 40)

def demo_marks_import():
    """Demonstrate marks import functionality"""
    print("📝 Marks Import Demo")
    print("=" * 40)
    
    # Create sample data
    marks_df = create_sample_marks_file()
    print(f"Created sample marks data with {len(marks_df)} records")
    print("\nSample data:")
    print(marks_df.head())
    
    # Get requirements
    requirements = get_file_requirements('Marks')
    print(f"\nRequired columns: {requirements['required_columns']}")
    print(f"Optional columns: {requirements.get('optional_columns', [])}")
    
    # Validate structure
    is_valid, errors, warnings = validate_dataframe_structure(marks_df, 'Marks')
    print(f"\nValidation results:")
    print(f"  Valid: {is_valid}")
    print(f"  Errors: {len(errors)}")
    print(f"  Warnings: {len(warnings)}")
    
    print("\n" + "-" * 40)

def demo_import_results():
    """Demonstrate import results formatting"""
    print("📊 Import Results Demo")
    print("=" * 40)
    
    # Simulate import results
    success_count = 45
    error_count = 5
    total_count = 50
    import_errors = [
        "Row 12: Student ID 999 does not exist",
        "Row 23: Marks Obtained cannot exceed Max Marks",
        "Row 34: Invalid date format for Assessment Date",
        "Row 41: Subject ID 15 does not exist",
        "Row 47: Marks Obtained cannot be negative"
    ]
    
    results = format_import_results(success_count, error_count, total_count, import_errors)
    
    print(f"Import Summary:")
    print(f"  Successfully imported: {results['success_count']}")
    print(f"  Failed: {results['error_count']}")
    print(f"  Total records: {results['total_count']}")
    print(f"  Success rate: {results['success_rate']:.1f}%")
    print(f"  Summary: {results['summary']}")
    
    print(f"\nError details:")
    for error in results['errors']:
        print(f"  - {error}")
    
    print("\n" + "-" * 40)

def demo_file_creation():
    """Demonstrate creating and saving sample files"""
    print("💾 File Creation Demo")
    print("=" * 40)
    
    # Create sample files
    students_df = create_sample_students_file()
    subjects_df = create_sample_subjects_file()
    marks_df = create_sample_marks_file()
    
    # Save to CSV files
    students_df.to_csv('sample_students.csv', index=False)
    subjects_df.to_csv('sample_subjects.csv', index=False)
    marks_df.to_csv('sample_marks.csv', index=False)
    
    print("Created sample CSV files:")
    print("  - sample_students.csv")
    print("  - sample_subjects.csv")
    print("  - sample_marks.csv")
    
    print("\nYou can now use these files to test the bulk import functionality!")
    print("\n" + "-" * 40)

def main():
    """Run all demos"""
    print("🎓 Student Performance Tracker - Bulk Import Demo")
    print("=" * 60)
    print("This demo shows how the bulk import functionality works.")
    print("You can use this to understand the data formats and validation.")
    print()
    
    # Run all demos
    demo_students_import()
    demo_subjects_import()
    demo_marks_import()
    demo_import_results()
    demo_file_creation()
    
    print("✅ Demo completed successfully!")
    print("\nNext steps:")
    print("1. Run the Streamlit app: streamlit run app.py")
    print("2. Navigate to 'Bulk Data Import' page")
    print("3. Use the sample files created in this demo")
    print("4. Test the import functionality with your own data")

if __name__ == "__main__":
    main()
