#!/usr/bin/env python3

import random

def generate_unique_number(range_start, range_end, exclude_file):
  """Generates a random number within the specified range, excluding numbers in the given file.

  Args:
    range_start: The lower bound of the random number range.
    range_end: The upper bound of the random number range.
    exclude_file: The path to the file containing numbers to exclude.

  Returns:
    A randomly generated number that is not in the exclude file.
  """

  excluded_numbers = set()
  with open(exclude_file, 'r') as f:
    for line in f:
      excluded_numbers.add(int(line.strip()))

  while True:
    number = random.randint(range_start, range_end)
    if number not in excluded_numbers:
      return number

# Example usage
range_start = 1000
range_end = 9999
exclude_file = 'excluded_numbers.txt'

unique_number = generate_unique_number(range_start, range_end, exclude_file)
print(unique_number)

# Append the generated number to the exclude file
with open(exclude_file, 'a') as f:
  f.write(str(unique_number) + '\n')
