import csv


class FileHandler:
    def __init__(self, path_input, path_output, start_line=1, count_line=None, column_url=0):
        self.path_input = path_input
        self.path_output = path_output
        self.start_line = start_line - 1
        self.count_line = count_line
        self.end_line = self.start_line + count_line if count_line is not None else None
        self.column_url = column_url
        self.lines = self.read()

    def read(self):
        file_extension = self.path_input.split('.')[-1].lower()
        if file_extension == 'csv':
            list_url = self.read_from_csv()
        elif file_extension == 'txt':
            list_url = self.read_from_txt()
        else:
            raise ValueError("Unsupported file format. Please use a .csv or .txt file.")
        return list_url

    def read_from_txt(self):
        with open(self.path_input, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            end_line = self.end_line if len(lines) is None else self.end_line
            return [line.strip() for line in lines[self.start_line:end_line] if line.strip()]

    def read_from_csv(self):
        with open(self.path_input, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # skip header
            end_line = self.end_line if reader.line_num is None else self.end_line
            return [row[self.column_url] for row in reader][self.start_line:end_line]

    def writer(self, data):
        with open(self.path_output, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(data)

    def writer_header_to_csv(self, header=None):
        self.writer(header)
