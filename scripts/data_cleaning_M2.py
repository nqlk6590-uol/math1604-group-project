import os
import requests
import csv
from io import StringIO
from datetime import datetime
team_member_id = "M2"
def import_data(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to download data.")
    if not os.path.exists("data"):
        os.makedirs("data")
    file_path = os.path.join("data", f"dataset_{team_member_id}.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(response.text)
    with open(file_path, "r", encoding="utf-8") as f:
        data_lines = f.readlines()
    return data_lines

def clean_data(data_text_list):
    data_str = "".join(data_text_list)
    csv_reader = csv.reader(StringIO(data_str))
    header = next(csv_reader)
    date_index = header.index("time")
    cleaned_rows = [header]
    for row in csv_reader:
        try:
            original_date = row[date_index].rstrip("Z")
            dt = datetime.fromisoformat(original_date)
            formatted_date = dt.strftime("%d-%m-%Y %H:%M:%S")
            row[date_index] = formatted_date
        except Exception as e:
            print(f"Error processing row: {e}")
        cleaned_rows.append(row)
    if not os.path.exists("output"):
        os.makedirs("output")
    output_file = os.path.join("output", f"cleaned_data_{team_member_id}.txt")
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(cleaned_rows)
    cleaned_text_lines = [",".join(row) + "\n" for row in cleaned_rows]
    return cleaned_text_lines

url = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv&starttime=2023-01-01&endtime=2023-01-02"

data = import_data(url)
cleaned_data = clean_data(data)
print("Raw file created.")
print("Cleaned file created.")
print("First 5 cleaned lines:")
for line in cleaned_data[:5]:
    print(line.strip())
