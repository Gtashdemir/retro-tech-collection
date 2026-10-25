# Retro Tech Collection

A Python and SQLite command-line application for managing a collection of retro technology items.

## About the Project

This application was created to provide a simple way to store and manage information about retro technology items.

The collection supports four item types:

- Computer
- Camera
- Phone
- Video Player

Data is stored locally using an SQLite database.

## Features

The application allows users to:

- Add a new item to the collection
- View items by type
- Search for items by name
- Browse large collections using pagination
- Update existing items
- Delete items from the collection
- Validate user input, including dates
- Automatically record when an item is added

## Technologies Used

- Python
- SQLite
- SQL
- Git
- GitHub

## Project Structure

- `app.py` - Main command-line application and user interaction
- `database.py` - Database connection and database operations
- `add-test-data.py` - Adds test data for testing the application
- `collection.db` - SQLite database
- `.gitignore` - Files and folders excluded from Git

## Running the Application

Make sure Python is installed on your computer.

Run the application from the project directory:

```bash
python app.py