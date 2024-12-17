from flask import Flask, render_template, request, redirect, url_for # type: ignore
from random_num import generate_unique_number
import random
import os

app = Flask(__name__)

# Path to the exclusion file
EXCLUDE_FILE = 'excluded_numbers.txt'

def generate_unique_number(range_start, range_end, exclude_file):
    """Generates a random number within the specified range, excluding numbers in the given file."""
    # Convert inputs to integers to ensure proper type
    range_start = int(range_start)
    range_end = int(range_end)

    
    # Read excluded numbers
    excluded_numbers = set()
    if os.path.exists(exclude_file):
        with open(exclude_file, 'r') as f:
            excluded_numbers = {int(line.strip()) for line in f}
    
    # Find a unique number
    available_numbers = set(range(range_start, range_end + 1)) - excluded_numbers
    
    if not available_numbers:
        raise ValueError("No unique numbers available in the specified range")
    
    # Choose a random number from available numbers
    unique_number = random.choice(list(available_numbers))
    
    # Write the number to exclude file
    with open(exclude_file, 'a') as f:
        f.write(str(unique_number) + '\n')
    
    return unique_number

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    unique_number = None
    error_message = None

    if request.method == 'POST':
        try:
            # Ensure form inputs are integers
            range_start = int(request.form['range_start'])
            range_end = int(request.form['range_end'])

            # Validate range
            if range_start >= range_end:
                error_message = "Range start must be less than range end"
            else:
       
                # Generate unique number
                unique_number = generate_unique_number(range_start, range_end, EXCLUDE_FILE)
        
        except ValueError as e:
            error_message = str(e)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"

    return render_template('index.html', 
                           unique_number=unique_number, 
                           error_message=error_message)

if __name__ == '__main__':
    print('\nunigue_number')