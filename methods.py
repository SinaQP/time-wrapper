import re



def is_valid_date_format(input_string):
    # Define a regular expression pattern for "YYYY-MM-DD" format
    pattern = r'^\d{4}-\d{2}-\d{2}$'

    # Use the re.match() function to check if the input string matches the pattern
    if re.match(pattern, input_string):
        return True
    else:
        return False
