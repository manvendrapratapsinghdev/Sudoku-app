# Sudoku Streamlit App

This project is a simple Streamlit application that displays a Sudoku puzzle. It utilizes existing Sudoku logic to generate and present the puzzle in a user-friendly format.

## Project Structure

```
sudoku-streamlit-app
├── src
│   ├── app.py          # Main entry point for the Streamlit application
│   └── sudo.py         # Contains Sudoku logic and functions
├── requirements.txt     # Lists project dependencies
└── README.md            # Project documentation
```

## Setup Instructions

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd sudoku-streamlit-app
   ```

2. **Create a virtual environment** (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required dependencies**:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the Streamlit application, execute the following command in your terminal:

```
streamlit run src/app.py
```

This will start the Streamlit server and open the Sudoku puzzle UI in your default web browser.

## Contributing

Feel free to submit issues or pull requests if you have suggestions or improvements for the project.