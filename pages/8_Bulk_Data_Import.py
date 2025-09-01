"""
Bulk Data Import Page - Import Excel/CSV files for students, subjects, and marks
"""
import streamlit as st
import pandas as pd
import numpy as np
from datetime import date, datetime
import sys
import os
import io

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.student import Student
from models.subject import Subject
from models.marks import Marks

st.set_page_config(
    page_title="Bulk Data Import",
    page_icon="📥",
    layout="wide"
)

st.title("📥 Bulk Data Import")
st.markdown("Import student, subject, and marks data from Excel or CSV files")

# Sidebar for navigation
with st.sidebar:
    st.subheader("Import Options")
    import_type = st.radio(
        "Choose Data Type:",
        ["Students", "Subjects", "Marks"],
        key="import_type"
    )
    
    st.markdown("---")
    st.markdown("### 📋 File Requirements")
    
    if import_type == "Students":
        st.markdown("""
        **Students CSV/Excel Format:**
        - Name (required)
        - Class (required)
        - Section (required)
        - DOB (YYYY-MM-DD format)
        """)
    elif import_type == "Subjects":
        st.markdown("""
        **Subjects CSV/Excel Format:**
        - Subject Name (required)
        """)
    elif import_type == "Marks":
        st.markdown("""
        **Marks CSV/Excel Format:**
        - Student ID (required)
        - Subject ID (required)
        - Marks Obtained (required)
        - Max Marks (required)
        - Assessment Date (YYYY-MM-DD format)
        - Assessment Type (optional)
        """)

def validate_student_data(df):
    """Validate student data from DataFrame"""
    errors = []
    warnings = []
    
    # Check required columns
    required_columns = ['Name', 'Class', 'Section']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        errors.append(f"Missing required columns: {', '.join(missing_columns)}")
        return False, errors, warnings
    
    # Validate data types and values
    for index, row in df.iterrows():
        row_num = index + 2  # Excel rows start from 2 (1 is header)
        
        # Check name
        if pd.isna(row['Name']) or str(row['Name']).strip() == '':
            errors.append(f"Row {row_num}: Name is required")
        
        # Check class
        if pd.isna(row['Class']) or str(row['Class']).strip() == '':
            errors.append(f"Row {row_num}: Class is required")
        elif str(row['Class']) not in ['10', '11', '12']:
            errors.append(f"Row {row_num}: Class must be 10, 11, or 12")
        
        # Check section
        if pd.isna(row['Section']) or str(row['Section']).strip() == '':
            errors.append(f"Row {row_num}: Section is required")
        elif str(row['Section']) not in ['A', 'B', 'C']:
            errors.append(f"Row {row_num}: Section must be A, B, or C")
        
        # Check DOB if present
        if 'DOB' in df.columns and not pd.isna(row['DOB']):
            try:
                if isinstance(row['DOB'], str):
                    datetime.strptime(row['DOB'], '%Y-%m-%d')
                elif isinstance(row['DOB'], datetime):
                    pass  # Already a datetime object
                else:
                    errors.append(f"Row {row_num}: Invalid DOB format. Use YYYY-MM-DD")
            except ValueError:
                errors.append(f"Row {row_num}: Invalid DOB format. Use YYYY-MM-DD")
    
    return len(errors) == 0, errors, warnings

def validate_subject_data(df):
    """Validate subject data from DataFrame"""
    errors = []
    warnings = []
    
    # Check required columns
    if 'Subject Name' not in df.columns:
        errors.append("Missing required column: Subject Name")
        return False, errors, warnings
    
    # Validate data
    for index, row in df.iterrows():
        row_num = index + 2
        
        if pd.isna(row['Subject Name']) or str(row['Subject Name']).strip() == '':
            errors.append(f"Row {row_num}: Subject Name is required")
        elif len(str(row['Subject Name']).strip()) < 2:
            errors.append(f"Row {row_num}: Subject Name must be at least 2 characters")
        elif len(str(row['Subject Name']).strip()) > 50:
            errors.append(f"Row {row_num}: Subject Name must be less than 50 characters")
    
    return len(errors) == 0, errors, warnings

def validate_marks_data(df):
    """Validate marks data from DataFrame"""
    errors = []
    warnings = []
    
    # Check required columns
    required_columns = ['Student ID', 'Subject ID', 'Marks Obtained', 'Max Marks']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        errors.append(f"Missing required columns: {', '.join(missing_columns)}")
        return False, errors, warnings
    
    # Validate data
    for index, row in df.iterrows():
        row_num = index + 2
        
        # Check Student ID
        if pd.isna(row['Student ID']):
            errors.append(f"Row {row_num}: Student ID is required")
        else:
            try:
                student_id = int(row['Student ID'])
                # Check if student exists
                student = Student.get_student_by_id(student_id)
                if not student:
                    errors.append(f"Row {row_num}: Student ID {student_id} does not exist")
            except ValueError:
                errors.append(f"Row {row_num}: Student ID must be a number")
        
        # Check Subject ID
        if pd.isna(row['Subject ID']):
            errors.append(f"Row {row_num}: Subject ID is required")
        else:
            try:
                subject_id = int(row['Subject ID'])
                # Check if subject exists
                subject = Subject.get_subject_by_id(subject_id)
                if not subject:
                    errors.append(f"Row {row_num}: Subject ID {subject_id} does not exist")
            except ValueError:
                errors.append(f"Row {row_num}: Subject ID must be a number")
        
        # Check Marks Obtained
        if pd.isna(row['Marks Obtained']):
            errors.append(f"Row {row_num}: Marks Obtained is required")
        else:
            try:
                marks_obtained = float(row['Marks Obtained'])
                if marks_obtained < 0:
                    errors.append(f"Row {row_num}: Marks Obtained cannot be negative")
            except ValueError:
                errors.append(f"Row {row_num}: Marks Obtained must be a number")
        
        # Check Max Marks
        if pd.isna(row['Max Marks']):
            errors.append(f"Row {row_num}: Max Marks is required")
        else:
            try:
                max_marks = float(row['Max Marks'])
                if max_marks <= 0:
                    errors.append(f"Row {row_num}: Max Marks must be greater than 0")
            except ValueError:
                errors.append(f"Row {row_num}: Max Marks must be a number")
        
        # Check if marks obtained > max marks
        if not pd.isna(row['Marks Obtained']) and not pd.isna(row['Max Marks']):
            try:
                if float(row['Marks Obtained']) > float(row['Max Marks']):
                    errors.append(f"Row {row_num}: Marks Obtained cannot exceed Max Marks")
            except ValueError:
                pass  # Already handled above
        
        # Check Assessment Date if present
        if 'Assessment Date' in df.columns and not pd.isna(row['Assessment Date']):
            try:
                if isinstance(row['Assessment Date'], str):
                    datetime.strptime(row['Assessment Date'], '%Y-%m-%d')
                elif isinstance(row['Assessment Date'], datetime):
                    pass
                else:
                    errors.append(f"Row {row_num}: Invalid Assessment Date format. Use YYYY-MM-DD")
            except ValueError:
                errors.append(f"Row {row_num}: Invalid Assessment Date format. Use YYYY-MM-DD")
    
    return len(errors) == 0, errors, warnings

def import_students_data(df):
    """Import students data from DataFrame"""
    success_count = 0
    error_count = 0
    errors = []
    
    for index, row in df.iterrows():
        try:
            name = str(row['Name']).strip()
            class_name = str(row['Class']).strip()
            section = str(row['Section']).strip()
            
            # Handle DOB
            dob = None
            if 'DOB' in df.columns and not pd.isna(row['DOB']):
                if isinstance(row['DOB'], str):
                    dob = datetime.strptime(row['DOB'], '%Y-%m-%d').date()
                elif isinstance(row['DOB'], datetime):
                    dob = row['DOB'].date()
            
            # Validate data
            valid, validation_errors = Student.validate_student_data(name, class_name, section, dob)
            if not valid:
                errors.append(f"Row {index + 2}: {', '.join(validation_errors)}")
                error_count += 1
                continue
            
            # Add student
            student_id = Student.add_student(name, class_name, section, dob)
            if student_id:
                success_count += 1
            else:
                errors.append(f"Row {index + 2}: Failed to add student")
                error_count += 1
                
        except Exception as e:
            errors.append(f"Row {index + 2}: {str(e)}")
            error_count += 1
    
    return success_count, error_count, errors

def import_subjects_data(df):
    """Import subjects data from DataFrame"""
    success_count = 0
    error_count = 0
    errors = []
    
    for index, row in df.iterrows():
        try:
            subject_name = str(row['Subject Name']).strip()
            
            # Validate data
            valid, validation_errors = Subject.validate_subject_data(subject_name)
            if not valid:
                errors.append(f"Row {index + 2}: {', '.join(validation_errors)}")
                error_count += 1
                continue
            
            # Add subject
            subject_id = Subject.add_subject(subject_name)
            if subject_id:
                success_count += 1
            else:
                errors.append(f"Row {index + 2}: Failed to add subject")
                error_count += 1
                
        except Exception as e:
            errors.append(f"Row {index + 2}: {str(e)}")
            error_count += 1
    
    return success_count, error_count, errors

def import_marks_data(df):
    """Import marks data from DataFrame"""
    success_count = 0
    error_count = 0
    errors = []
    
    for index, row in df.iterrows():
        try:
            student_id = int(row['Student ID'])
            subject_id = int(row['Subject ID'])
            marks_obtained = float(row['Marks Obtained'])
            max_marks = float(row['Max Marks'])
            
            # Handle Assessment Date
            assessment_date = date.today()
            if 'Assessment Date' in df.columns and not pd.isna(row['Assessment Date']):
                if isinstance(row['Assessment Date'], str):
                    assessment_date = datetime.strptime(row['Assessment Date'], '%Y-%m-%d').date()
                elif isinstance(row['Assessment Date'], datetime):
                    assessment_date = row['Assessment Date'].date()
            
            # Handle Assessment Type
            assessment_type = "Final"
            if 'Assessment Type' in df.columns and not pd.isna(row['Assessment Type']):
                assessment_type = str(row['Assessment Type']).strip()
            
            # Validate data
            valid, validation_errors = Marks.validate_marks_data(marks_obtained, max_marks, assessment_date)
            if not valid:
                errors.append(f"Row {index + 2}: {', '.join(validation_errors)}")
                error_count += 1
                continue
            
            # Add marks
            marks_id = Marks.add_marks(student_id, subject_id, marks_obtained, max_marks, assessment_date, assessment_type)
            if marks_id:
                success_count += 1
            else:
                errors.append(f"Row {index + 2}: Failed to add marks")
                error_count += 1
                
        except Exception as e:
            errors.append(f"Row {index + 2}: {str(e)}")
            error_count += 1
    
    return success_count, error_count, errors

# Main content area
st.markdown("---")

# File upload section
st.subheader(f"📁 Upload {import_type} Data File")

uploaded_file = st.file_uploader(
    f"Choose {import_type} file",
    type=['csv', 'xlsx', 'xls'],
    help=f"Upload a CSV or Excel file containing {import_type.lower()} data"
)

if uploaded_file is not None:
    try:
        # Read the file
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        st.success(f"✅ File uploaded successfully! Found {len(df)} rows of data.")
        
        # Display preview
        st.subheader("📋 Data Preview")
        st.dataframe(df.head(10), use_container_width=True)
        
        # Validate data
        st.subheader("🔍 Data Validation")
        with st.spinner("Validating data..."):
            if import_type == "Students":
                is_valid, errors, warnings = validate_student_data(df)
            elif import_type == "Subjects":
                is_valid, errors, warnings = validate_subject_data(df)
            elif import_type == "Marks":
                is_valid, errors, warnings = validate_marks_data(df)
        
        # Display validation results
        if is_valid:
            st.success("✅ All data is valid!")
        else:
            st.error(f"❌ Found {len(errors)} validation errors:")
            for error in errors[:10]:  # Show first 10 errors
                st.write(f"• {error}")
            if len(errors) > 10:
                st.write(f"... and {len(errors) - 10} more errors")
        
        if warnings:
            st.warning("⚠️ Warnings:")
            for warning in warnings:
                st.write(f"• {warning}")
        
        # Import button
        if is_valid:
            st.subheader("🚀 Import Data")
            if st.button(f"Import {len(df)} {import_type.lower()} records", type="primary"):
                with st.spinner(f"Importing {import_type.lower()} data..."):
                    if import_type == "Students":
                        success_count, error_count, import_errors = import_students_data(df)
                    elif import_type == "Subjects":
                        success_count, error_count, import_errors = import_subjects_data(df)
                    elif import_type == "Marks":
                        success_count, error_count, import_errors = import_marks_data(df)
                
                # Display import results
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("✅ Successfully Imported", success_count)
                with col2:
                    st.metric("❌ Failed", error_count)
                with col3:
                    st.metric("📊 Total Records", len(df))
                
                if import_errors:
                    with st.expander("❌ Import Errors"):
                        for error in import_errors:
                            st.write(f"• {error}")
                
                if success_count > 0:
                    st.success(f"🎉 Successfully imported {success_count} {import_type.lower()} records!")
                    
                    # Show recent additions
                    with st.expander("📋 Recent Additions"):
                        if import_type == "Students":
                            recent_data = Student.get_all_students()[-5:]
                            for student in recent_data:
                                st.write(f"• {student[1]} (Class {student[2]}-{student[3]})")
                        elif import_type == "Subjects":
                            recent_data = Subject.get_all_subjects()[-5:]
                            for subject in recent_data:
                                st.write(f"• {subject[1]}")
                        elif import_type == "Marks":
                            st.write("Marks data imported successfully")
        
    except Exception as e:
        st.error(f"❌ Error reading file: {str(e)}")

# Sample file download section
st.markdown("---")
st.subheader("📄 Download Sample Files")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📥 Download Sample Students CSV"):
        sample_students = pd.DataFrame({
            'Name': ['John Doe', 'Jane Smith', 'Mike Johnson'],
            'Class': ['10', '11', '12'],
            'Section': ['A', 'B', 'C'],
            'DOB': ['2008-05-15', '2007-03-20', '2006-11-10']
        })
        csv = sample_students.to_csv(index=False)
        st.download_button(
            label="Download Sample Students CSV",
            data=csv,
            file_name="sample_students.csv",
            mime="text/csv"
        )

with col2:
    if st.button("📥 Download Sample Subjects CSV"):
        sample_subjects = pd.DataFrame({
            'Subject Name': ['Mathematics', 'Physics', 'Chemistry', 'Biology', 'English']
        })
        csv = sample_subjects.to_csv(index=False)
        st.download_button(
            label="Download Sample Subjects CSV",
            data=csv,
            file_name="sample_subjects.csv",
            mime="text/csv"
        )

with col3:
    if st.button("📥 Download Sample Marks CSV"):
        sample_marks = pd.DataFrame({
            'Student ID': [1, 1, 2, 2, 3],
            'Subject ID': [1, 2, 1, 3, 2],
            'Marks Obtained': [85, 78, 92, 88, 75],
            'Max Marks': [100, 100, 100, 100, 100],
            'Assessment Date': ['2024-01-15', '2024-01-16', '2024-01-15', '2024-01-17', '2024-01-16'],
            'Assessment Type': ['Final', 'Final', 'Final', 'Final', 'Final']
        })
        csv = sample_marks.to_csv(index=False)
        st.download_button(
            label="Download Sample Marks CSV",
            data=csv,
            file_name="sample_marks.csv",
            mime="text/csv"
        )

# Instructions section
st.markdown("---")
st.subheader("📖 Instructions")

with st.expander("How to use Bulk Import"):
    st.markdown("""
    ### Step-by-Step Guide:
    
    1. **Prepare Your Data**: Create a CSV or Excel file with the required columns
    2. **Download Sample Files**: Use the sample files above as templates
    3. **Upload File**: Choose your file using the upload button
    4. **Validate Data**: The system will automatically validate your data
    5. **Import**: Click the import button to add the data to the system
    
    ### File Format Requirements:
    
    **Students File:**
    - Name (required): Student's full name
    - Class (required): 10, 11, or 12
    - Section (required): A, B, or C
    - DOB (optional): Date of birth in YYYY-MM-DD format
    
    **Subjects File:**
    - Subject Name (required): Name of the subject
    
    **Marks File:**
    - Student ID (required): Existing student ID from the system
    - Subject ID (required): Existing subject ID from the system
    - Marks Obtained (required): Numeric value
    - Max Marks (required): Numeric value
    - Assessment Date (optional): Date in YYYY-MM-DD format
    - Assessment Type (optional): Type of assessment (e.g., "Final", "Mid-term")
    
    ### Tips:
    - Use the sample files as templates
    - Ensure all required fields are filled
    - Check that Student IDs and Subject IDs exist in the system
    - Use consistent date formats (YYYY-MM-DD)
    """)

# Current data summary
st.markdown("---")
st.subheader("📊 Current Data Summary")

col1, col2, col3 = st.columns(3)

with col1:
    try:
        students_count = len(Student.get_all_students())
        st.metric("👥 Total Students", students_count)
    except:
        st.metric("👥 Total Students", 0)

with col2:
    try:
        subjects_count = len(Subject.get_all_subjects())
        st.metric("📚 Total Subjects", subjects_count)
    except:
        st.metric("📚 Total Subjects", 0)

with col3:
    try:
        marks_count = len(Marks.get_all_marks())
        st.metric("📝 Total Marks Records", marks_count)
    except:
        st.metric("📝 Total Marks Records", 0)

