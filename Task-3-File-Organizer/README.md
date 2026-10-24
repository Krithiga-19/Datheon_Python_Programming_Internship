# Task 3 – Automated File Organizer & Cleanup Utility

## Description
A Python utility that organizes files into separate folders based on their file extensions.

## Features
- Scans files in a selected folder
- Identifies file extensions
- Creates category folders automatically
- Moves files into the appropriate folders
- Handles duplicate filenames
- Handles permission errors
- Displays an execution summary
- Supports preview mode before moving files

## Categories
- Documents
- Images
- Videos
- Archives
- Code
- Others

## Technologies Used
- Python 3
- pathlib
- shutil
- File handling and exception handling

## How to Run
1. Install Python 3.
2. Open a terminal in this folder.
3. Run:

```bash
python organizer.py
```

4. Choose preview mode to check the proposed organization.
5. Choose move mode only after reviewing the preview.

## Safety Note
Always review the preview before moving files. Test the utility with sample files before organizing important folders.
