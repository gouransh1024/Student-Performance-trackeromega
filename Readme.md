# 🎓 Student Performance Tracker
> **A comprehensive web-based academic management system built with Streamlit and SQLite for tracking student performance, generating analytics, and managing educational data.**

## 🚀 Live Demo

**[🌐 Access the Application]((https://student-performance-trackeromega-adjsjs6zxkq5btxzrchwtu.streamlit.app/))**

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage Guide](#usage-guide)
- [Project Structure](#project-structure)
- [Technical Implementation](#technical-implementation)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## 🎯 Overview

The **Student Performance Tracker** is a full-stack web application designed to streamline academic performance management for educational institutions. Built with modern web technologies, it provides real-time analytics, automated grade calculations, and comprehensive reporting capabilities.

### 🎨 Key Highlights

- **📊 Real-time Analytics**: Live performance dashboards with interactive visualizations
- **🎯 Automated Grading**: Intelligent grade calculation system (A+ to F)
- **📱 Responsive Design**: Cross-platform compatibility with modern UI/UX
- **⚡ SQLite Database**: Lightweight, portable database with optimized queries
- **🛡️ Data Validation**: Comprehensive input validation and error handling
- **📤 Export Capabilities**: CSV export for all data types

## ✨ Features

### 👥 **Student Management System**
- Complete CRUD operations with search and filtering
- Class and section-based organization (10A, 10B, 11A, etc.)
- Student profile management with date of birth tracking
- Bulk data export functionality
- Advanced search with multiple criteria

### 📚 **Subject Management**
- Dynamic subject creation and organization
- Quick-add functionality for common subjects
- Subject-wise performance tracking
- Unique subject validation to prevent duplicates

### 📝 **Assessment & Marks Management**
- Flexible marks entry with multiple assessment types (Quiz, Assignment, Midterm, Final)
- Real-time percentage calculation and grade assignment
- Assessment date tracking and validation
- Maximum marks customization (default: 100)
- Input validation to prevent invalid data entry

### 📥 **Bulk Data Import**
- Excel and CSV file import for students, subjects, and marks
- Comprehensive data validation with detailed error reporting
- Sample file templates for easy data preparation
- Batch processing for large datasets
- Import statistics and success rate tracking

### 📋 **Performance Analytics & Reporting**
- Individual student report cards with detailed breakdowns
- Class-wise performance analytics with comparative metrics
- Subject-wise performance analysis and trends
- Grade distribution analysis across classes
- Pass/fail rate tracking with visual indicators
- Top performers identification and ranking

### 📊 **Interactive Visualizations**
- Grade distribution pie charts and bar graphs
- Class performance comparison charts
- Subject performance analysis with range visualization
- Performance trends over time
- Pass/fail analysis with risk assessment
- Top performers leaderboard with ranking

### ⚙️ **System Administration**
- Database management and monitoring
- Sample data generation for testing
- Data backup and export functionality
- Application settings and preferences
- System statistics and health monitoring

## 🛠️ Tech Stack

### **Frontend & Web Framework**
- **[Streamlit](https://streamlit.io/)** - Modern web app framework for rapid development
- **[Pandas](https://pandas.pydata.org/)** - Data manipulation and analysis
- **[Plotly](https://plotly.com/)** - Interactive data visualizations
- **[Altair](https://altair-viz.github.io/)** - Statistical visualizations

### **Backend & Database**
- **[Python 3.8+](https://www.python.org/)** - Core programming language
- **[SQLite](https://www.sqlite.org/)** - Lightweight, serverless database
- **[SQLAlchemy-style queries](https://www.sqlalchemy.org/)** - Optimized database operations

### **Development & Deployment**
- **Git** - Version control
- **GitHub** - Code repository and collaboration
- **Streamlit Cloud** - Cloud deployment platform

## 🚀 Installation

### **Prerequisites**
- Python 3.8 or higher
- Git (for cloning the repository)

### **Quick Start**

1. **Clone the Repository**
```bash
git clone https://github.com/gouransh1024/Student-Performance-tracker.git
cd student-performance-tracker
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the Application**
```bash
streamlit run app.py
```

4. **Access the Application**
- Open your browser and navigate to `http://localhost:8501`
- The database will be automatically initialized with sample data

### **Alternative Setup**
```bash
python install.py  # For Python 3.13 compatibility
```

## 📖 Usage Guide

### **Getting Started Workflow**
1. **🏠 Dashboard**: Overview of system statistics and quick actions
2. **👥 Manage Students**: Add, edit, delete, and search students
3. **📚 Manage Subjects**: Create and organize subject curriculum
4. **📝 Enter Marks**: Input student assessments and grades
5. **📋 Report Cards**: Generate individual student reports
6. **📊 Class Analytics**: Analyze class and section performance
7. **📈 Visual Reports**: Interactive charts and insights
8. **⚙️ Settings**: Configure application preferences

### **Key Operations**
- **Adding Students**: Navigate to "Manage Students" → "Add New Student"
- **Entering Marks**: Go to "Enter Marks" → Select student and subject → Input scores
- **Viewing Analytics**: Access "Class Analytics" → Select class/section → View insights
- **Exporting Data**: Use export buttons in any section → Download CSV files
- **Bulk Import**: Go to "Bulk Data Import" → Upload Excel/CSV files for students, subjects, or marks

## 📁 Project Structure

```
student-performance-tracker/
├── 📄 app.py                    # Main application entry point
├── 📂 pages/                    # Streamlit pages
│   ├── 1_Manage_Students.py     # Student management interface
│   ├── 2_Manage_Subjects.py     # Subject management interface
│   ├── 3_Enter_Update_Marks.py  # Marks entry and updating
│   ├── 4_Student_Report_Card.py # Individual report generation
│   ├── 5_Class_Analytics.py     # Class performance analytics
│   ├── 6_Visual_Reports.py      # Interactive visual dashboards
│   ├── 7_Settings.py            # Application configuration
│   └── 8_Bulk_Data_Import.py    # Bulk data import functionality
├── 📂 models/                   # Data models and business logic
│   ├── student.py               # Student model and operations
│   ├── subject.py               # Subject model and operations
│   └── marks.py                 # Marks model and calculations
├── 📂 db/                       # Database layer
│   └── connection.py            # SQLite connection and utilities
├── 📂 utils/                    # Utility functions
│   ├── analytics.py             # Advanced analytics functions
│   └── data_import.py           # Data import utilities
├── 📂 tests/                    # Test suite
│   └── test_cases.py            # Unit and integration tests
├── 📄 requirements.txt          # Python dependencies
├── 📄 install.py                # Installation script
├── 📄 README.md                 # Project documentation
└── 📄 student_tracker.db        # SQLite database (auto-generated)
```

## 🔧 Technical Implementation

### **Database Schema**

#### **Student Table**
```sql
CREATE TABLE Student (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL CHECK(length(trim(name)) >= 2),
    class TEXT NOT NULL CHECK(class IN ('10', '11', '12')),
    section TEXT NOT NULL CHECK(section IN ('A', 'B', 'C')),
    dob DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

#### **Subject Table**
```sql
CREATE TABLE Subject (
    subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_name TEXT NOT NULL UNIQUE CHECK(length(trim(subject_name)) >= 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

#### **Marks Table**
```sql
CREATE TABLE Marks (
    mark_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    subject_id INTEGER NOT NULL,
    marks_obtained INTEGER NOT NULL CHECK(marks_obtained >= 0),
    max_marks INTEGER DEFAULT 100 CHECK(max_marks > 0),
    assessment_date DATE DEFAULT (date('now')),
    assessment_type TEXT DEFAULT 'Assignment' 
        CHECK(assessment_type IN ('Quiz', 'Assignment', 'Midterm', 'Final', 'Project')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES Student(student_id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES Subject(subject_id) ON DELETE CASCADE,
    CHECK(marks_obtained <= max_marks)
)
```

### **Grade Calculation System**

| Percentage Range | Grade | Description |
| :-- | :-- | :-- |
| 90% - 100% | A+ | Outstanding |
| 80% - 89% | A | Excellent |
| 70% - 79% | B+ | Very Good |
| 60% - 69% | B | Good |
| 50% - 59% | C+ | Above Average |
| 40% - 49% | C | Average |
| Below 40% | F | Fail |

### **Key Algorithms**

#### **Percentage Calculation**
```python
def calculate_percentage(marks_obtained: int, max_marks: int) -> float:
    if max_marks == 0:
        return 0.0
    return round((marks_obtained / max_marks) * 100, 2)
```

#### **Grade Assignment**
```python
def calculate_grade(percentage: float) -> str:
    if percentage >= 90: return "A+"
    elif percentage >= 80: return "A"
    elif percentage >= 70: return "B+"
    elif percentage >= 60: return "B"
    elif percentage >= 50: return "C+"
    elif percentage >= 40: return "C"
    else: return "F"
```

### **Performance Optimizations**
- **Database Indexing**: Optimized queries with proper indexes
- **Connection Pooling**: Efficient database connection management
- **Caching**: Streamlit caching for improved performance
- **Query Optimization**: Optimized SQL queries for large datasets

## 📸 Screenshots

### **Dashboard Overview**
<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/6896945d-9d6d-4851-87b9-6d414d8bdf12" />

### **Student Management**
<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/3195144f-a1c0-4513-9618-88e600023dc8" />
<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/8445f026-a758-4fba-a6c1-c4d224179af2" />

### **Class Analytics**
<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/db6ce9e3-1cae-47d4-9db8-689a11d04191" />
<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/bba74870-aebc-4fea-b137-d10ec56647e3" />

### **Visual Reports**
<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/82884151-a05c-4a4f-9d3f-cf3f5bde0d8d" />
<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/7eb677ce-8012-400d-88bd-cd8b74381585" />

## 🤝 Contributing

We welcome contributions to improve the Student Performance Tracker! Here's how you can help:

### **Getting Started**

1. **Fork the Repository**
```bash
git fork https://github.com/gouransh1024/Student-Performance-tracker.git
```

2. **Create a Feature Branch**
```bash
git checkout -b feature/amazing-feature
```

3. **Make Your Changes**
   - Follow Python PEP 8 style guidelines
   - Add tests for new functionality
   - Update documentation as needed

4. **Commit Your Changes**
```bash
git commit -m "Add amazing feature"
```

5. **Push to Your Branch**
```bash
git push origin feature/amazing-feature
```

6. **Open a Pull Request**

### **Development Guidelines**
- **Code Style**: Follow PEP 8 conventions
- **Testing**: Add unit tests for new features
- **Documentation**: Update README and inline docs
- **Commits**: Use clear, descriptive commit messages

### **Areas for Contribution**
- 🔧 **New Features**: Additional analytics, reporting capabilities
- 🐛 **Bug Fixes**: Identify and resolve issues
- 📚 **Documentation**: Improve guides and examples
- 🎨 **UI/UX**: Enhance user interface and experience
- ⚡ **Performance**: Optimize database queries and rendering

## 🙋♂️ Contact

**Gouransh Soni** - *Full Stack Developer & Data Enthusiast*

- 📧 **Email**: [gouransh1024@gmail.com](mail to:gouransh1024@gmail.com)
- 📱 **Phone**: [+91 9509682181](tel:+919509682181)
- 💼 **LinkedIn**: [Gouransh SOni](https://www.linkedin.com/in/gouransh-soni-3556192b1)
- 🔗 **GitHub**: [gouransh1024](https://github.com/gouransh1024)
- 🌐 **Live App**: [Student Performance Tracker](https://student-performance-tracker.streamlit.app/)

## 🙏 Acknowledgments

- **[Streamlit Team](https://streamlit.io/)** for the amazing framework
- **[SQLite](https://www.sqlite.org/)** for the reliable database engine
- **[Pandas](https://pandas.pydata.org/)** for powerful data manipulation
- **[Plotly](https://plotly.com/)** for interactive visualizations
- **Open Source Community** for inspiration and support

## 📥 Bulk Data Import Feature

The application now includes a comprehensive bulk data import system that allows you to import large amounts of data from Excel and CSV files.

### **Supported Import Types**
- **Students**: Import student information (name, class, section, date of birth)
- **Subjects**: Import subject names for the curriculum
- **Marks**: Import student marks with assessment details

### **Key Features**
- ✅ **File Format Support**: CSV and Excel (.xlsx, .xls) files
- ✅ **Data Validation**: Comprehensive validation with detailed error reporting
- ✅ **Sample Templates**: Download sample files for easy data preparation
- ✅ **Batch Processing**: Handle large datasets efficiently
- ✅ **Import Statistics**: Track success rates and error details
- ✅ **Error Handling**: Detailed error messages for troubleshooting

### **Quick Start**
1. Navigate to "Bulk Data Import" page
2. Choose the data type (Students, Subjects, or Marks)
3. Download sample files as templates
4. Prepare your data following the format requirements
5. Upload and validate your file
6. Import the data and review results

For detailed instructions, see the [Bulk Import Guide](BULK_IMPORT_GUIDE.md).

## 🔮 Future Roadmap

### **Phase 1 - Enhanced Analytics**
- [ ] Advanced statistical analysis and predictive modeling
- [ ] Comparative benchmarking across institutions
- [ ] Performance trend forecasting

### **Phase 2 - Extended Features**
- [ ] PDF report generation with custom templates
- [ ] Email notification system for parents/teachers
- [ ] Multi-language support for international use
- [ ] Advanced user roles and permissions system

### **Phase 3 - Integration & APIs**
- [ ] REST API development for third-party integrations
- [ ] Mobile application development
- [ ] Cloud storage integration
- [ ] Real-time collaboration features

## ⭐ Show Your Support

If you find this project helpful, please consider:

- ⭐ **Starring** the repository
- 🐛 **Reporting** issues and bugs
- 💡 **Suggesting** new features
- 🤝 **Contributing** to the codebase
- 📢 **Sharing** with others

---

<div align="center">

**Built with ❤️ by [Gouransh Soni](https://github.com/gouransh1024)**

*Empowering education through data-driven insights* 📚✨

</div>

