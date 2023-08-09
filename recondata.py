import json

def create_table(num_columns):
    table = []
    column_names = []

    for i in range(num_columns):
        col_name = input(f"Enter name for column {i + 1}: ")
        column_names.append(col_name)

    counter = 103
    while True:
        row = {'ID': counter}  # First column auto-increment
        counter += 1

        for col_name in column_names[1:]:  # Skip the first column (auto-increment)
            value = input(f"Enter value for {col_name}: ")
            row[col_name] = value

        table.append(row)
        continue_input = input("Add another row? (yes/no): ").lower()
        if continue_input != 'yes':
            break

    return table

def main():
    num_columns = int(input("Enter the number of columns (including auto-increment column): "))
    table_data = create_table(num_columns)

    output_filename = "output.json"
    with open(output_filename, 'w') as output_file:
        json.dump(table_data, output_file, indent=4)
        print(f"Data saved to {output_filename}")

if __name__ == "__main__":
    main()
