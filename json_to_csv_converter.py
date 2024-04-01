import json
import csv


def convert(json_filename):
    with open(f"{json_filename}.json") as json_file:
        data = json.load(json_file)

    csv_file = open(f"{json_filename}.csv", "w", encoding="utf-8")
    csv_writer = csv.writer(csv_file)

    counter = 0
    for team in data:
        if counter == 0:
            top_row = filter(data[team].keys())
            top_row.insert(0, "team")
            print(top_row)
            csv_writer.writerow(top_row)
            counter += 1
        row = [i for i in data[team].values()]
        row.insert(0, team)
        csv_writer.writerow(row)
        print(row)
    csv_file.close()


def filter(props):
    copy = [i for i in props]
    for i in range(0, len(copy)):
        copy[i] = copy[i][copy[i].index(" "):].strip()
    return copy
