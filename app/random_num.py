#!/usr/bin/env python3

import os
import random


def get_exclude_file_path(exclude_file=None):
  if exclude_file:
    return exclude_file
  return os.getenv('EXCLUDE_FILE') or os.getenv('EXCLUDE_PATH') or '/tmp/excluded_numbers.txt'


def generate_unique_number(range_start, range_end, exclude_file):
  """Generates a random number within the specified range, excluding numbers in the given file.

  Args:
    range_start: The lower bound of the random number range.
    range_end: The upper bound of the random number range.
    exclude_file: The path to the file containing numbers to exclude.

  Returns:
    A randomly generated number that is not in the exclude file.
  """

  exclude_file = get_exclude_file_path(exclude_file)
  excluded_numbers = set()
  parent_dir = os.path.dirname(exclude_file)
  if parent_dir:
    os.makedirs(parent_dir, exist_ok=True)

  if os.path.exists(exclude_file):
    with open(exclude_file, 'r', encoding='utf-8') as f:
      for line in f:
        line = line.strip()
        if line:
          excluded_numbers.add(int(line))

  while True:
    number = random.randint(range_start, range_end)
    if number not in excluded_numbers:
      return number


if __name__ == '__main__':
  # Example usage when run as a script
  range_start = 1000
  range_end = 9999
  exclude_file = get_exclude_file_path()

  unique_number = generate_unique_number(range_start, range_end, exclude_file)
  print(unique_number)

  # Append the generated number to the exclude file
  with open(exclude_file, 'a', encoding='utf-8') as f:
    f.write(str(unique_number) + '\n')
