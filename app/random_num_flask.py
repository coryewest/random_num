from flask import Flask, render_template, request, redirect, url_for # type: ignore
from random_num import generate_unique_number, get_exclude_file_path
import os

app = Flask(__name__)

# Path to the exclusion file
EXCLUDE_FILE = os.getenv('EXCLUDE_FILE') or os.getenv('EXCLUDE_PATH') or '/tmp/excluded_numbers.txt'
EXCLUDE_PATH = get_exclude_file_path(EXCLUDE_FILE)

# Fixed range for generated numbers
RANGE_START = 1000
RANGE_END = 9999
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    unique_number = None
    error_message = None

    if request.method == 'POST':
        try:
            # Generate unique number using fixed range
            unique_number = generate_unique_number(RANGE_START, RANGE_END, EXCLUDE_PATH)
            with open(EXCLUDE_PATH, 'a') as f:
                f.write(str(unique_number) + '\n')
        
        except ValueError as e:
            error_message = str(e)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"

    return render_template('index.html', 
                           unique_number=unique_number, 
                           error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)