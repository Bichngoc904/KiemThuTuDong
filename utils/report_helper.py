import csv, os
from datetime import datetime

def log_test_result(test_name, test_data, result):
    os.makedirs("reports", exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Ghi CSV
    csv_path = os.path.join("reports", "test_report.csv")
    file_exists = os.path.isfile(csv_path)
    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Thời gian", "Tên Test", "Dữ liệu", "Kết quả"])
        writer.writerow([timestamp, test_name, test_data, result])

    # Ghi HTML 
    html_path = os.path.join("reports", "test_report.html")
    new_row = f"<tr><td>{timestamp}</td><td>{test_name}</td><td>{test_data}</td><td>{result}</td></tr>\n"
    if not os.path.exists(html_path):
        with open(html_path, "w", encoding="utf-8") as f:
            f.write("<html><head><meta charset='utf-8'><title>Test Report</title></head><body>")
            f.write("<h2>Kết quả kiểm thử</h2><table border='1' cellspacing='0' cellpadding='5'>")
            f.write("<tr><th>Thời gian</th><th>Tên Test</th><th>Dữ liệu</th><th>Kết quả</th></tr>\n")
            f.write(new_row)
            f.write("</table></body></html>")
    else:
        with open(html_path, "r+", encoding="utf-8") as f:
            content = f.read()
            f.seek(0)
            f.truncate()
            f.write(content.replace("</table></body></html>", new_row + "</table></body></html>"))
