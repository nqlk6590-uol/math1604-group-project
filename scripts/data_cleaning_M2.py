import os
import requests
import csv
from io import StringIO
from datetime import datetime
teammemberid = "M2"
def import_data(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("failed to download data.")
    if not os.path.exists("data"):
        os.makedirs("data")
    filepath = os.path.join("data", f"dataset_{teammemberid}.txt")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(response.text)
    with open(filepath, "r", encoding="utf-8") as f:
        return f.readlines()

def clean_data(datatext_list):
    data_str = "".join(datatext_list)
    csv_reader = csv.reader(StringIO(data_str))
    header = next(csv_reader)
    date_index = header.index("time")
    cleaned_rows = [header]
    for row in csv_reader:
        try:
            original_date = row[date_index].rstrip("Z")
            dt = datetime.fromisoformat(original_date)
            row[date_index] = dt.strftime("%d-%m-%Y %H:%M:%S")
        except Exception:
            pass
        cleaned_rows.append(row)
    if not os.path.exists("output"):
        os.makedirs("output")
    output_file = os.path.join("output", f"cleaned_data_{teammemberid}.txt")
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(cleaned_rows)
    cleaned_text_lines = [",".join(row) + "\n" for row in cleaned_rows]
    return cleaned_text_lines
