# File: /sudoku-streamlit-app/sudoku-streamlit-app/src/sudo.py

from itertools import product
import io
import random
from PIL import Image, ImageDraw, ImageFont
import streamlit as st
import time

rows = '123456789'
cols = '123456789'

def cross(a, b):
    return [x + y for x, y in product(a, b)]

cells = cross(rows, cols)

grid_str = (
    "53..7...."
    "6..195..."
    ".98....6."
    "8...6...3"
    "4..8.3..1"
    "7...2...6"
    ".6....28."
    "...419..5"
    "....8..79"
)

domains = {}
for cell, val in zip(cells, grid_str):
    if val in '123456789':
        domains[cell] = [int(val)]
    else:
        domains[cell] = list(range(1, 10))

unit_list = []

for r in rows:
    unit_list.append(cross(r, cols))

for c in cols:
    unit_list.append(cross(rows, c))

box_rows = ('123', '456', '789')
box_cols = ('123', '456', '789')
for rs in box_rows:
    for cs in box_cols:
        unit_list.append(cross(rs, cs))

units = {cell: [unit for unit in unit_list if cell in unit] for cell in cells}
peers = {cell: set(sum(units[cell], [])) - {cell} for cell in cells}

def is_consistent(cell, value, assignment):
    for peer in peers[cell]:
        if peer in assignment and assignment[peer] == value:
            return False
    return True

assignment = {cell: domains[cell][0] for cell in cells if len(domains[cell]) == 1}

def get_assignment():
    return assignment

def get_domains():
    return domains

def get_cells():
    return cells

def get_peers():
    return peers

def print_sudoku(assignments):
    # Generate HTML for the Sudoku grid
    grid_html = '<table style="border-collapse: collapse; margin: auto;">'
    for i in range(9):
        grid_html += '<tr>'
        for j in range(9):
            cell = rows[i] + cols[j]
            val = assignments.get(cell, 0)
            border_style = "border: 1px solid black;"

            # Add thicker borders for 3x3 subgrids
            if j % 3 == 0:
                border_style += " border-left: 2px solid black;"
            if i % 3 == 0:
                border_style += " border-top: 2px solid black;"
            if j == 8:
                border_style += " border-right: 2px solid black;"
            if i == 8:
                border_style += " border-bottom: 2px solid black;"

            grid_html += f'<td style="{border_style} width: 40px; height: 40px; text-align: center; font-size: 20px;">'
            grid_html += str(val) if val != 0 else "&nbsp;"
            grid_html += '</td>'
        grid_html += '</tr>'
    grid_html += '</table>'

    # Render the grid in Streamlit
    st.markdown(grid_html, unsafe_allow_html=True)

def print_solved_sudoku(board):
    # Generate HTML for the solved Sudoku grid
    grid_html = '<table style="border-collapse: collapse; margin: auto;">'
    for i in range(9):
        grid_html += '<tr>'
        for j in range(9):
            val = board[i][j]
            border_style = "border: 1px solid black;"

            # Add thicker borders for 3x3 subgrids
            if j % 3 == 0:
                border_style += " border-left: 2px solid black;"
            if i % 3 == 0:
                border_style += " border-top: 2px solid black;"
            if j == 8:
                border_style += " border-right: 2px solid black;"
            if i == 8:
                border_style += " border-bottom: 2px solid black;"

            grid_html += f'<td style="{border_style} width: 40px; height: 40px; text-align: center; font-size: 20px;">'
            grid_html += str(val) if val != 0 else "&nbsp;"
            grid_html += '</td>'
        grid_html += '</tr>'
    grid_html += '</table>'

    # Render the grid in Streamlit
    st.markdown(grid_html, unsafe_allow_html=True)

def regenerate_sudoku():
    global grid_str, domains, assignment

    def is_valid(board, row, col, num):
        # Check row
        for x in range(9):
            if board[row][x] == num:
                return False

        # Check column
        for x in range(9):
            if board[x][col] == num:
                return False

        # Check 3x3 box
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if board[start_row + i][start_col + j] == num:
                    return False

        return True

    def fill_board(board):
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    random.shuffle(numbers)
                    for num in numbers:
                        if is_valid(board, row, col, num):
                            board[row][col] = num
                            if fill_board(board):
                                return True
                            board[row][col] = 0
                    return False
        return True

    # Initialize an empty board
    board = [[0 for _ in range(9)] for _ in range(9)]
    numbers = list(range(1, 10))

    # Fill the board with a valid Sudoku solution
    fill_board(board)

    # Remove some numbers to create a puzzle
    for _ in range(random.randint(20, 30)):
        row, col = random.randint(0, 8), random.randint(0, 8)
        board[row][col] = 0

    # Convert the board to a string format
    grid_str = ''.join(str(cell) if cell != 0 else '.' for row in board for cell in row)

    # Update domains and assignment
    domains = {}
    for cell, val in zip(cells, grid_str):
        if val in '123456789':
            domains[cell] = [int(val)]
        else:
            domains[cell] = list(range(1, 10))
    assignment = {cell: domains[cell][0] for cell in cells if len(domains[cell]) == 1}

def download_sudoku_as_image(assignments):
    # Create an image for the Sudoku grid
    img_size = 360  # 40px per cell * 9 cells
    cell_size = 40
    img = Image.new('RGB', (img_size, img_size), color='white')
    draw = ImageDraw.Draw(img)

    # Load a default font
    try:
        font = ImageFont.load_default()
    except Exception as e:
        st.error("Failed to load font: " + str(e))

    # Draw grid lines
    for i in range(10):
        line_width = 3 if i % 3 == 0 else 1
        draw.line([(i * cell_size, 0), (i * cell_size, img_size)], fill='black', width=line_width)
        draw.line([(0, i * cell_size), (img_size, i * cell_size)], fill='black', width=line_width)

    # Draw numbers
    for i in range(9):
        for j in range(9):
            cell = rows[i] + cols[j]
            val = assignments.get(cell, 0)
            if val != 0:
                text_bbox = draw.textbbox((0, 0), str(val), font=font)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]
                text_x = j * cell_size + (cell_size - text_width) / 2
                text_y = i * cell_size + (cell_size - text_height) / 2
                draw.text((text_x, text_y), str(val), fill='black', font=font)

    # Save the image to a BytesIO object
    img_buffer = io.BytesIO()
    img.save(img_buffer, format='PNG')
    img_buffer.seek(0)

    st.download_button(
        label="\U0001F4BE",  # Adding a floppy disk emoji for the download icon
        data=img_buffer,
        file_name="sudoku.png",
        mime="image/png",
        key="download_button"
    )

assignment_count = 0  # Global counter for assignments

def increment_assignment_count():
    global assignment_count
    assignment_count += 1

def backtracking_search():
    global assignment_count
    assignment_count = 0  # Reset counter

    def is_valid(board, row, col, num):
        for x in range(9):
            if board[row][x] == num or board[x][col] == num:
                return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if board[start_row + i][start_col + j] == num:
                    return False
        return True

    def solve(board):
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    for num in range(1, 10):
                        if is_valid(board, row, col, num):
                            board[row][col] = num
                            increment_assignment_count()  # Increment assignment count
                            if solve(board):
                                return True
                            board[row][col] = 0
                    return False
        return True

    board = [[int(grid_str[i * 9 + j]) if grid_str[i * 9 + j] != '.' else 0 for j in range(9)] for i in range(9)]
    solve(board)
    return board

def forward_checking():
    global assignment_count
    assignment_count = 0  # Reset counter

    def is_valid(board, row, col, num):
        for x in range(9):
            if board[row][x] == num or board[x][col] == num:
                return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if board[start_row + i][start_col + j] == num:
                    return False
        return True

    def forward_check(board):
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    domain = [num for num in range(1, 10) if is_valid(board, row, col, num)]
                    if not domain:
                        return False
                    for num in domain:
                        board[row][col] = num
                        increment_assignment_count()  # Increment assignment count
                        if forward_check(board):
                            return True
                        board[row][col] = 0
                    return False
        return True

    board = [[int(grid_str[i * 9 + j]) if grid_str[i * 9 + j] != '.' else 0 for j in range(9)] for i in range(9)]
    forward_check(board)
    return board

def arc_consistency_ac3():
    def revise(domains, xi, xj):
        revised = False
        for x in domains[xi]:
            if not any(x != y for y in domains[xj]):
                domains[xi].remove(x)
                revised = True
        return revised

    def ac3(domains, arcs):
        while arcs:
            xi, xj = arcs.pop(0)
            if revise(domains, xi, xj):
                if not domains[xi]:
                    return False
                for xk in peers[xi]:
                    if xk != xj:
                        arcs.append((xk, xi))
        return True

    # Initialize domains and arcs
    domains = {cell: list(range(1, 10)) if grid_str[i] == '.' else [int(grid_str[i])] for i, cell in enumerate(cells)}
    arcs = [(xi, xj) for xi in cells for xj in peers[xi]]

    if ac3(domains, arcs):
        return [[domains[rows[i] + cols[j]][0] if len(domains[rows[i] + cols[j]]) == 1 else 0 for j in range(9)] for i in range(9)]
    else:
        return None

def backtracking_search_with_heuristics(heuristic):
    def is_valid(board, row, col, num):
        for x in range(9):
            if board[row][x] == num or board[x][col] == num:
                return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if board[start_row + i][start_col + j] == num:
                    return False
        return True

    def select_variable_mrv(board):
        min_options = 10
        best_cell = None
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    options = [num for num in range(1, 10) if is_valid(board, row, col, num)]
                    if len(options) < min_options:
                        min_options = len(options)
                        best_cell = (row, col)
        return best_cell

    def select_variable_degree(board):
        max_degree = -1
        best_cell = None
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    degree = sum(1 for num in range(1, 10) if is_valid(board, row, col, num))
                    if degree > max_degree:
                        max_degree = degree
                        best_cell = (row, col)
        return best_cell

    def order_values_lcv(board, row, col):
        def count_constraints(value):
            constraints = 0
            for x in range(9):
                if board[row][x] == 0 and is_valid(board, row, x, value):
                    constraints += 1
                if board[x][col] == 0 and is_valid(board, x, col, value):
                    constraints += 1
            start_row, start_col = 3 * (row // 3), 3 * (col // 3)
            for i in range(3):
                for j in range(3):
                    if board[start_row + i][start_col + j] == 0 and is_valid(board, start_row + i, start_col + j, value):
                        constraints += 1
            return constraints

        values = [num for num in range(1, 10) if is_valid(board, row, col, num)]
        return sorted(values, key=count_constraints)

    def solve(board):
        empty_cell = select_variable_mrv(board)
        if not empty_cell:
            return True

        row, col = empty_cell
        values = order_values_lcv(board, row, col)

        for num in values:
            if is_valid(board, row, col, num):
                board[row][col] = num
                if solve(board):
                    return True
                board[row][col] = 0
        return False

    board = [[int(grid_str[i * 9 + j]) if grid_str[i * 9 + j] != '.' else 0 for j in range(9)] for i in range(9)]
    solve(board)
    return board

def heuristics():
    def is_valid(board, row, col, num):
        for x in range(9):
            if board[row][x] == num or board[x][col] == num:
                return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if board[start_row + i][start_col + j] == num:
                    return False
        return True

    def find_empty_with_heuristics(board):
        min_options = 10
        best_cell = None
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    options = [num for num in range(1, 10) if is_valid(board, row, col, num)]
                    if len(options) < min_options:
                        min_options = len(options)
                        best_cell = (row, col)
        return best_cell

    def solve_with_heuristics(board):
        empty_cell = find_empty_with_heuristics(board)
        if not empty_cell:
            return True

        row, col = empty_cell
        for num in range(1, 10):
            if is_valid(board, row, col, num):
                board[row][col] = num
                if solve_with_heuristics(board):
                    return True
                board[row][col] = 0
        return False

    board = [[int(grid_str[i * 9 + j]) if grid_str[i * 9 + j] != '.' else 0 for j in range(9)] for i in range(9)]
    solve_with_heuristics(board)
    return board

# Update the main function to include solving and displaying the solved Sudoku
def main():
    st.title("Sudoku App")
    st.write("This is a Sudoku solver app. You can generate a new Sudoku puzzle, solve it, and download the solved puzzle as an image.")
    

    col1, col2 = st.columns([3, 1], gap="small")
    with col1:
        if st.button("Regenerate"):
            regenerate_sudoku()  # Print the unsolved Sudoku
    with col2:
        download_sudoku_as_image(assignment)
    print_sudoku(assignment)    
    st.sidebar.title("Sudoku Solver Options")
    algo = st.sidebar.selectbox(
        "Choose the solving algorithm:",
        ["Backtracking Search", "Forward Checking (Constraint Propagation)", "Arc Consistency (AC-3)", "Heuristics"]
    )

    # Move the solve button logic to the sidebar
    if st.sidebar.button("Solve"):
        performance_metrics = []

        # Run all algorithms and collect performance metrics
        for method_name, method_function in [
            ("Backtracking Search", backtracking_search),
            ("Forward Checking", forward_checking),
            ("Arc Consistency (AC-3)", arc_consistency_ac3),
            ("Heuristics", heuristics)
        ]:
            global assignment_count
            assignment_count = 0  # Reset assignment count before each method

            start_time = time.time()
            solved_board = method_function()
            elapsed_time = time.time() - start_time

            # Collect metrics
            assignments = assignment_count  # Use the global assignment count
            backtracks = random.randint(0, 100)  # Placeholder
            nodes_explored = random.randint(0, 1000)  # Placeholder

            performance_metrics.append({
                "Method": method_name,
                "Time (s)": elapsed_time,
                "Assignments": assignments,
                "Backtracks": backtracks,
                "Nodes Explored": nodes_explored
            })

        # Display performance metrics in a table
        st.sidebar.write("### Performance Metrics")
        st.sidebar.table(performance_metrics)

        # Solve based on the selected algorithm
        start_time = time.time()
        if algo == "Backtracking Search":
            solved_board = backtracking_search()
        elif algo == "Forward Checking (Constraint Propagation)":
            solved_board = forward_checking()
        elif algo == "Arc Consistency (AC-3)":
            solved_board = arc_consistency_ac3()
        elif algo == "Heuristics":
            solved_board = heuristics()

        elapsed_time = time.time() - start_time
        # Move the "Solved Sudoku" title to the right side
        st.write("### Solved Sudoku")
        print_solved_sudoku(solved_board)  # Print the solved Sudoku
        

if __name__ == "__main__":
    main()