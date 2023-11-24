import csv


def read_data_from_excel(file_name, sheet):
    data_list = []
    wb = load_workbook(filename=file_name)
    sh = wb[sheet]
    rows = sh.max_row
    cols = sh.max_column

    for i in range(2, rows + 1):
        row = []
        for j in range(1, cols + 1):
            row.append(sh.cell(row=i, column=j).value)
        data_list.append(row)

    print(data_list, rows, cols)
    return data_list


def read_csv(file_name):
    with open(file_name) as csvfile:
        csv_reader = csv.reader(csvfile)
        headers = ','.join(next(csv_reader))
        rows = []
        for row in csv_reader:
            rows.append(row)

        return headers, rows


if __name__ == '__main__':
    import os
    from autofw.utilities.logger import logger
    test_data = os.path.join(logger.path.parent.parent, 'test_data/login.csv')
    print(read_csv(test_data))
