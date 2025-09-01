"""
Data Management Utilities - Helper functions for managing application data
"""
import streamlit as st
from db.connection import execute_query, fetch_one, fetch_all
from models.student import Student
from models.subject import Subject
from models.marks import Marks

def is_sample_data_present():
    """
    Check if sample data exists in the database
    Returns: bool - True if sample data exists, False otherwise
    """
    try:
        # Check for sample students (the sample data has 10 specific students)
        sample_student_names = [
            "Aarav Sharma", "Priya Patel", "Rohit Kumar", "Sneha Singh", 
            "Vikram Rao", "Anita Desai", "Kiran Reddy", "Meera Joshi", 
            "Arjun Nair", "Deepika Gupta"
        ]
        
        # Check if any of these sample names exist
        for name in sample_student_names:
            result = fetch_one("SELECT COUNT(*) FROM Student WHERE name = ?", (name,))
            if result and result[0] > 0:
                return True
        
        return False
    except Exception as e:
        st.error(f"Error checking sample data: {str(e)}")
        return False

def get_sample_data_info():
    """
    Get information about sample data in the database
    Returns: dict with sample data statistics
    """
    try:
        students = Student.get_all_students()
        subjects = Subject.get_all_subjects()
        marks = Marks.get_all_marks()
        
        return {
            'student_count': len(students) if students else 0,
            'subject_count': len(subjects) if subjects else 0,
            'marks_count': len(marks) if marks else 0,
            'is_sample_data': is_sample_data_present()
        }
    except Exception as e:
        st.error(f"Error getting sample data info: {str(e)}")
        return {
            'student_count': 0,
            'subject_count': 0,
            'marks_count': 0,
            'is_sample_data': False
        }

def delete_sample_data():
    """
    Delete all sample data from the database
    Returns: bool - True if successful, False otherwise
    """
    try:
        # Delete in order due to foreign key constraints
        execute_query("DELETE FROM Marks")
        execute_query("DELETE FROM Student")
        execute_query("DELETE FROM Subject")
        
        return True
    except Exception as e:
        st.error(f"Error deleting sample data: {str(e)}")
        return False

def reset_to_sample_data():
    """
    Clear existing data and restore fresh sample data
    Returns: bool - True if successful, False otherwise
    """
    try:
        from db.connection import initialize_sample_data
        
        # Clear existing data
        execute_query("DELETE FROM Marks")
        execute_query("DELETE FROM Student")
        execute_query("DELETE FROM Subject")
        
        # Reinitialize with sample data
        return initialize_sample_data()
    except Exception as e:
        st.error(f"Error resetting to sample data: {str(e)}")
        return False

def get_data_summary():
    """
    Get a comprehensive summary of all data in the database
    Returns: dict with data summary
    """
    try:
        students = Student.get_all_students()
        subjects = Subject.get_all_subjects()
        marks = Marks.get_all_marks()
        
        # Calculate additional statistics
        if marks:
            total_marks = sum(mark[3] for mark in marks)
            max_possible = sum(mark[4] for mark in marks)
            average_percentage = (total_marks / max_possible * 100) if max_possible > 0 else 0
            
            # Grade distribution
            grade_counts = {}
            for mark in marks:
                percentage = Marks.calculate_percentage(mark[3], mark[4])
                grade = Marks.calculate_grade(percentage)
                grade_counts[grade] = grade_counts.get(grade, 0) + 1
        else:
            average_percentage = 0
            grade_counts = {}
        
        return {
            'total_students': len(students) if students else 0,
            'total_subjects': len(subjects) if subjects else 0,
            'total_assessments': len(marks) if marks else 0,
            'average_percentage': round(average_percentage, 2),
            'grade_distribution': grade_counts,
            'is_sample_data': is_sample_data_present()
        }
    except Exception as e:
        st.error(f"Error getting data summary: {str(e)}")
        return {
            'total_students': 0,
            'total_subjects': 0,
            'total_assessments': 0,
            'average_percentage': 0,
            'grade_distribution': {},
            'is_sample_data': False
        }
