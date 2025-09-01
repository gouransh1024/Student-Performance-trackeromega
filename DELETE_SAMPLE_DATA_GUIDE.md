# Delete Sample Data Feature Guide

## Overview
The Student Performance Tracker now includes a comprehensive feature to delete sample data and manage your database content. This feature allows you to:

- **Delete Sample Data**: Remove all existing data (students, subjects, and marks)
- **Reset to Sample Data**: Clear existing data and restore fresh sample data
- **Data Management**: Access data management tools from multiple locations

## How to Access

### 1. From Main Dashboard
- Navigate to the main dashboard
- Look for the "📊 Data Management" section
- Click "🗑️ Quick Delete Data" button
- Confirm deletion when prompted

### 2. From Settings Page
- Click the "⚙️ Settings" button in the sidebar
- Select "Database Management" category
- Scroll to "Sample Data Management" section
- Use either "Delete Sample Data" or "Reset to Sample Data" options

### 3. From Sidebar Navigation
- Click "⚙️ Settings" in the sidebar
- This takes you directly to the Settings page

## Features Available

### Delete All Data
- **Purpose**: Remove all students, subjects, and marks from the database
- **Use Case**: When you want to start fresh with a clean database
- **Safety**: Requires confirmation checkbox to prevent accidental deletion

### Reset to Sample Data
- **Purpose**: Clear existing data and restore the original sample dataset
- **Use Case**: When you want to return to the default sample data
- **Sample Data Includes**:
  - 10 sample students across different classes
  - 8 core subjects (Mathematics, Physics, Chemistry, Biology, English, History, Geography, Computer Science)
  - Sample marks and assessments for each student

### Data Summary
- **Purpose**: View comprehensive statistics about your current data
- **Information Displayed**:
  - Total counts (students, subjects, assessments)
  - Average performance percentage
  - Grade distribution breakdown
  - Sample data detection indicator

## Safety Features

### Confirmation Required
- All deletion operations require explicit confirmation
- Checkbox must be checked before deletion proceeds
- Clear warning messages about data loss

### Foreign Key Constraints
- Data is deleted in the correct order to maintain database integrity
- Marks are deleted first, then students, then subjects
- Prevents database corruption

### Error Handling
- Comprehensive error messages if operations fail
- Database state is preserved if errors occur
- User feedback for all operations

## Sample Data Details

The sample data includes:

**Students (10 total):**
- Class 10A: Aarav Sharma, Priya Patel
- Class 10B: Rohit Kumar, Sneha Singh  
- Class 11A: Vikram Rao, Anita Desai
- Class 11B: Kiran Reddy
- Class 12A: Meera Joshi, Arjun Nair
- Class 12B: Deepika Gupta

**Subjects (8 total):**
- Mathematics, Physics, Chemistry, Biology
- English, History, Geography, Computer Science

**Assessments:**
- 5 subjects per student with random marks (45-95)
- Various assessment types: Quiz, Assignment, Midterm, Final
- Recent assessment dates

## Best Practices

### Before Deleting Data
1. **Export Important Data**: Use the export features in Settings to backup any custom data
2. **Verify Intent**: Ensure you really want to delete all data
3. **Check Dependencies**: Make sure no other users depend on this data

### After Deleting Data
1. **Verify Deletion**: Check that all data has been removed
2. **Add New Data**: Use the management pages to add new students, subjects, and marks
3. **Test Functionality**: Ensure the application works correctly with the new data

### Regular Maintenance
1. **Monitor Database Size**: Check database size in the sidebar
2. **Review Data Quality**: Regularly review and clean up data
3. **Backup Important Data**: Export data periodically for safekeeping

## Troubleshooting

### Common Issues

**"Failed to delete data" error:**
- Check database connection
- Ensure no other operations are running
- Try refreshing the page and retrying

**"Database locked" error:**
- Close any other applications using the database
- Wait a few moments and retry
- Restart the application if necessary

**Partial deletion:**
- Check error messages for specific issues
- Use the "Reset to Sample Data" option as a fallback
- Contact support if problems persist

### Recovery Options

If you accidentally delete data:
1. **Check if it's sample data**: Use "Reset to Sample Data" to restore
2. **Check exports**: Look for any exported CSV files
3. **Database backup**: Check if you have a backup of the database file

## Technical Details

### Database Operations
- Uses SQLite DELETE statements
- Maintains referential integrity
- Transaction-based operations for safety

### File Locations
- Main application: `app.py`
- Settings page: `pages/7_Settings.py`
- Utility functions: `utils/data_management.py`
- Database connection: `db/connection.py`

### Dependencies
- Streamlit for the web interface
- SQLite for database operations
- Pandas for data manipulation
- Custom utility functions for data management

## Support

If you encounter issues with the delete sample data feature:

1. **Check the error messages** displayed in the application
2. **Review the console output** for technical details
3. **Verify database permissions** and file access
4. **Contact the development team** with specific error details

---

**Note**: This feature is designed for development, testing, and data management purposes. Always ensure you have backups of important data before performing deletion operations.
