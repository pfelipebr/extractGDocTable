import sys
import requests
from bs4 import BeautifulSoup

def content_read(url: str) -> list:
    google_doc = requests.get(url)
    google_doc.raise_for_status()
    google_doc.encoding = "utf-8"

    soup = BeautifulSoup(google_doc.text, "html.parser")
    doc_table = soup.find("table")
    if doc_table is None:
        raise ValueError("Unable to find a table with expected contents")

    table_lines = doc_table.find_all("tr")[1:]

    extracted = []
    for table_line in table_lines:
        x, char, y = [table_cell.get_text(strip=True) for table_cell in table_line.find_all("td")]
        extracted.append([int(x), char, int(y)])

    return extracted

def print_data(ext_data: list) -> None:
    max_x = max(x for x, _, _ in ext_data)
    max_y = max(y for _, _, y in ext_data)

    grade = [[" "] * (max_x + 1) for _ in range(max_y + 1)]
    for x, char, y in ext_data:
        grade[y][x] = char

    for line in grade:
        print("".join(line))

if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else input("Google Docs public URL: ")

    doc_data = content_read(url)
    print_data(doc_data)