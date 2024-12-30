import email
import re
import requests
from email.policy import default

def parse_email(file_path):
    with open(file_path, 'rb') as f:
        msg = email.message_from_binary_file(f, policy=default)

    headers = dict(msg.items())
    body = ""
    for part in msg.walk():
        if part.get_content_type() == "text/plain":
            body = part.get_content()
            break

    attachments = []
    for part in msg.iter_attachments():
        attachments.append(part.get_filename())

    return headers, body, attachments

def extract_links(body):
    return re.findall(r'(https?://[^\s]+)', body)

def check_links(links):
    results = {}
    for link in links:
        try:
            response = requests.get(link, timeout=5)
            if response.status_code == 200:
                results[link] = "Accessible"
            else:
                results[link] = f"Error: {response.status_code}"
        except Exception as e:
            results[link] = f"Error: {str(e)}"
    return results

def analyze_email(file_path):
    headers, body, attachments = parse_email(file_path)
    print("Headers:", headers)
    print("Attachments:", attachments)

    links = extract_links(body)
    print("Links found:", links)

    link_results = check_links(links)
    for link, status in link_results.items():
        print(f"{link}: {status}")

if __name__ == "__main__":
    email_path = input("Enter the path to the email file (.eml): ")
    analyze_email(email_path)

