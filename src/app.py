import streamlit as st
from streamlit.components.v1 import html
from sudo import regenerate_sudoku, print_sudoku, get_assignment

# Streamlit UI
st.title("🧩 Sudoku Puzzle Generator")

# Add a button to regenerate the Sudoku puzzle
if st.button("Regenerate Sudoku"):
    regenerate_sudoku()

# Display the Sudoku puzzle
st.text(print_sudoku(get_assignment()))