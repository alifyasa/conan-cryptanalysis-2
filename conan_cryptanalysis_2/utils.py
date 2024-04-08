def print_header(title, total_length=60, char="="):
    total_side_length = total_length - len(title) - 2  # Total length for both sides
    left_side_length = total_side_length // 2
    right_side_length = total_side_length - left_side_length  # Adjusts if odd
    print(char * left_side_length, title, char * right_side_length)