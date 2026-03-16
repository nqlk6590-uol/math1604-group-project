import os
import csv
import requests
from io import StringIO
from datetime import datetime


def import_data(url):
    response = requests.get(url)
    os.makedirs("data", exist_ok=True)
    file_path = os.path.join("data", "dataset_M3.txt")
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(response.text)
    with open(file_path, "r", encoding="utf-8") as file:
        data_text_list = file.readlines()
    return data_text_list

def clean_data(data_text_list):
    data_string = "".join(data_text_list)
    csv_reader = csv.reader(StringIO(data_string))
    rows = list(csv_reader)
    header = rows[0]
    time_index = header.index("time")
    cleaned_rows = [header]
    for row in rows[1:]:
        original_time = row[time_index].strip()
        cleaned_time = datetime.strptime(
            original_time, "%Y-%m-%dT%H:%M:%S.%fZ"
        ).strftime("%d-%m-%Y %H:%M:%S")

        row[time_index] = cleaned_time
        cleaned_rows.append(row)

    os.makedirs("output", exist_ok=True)
    output_path = os.path.join("output", "cleaned_data_M3.txt")

    with open(output_path, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(cleaned_rows)

    cleaned_text_list = []
    for row in cleaned_rows:
        cleaned_text_list.append(",".join(row) + "\n")

    return cleaned_text_list


url = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv&starttime=2023-01-01&endtime=2023-01-02"

raw_data = import_data(url)
cleaned_data = clean_data(raw_data)
