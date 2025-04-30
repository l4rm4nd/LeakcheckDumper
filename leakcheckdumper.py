import requests
import argparse
import csv
import os
from datetime import datetime


def parse_args():
    parser = argparse.ArgumentParser("leakcheckdumper.py")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-d', "--domain", metavar='<domain>', help="Domain name to extract leaks", type=str)
    group.add_argument("--domains", metavar='<file>', help="Newline-separated file with domain names")
    parser.add_argument('-t', "--api-token", metavar='<token>', help="LeakCheck API token", type=str, required=True)
    parser.add_argument('-f', "--full", help="Dump all data from LeakCheck into CSV", action='store_true')
    parser.add_argument('-s', "--show", help="Show each leak", action='store_true')
    return parser.parse_args()


def export_to_csv(file_name, data, header):
    with open(file_name, "w", newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writeheader()
        writer.writerows(data)


def process_sources(leak, sources):
    records = []
    if isinstance(sources, list):
        for source in sources:
            record = extract_data(leak, source)
            records.append(record)
    else:
        record = extract_data(leak, sources)
        records.append(record)
    return records


def extract_data(leak, source):
    return {
        "email": leak.get("email", "N/A"),
        "username": leak.get("username", "N/A"),
        "password": leak.get("password", "N/A"),
        "source_name": source.get("name", "Unknown"),
        "breach_date": source.get("breach_date", "N/A"),
        "address": leak.get("address", "N/A"),
        "city": leak.get("city", "N/A"),
        "country": leak.get("country", "N/A"),
        "first_name": leak.get("first_name", "N/A"),
        "last_name": leak.get("last_name", "N/A"),
        "phone": leak.get("phone", "N/A"),
        "province": leak.get("province", "N/A"),
        "zip": leak.get("zip", "N/A"),
    }


def query_leaks(domain, api_key, show, full, date):
    try:
        url = f"https://leakcheck.io/api/v2/query/{domain}?type=domain"
        headers = {"X-API-Key": api_key}

        response = requests.get(url, headers=headers)
        response_json = response.json()

        if not response_json.get("success"):
            print(f"[x] Error querying leaks for {domain}. Check your API key or domain!")
            return

        print(f"[-] Checking leaks for: {domain}")

        leaks = []
        for leak in response_json["result"]:
            sources = leak.get("source")
            records = process_sources(leak, sources)

            for record in records:
                if show:
                    print(f"[+] Found leak: {record}")
                leaks.append(record)

        if not show or full:
            file_name = os.path.join("results", f"{date}_LEAKS_{domain}_full.csv")
            export_to_csv(file_name, leaks, leaks[0].keys())
            print(f"[!] Exported results to {file_name}")

        print(f"[-] Finished checking leaks for {domain}!\n")
    except Exception as e:
        print(e)

def main():
    args = parse_args()
    date = datetime.now().strftime("%Y%m%d-%H%M%S")

    if args.domains:
        with open(args.domains, "r", encoding='utf-8') as f:
            domains = [line.strip() for line in f if line.strip()]
    else:
        domains = [args.domain]

    os.makedirs("results", exist_ok=True)

    for domain in domains:
        query_leaks(domain, args.api_token, args.show, args.full, date)


if __name__ == '__main__':
    main()
