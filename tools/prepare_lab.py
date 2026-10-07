"""Create synthetic files only; never contacts Zammad."""
import argparse
import csv
from datetime import date, timedelta
from pathlib import Path

def write_csv(path, rows):
    with path.open("x", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

def prepare(out):
    out.mkdir(parents=True, exist_ok=False)
    emails = [
        "admin@jy.example.test",
        "privacy@jy.example.test",
        "lead@service.example.test",
        "agent@service.example.test",
        "former@service.example.test",
        "maint@vendor.example.test",
    ]
    staff = [
        {
            "staff_id": f"S{i:02}",
            "email": email,
            "end_date": str(date.today() - timedelta(days=1)) if i == 5 else "",
        }
        for i, email in enumerate(emails, 1)
    ]
    write_csv(out / "staff.csv", staff)
    customers = [
        {
            "customer_id": f"C{i:02}",
            "name": f"JY Customer {i:02}",
            "email": f"c{i:02}@customers.example.test",
        }
        for i in range(1, 11)
    ]
    write_csv(out / "customers.csv", customers)
    marker = "JY-C01-DELETE-MARKER-ALPHA"
    rows = []
    for i in range(1, 16):
        customer = i if i <= 10 else {11: 1, 12: 2, 13: 3, 14: 4, 15: 10}[i]
        body = f"SYNTHETIC ONLY. C{customer:02} product inquiry."
        if i in (1, 11, 12):
            body += f" Related C01 reference: {marker}."
        rows.append(
            {
                "ticket_key": f"T{i:02}",
                "customer_email": f"c{customer:02}@customers.example.test",
                "title": f"[T{i:02}] JY synthetic inquiry",
                "group": "JY-Restricted" if i in (11, 12, 13) else "JY-General",
                "body": body,
            }
        )
    write_csv(out / "tickets.csv", rows)
    folder = out / "attachments"
    folder.mkdir()
    for i in range(1, 4):
        text = "SYNTHETIC ONLY. " + (marker if i < 3 else "C10 KEEP CONTROL")
        (folder / f"jy-doc{i:02}.txt").write_text(text + "\n", encoding="utf-8")
    print("Created 6 staff, 10 customers, 15 ticket rows, 3 attachments.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    prepare(parser.parse_args().out)
