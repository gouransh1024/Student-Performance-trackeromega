"""
Data Import Utilities
Helper functions for importing Excel and CSV files
"""
import pandas as pd
import numpy as np
from datetime import datetime, date
import streamlit as st
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.student import Student
from models.subject import Subject
from models.marks import Marks

def read_file_data(uploaded_file):
    """
    Read data from uploaded file (CSV or Excel)
    
    Args:
        uploaded_file: Streamlit uploaded file object
        
    Returns:
        pandas.DataFrame: The data from the file
    """
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        # Clean column names (remove extra spaces, convert to title case)
        df.columns = df.columns.str.strip().str.title()
        
        return df
    except Exception as e:
        raise Exception(f"Error reading file: {str(e)}")

def create_sample_students_file():
    """Create sample students data for download"""
    sample_data = {
        'Name': ['John Doe', 'Jane Smith', 'Mike Johnson', 'Sarah Wilson', 'David Brown'],
        'Class': ['10', '11', '12', '10', '11'],
        'Section': ['A', 'B', 'C', 'A', 'B'],
        'DOB': ['2008-05-15', '2007-03-20', '2006-11-10', '2008-08-25', '2007-12-05']
    }
    return pd.DataFrame(sample_data)

def create_sample_subjects_file():
    """Create sample subjects data for download"""
    sample_data = {
        'Subject Name': ['Mathematics', 'Physics', 'Chemistry', 'Biology', 'English', 'History', 'Geography']
    }
    return pd.DataFrame(sample_data)

def create_sample_marks_file():
    """Create sample marks data for download"""
    sample_data = {
        'Student ID': [1, 1, 1, 2, 2, 2, 3, 3, 3],
        'Subject ID': [1, 2, 3, 1, 2, 4, 2, 3, 5],
        'Marks Obtained': [85, 78, 92, 88, 75, 82, 90, 85, 79],
        'Max Marks': [100, 100, 100, 100, 100, 100, 100, 100, 100],
        'Assessment Date': ['2024-01-15', '2024-01-16', '2024-01-17', '2024-01-15', '2024-01-16', '2024-01-18', '2024-01-16', '2024-01-17', '2024-01-19'],
        'Assessment Type': ['Final', 'Final', 'Final', 'Final', 'Final', 'Final', 'Final', 'Final', 'Final']
    }
    return pd.DataFrame(sample_data)

def get_file_requirements(import_type):
    """
    Get file requirements for different import types
    
    Args:
        import_type (str): Type of import ('Students', 'Subjects', 'Marks')
        
    Returns:
        dict: Requirements information
    """
    requirements = {
        'Students': {
            'required_columns': ['Name', 'Class', 'Section'],
            'optional_columns': ['DOB'],
            'description': 'Student information including name, class, section, and optional date of birth',
            'format': {
                'Name': 'Text (required)',
                'Class': '10, 11, or 12 (required)',
                'Section': 'A, B, or C (required)',
                'DOB': 'YYYY-MM-DD format (optional)'
            }
        },
        'Subjects': {
            'required_columns': ['Subject Name'],
            'optional_columns': [],
            'description': 'Subject names for the curriculum',
            'format': {
                'Subject Name': 'Text, 2-50 characters (required)'
            }
        },
        'Marks': {
            'required_columns': ['Student ID', 'Subject ID', 'Marks Obtained', 'Max Marks'],
            'optional_columns': ['Assessment Date', 'Assessment Type'],
            'description': 'Student marks for different subjects',
            'format': {
                'Student ID': 'Number (must exist in system)',
                'Subject ID': 'Number (must exist in system)',
                'Marks Obtained': 'Number (0 or positive)',
                'Max Marks': 'Number (greater than 0)',
                'Assessment Date': 'YYYY-MM-DD format (optional)',
                'Assessment Type': 'Text (optional, e.g., "Final", "Mid-term")'
            }
        }
    }
    
    return requirements.get(import_type, {})

def validate_dataframe_structure(df, import_type):
    """
    Validate DataFrame structure for import type
    
    Args:
        df (pandas.DataFrame): Data to validate
        import_type (str): Type of import
        
    Returns:
        tuple: (is_valid, errors, warnings)
    """
    requirements = get_file_requirements(import_type)
    errors = []
    warnings = []
    
    if not requirements:
        errors.append(f"Unknown import type: {import_type}")
        return False, errors, warnings
    
    # Check required columns
    required_columns = requirements['required_columns']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        errors.append(f"Missing required columns: {', '.join(missing_columns)}")
    
    # Check for extra columns
    all_expected_columns = required_columns + requirements.get('optional_columns', [])
    extra_columns = [col for col in df.columns if col not in all_expected_columns]
    if extra_columns:
        warnings.append(f"Extra columns found (will be ignored): {', '.join(extra_columns)}")
    
    return len(errors) == 0, errors, warnings

def get_import_summary(import_type):
    """
    Get summary of current data for import type
    
    Args:
        import_type (str): Type of import
        
    Returns:
        dict: Summary information
    """
    try:
        if import_type == "Students":
            data = Student.get_all_students()
            return {
                'count': len(data),
                'recent': data[-5:] if data else [],
                'message': f"Currently {len(data)} students in the system"
            }
        elif import_type == "Subjects":
            data = Subject.get_all_subjects()
            return {
                'count': len(data),
                'recent': data[-5:] if data else [],
                'message': f"Currently {len(data)} subjects in the system"
            }
        elif import_type == "Marks":
            data = Marks.get_all_marks()
            return {
                'count': len(data),
                'recent': data[-5:] if data else [],
                'message': f"Currently {len(data)} marks records in the system"
            }
    except Exception as e:
        return {
            'count': 0,
            'recent': [],
            'message': f"Error getting data: {str(e)}"
        }
    
    return {
        'count': 0,
        'recent': [],
        'message': "No data available"
    }

def format_import_results(success_count, error_count, total_count, import_errors):
    """
    Format import results for display
    
    Args:
        success_count (int): Number of successful imports
        error_count (int): Number of failed imports
        total_count (int): Total number of records
        import_errors (list): List of error messages
        
    Returns:
        dict: Formatted results
    """
    return {
        'success_count': success_count,
        'error_count': error_count,
        'total_count': total_count,
        'success_rate': (success_count / total_count * 100) if total_count > 0 else 0,
        'errors': import_errors,
        'summary': f"Successfully imported {success_count} out of {total_count} records ({success_count/total_count*100:.1f}% success rate)"
    }

def create_import_log(import_type, results, filename):
    """
    Create a log of the import operation
    
    Args:
        import_type (str): Type of import
        results (dict): Import results
        filename (str): Original filename
        
    Returns:
        str: Log content
    """
    log_content = f"""
Import Log - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
==================================================
File: {filename}
Type: {import_type}
Total Records: {results['total_count']}
Successful: {results['success_count']}
Failed: {results['error_count']}
Success Rate: {results['success_rate']:.1f}%

Errors:
"""
    
    if results['errors']:
        for error in results['errors']:
            log_content += f"- {error}\n"
    else:
        log_content += "- None\n"
    
    return log_content

