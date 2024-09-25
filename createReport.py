import csv

def create_report(references, filename):
    with open(filename, mode='w', newline='') as csv_file:
        fieldnames = ['Referencia', 'Linea', 'Columna']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for ref in references:
            writer.writerow(ref)