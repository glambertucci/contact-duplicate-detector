# Contact Duplicate Detector

**Contact Duplicate Detector** is a Python application that detects potential duplicate contacts in a dataset by comparing multiple attributes such as name, email, and address. It classifies matches into **"High"** or **"Low"** accuracy based on similarity scores.

## Features

- **Custom Scoring Logic**: Weighs email, name, and address similarity.
- **High & Low Match Detection**: Identifies highly likely duplicates.
- **Performance Optimization**: Uses clustering and caching for faster execution.
- **CSV Input & Output**: Supports reading contacts from a CSV and writing matches to a results file.
- **Test Suite**: Includes tests to ensure correctness of duplicate detection logic.

## Usage

1. Clone the repository:
   ```bash
   git clone git@github.com:glambertucci/contact-duplicate-detector.git
   cd contact-duplicate-detector
    python main.py
