# Task 4 – Rule-Based Interactive Terminal Assistant / Chatbot

## Description
A rule-based conversational chatbot built with Python. It recognizes user intents and answers frequently asked questions using keyword matching, regular expressions, and a JSON dataset.

## Features
- Recognizes greetings such as hello and hi
- Answers business-hours questions
- Provides internship project submission instructions
- Answers certificate-related questions
- Supports multiple intents in one message
- Uses fallback responses for unknown questions
- Handles exit commands such as bye, exit, and quit
- Loads FAQ data from a JSON file
- Handles missing or invalid JSON files

## Technologies Used
- Python 3
- JSON
- Regular expressions (`re`)
- File handling (`pathlib`)
- Exception handling

## Project Files
- `chatbot.py` – Main chatbot program
- `sample_faq.json` – FAQ questions and answers

## How to Run
1. Install Python 3.
2. Keep both project files in the same folder.
3. Open a terminal in that folder.
4. Run:

```bash
python chatbot.py
```

## Example Questions
- Hi
- What are your working hours?
- How do I submit my internship project?
- When will I receive my certificate?
- What can you do?
- Bye

## Expected FAQ Information
- Working hours: Monday to Friday, 9:00 AM to 6:00 PM IST
- Project submission: Submit a public GitHub repository link through the Student Workspace
- Certificate: Reviewed and issued within 3–5 business days after code review

## Author
M.Tech Computer Science and Engineering Student
