import itertools
import string
import subprocess
import csv


def generate_permutations(max_length):
    charts = string.ascii_lowercase + string.digits
    for length in range(1, max_length + 1):
        for combination in itertools.product(charts, repeat=length):
            yield ''.join(combination) + '.pl'


def calculate_number_of_permutations(max_length, number_of_characters):
    return sum(number_of_characters ** i for i in range(1, max_length + 1))


def ping_i_save(address, file_path):
    try:
        result = subprocess.run(["ping", "-c", "1", address], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if result.returncode == 0:
            with open(file_path, "a") as file:
                file.write(address + "\n")
    except Exception as e:
        print(f"Błąd: {e}")


filepath = "/home/albert/Dokumenty/domains.txt"
main_max_length = 4
characters = string.ascii_lowercase + string.digits

number_possibilities = calculate_number_of_permutations(main_max_length, len(characters))
number_processed = 0

with open(filepath, mode='w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Domain'])
    for permutation in generate_permutations(main_max_length):
        ping_i_save(permutation, filepath)
        number_processed += 1
        percent = (number_processed / number_possibilities) * 100
        print(f"Sprawdzono: {permutation} ({percent:.2f}%)")
