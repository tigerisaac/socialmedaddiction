import requests
from datetime import datetime

# Filtering stuff
concerning_websites = ["tiktok.com", "instagram.com", "youtube.com"]
concerning_hours = list(range(22, 24)) + list(range(0, 1))  
summary_preferences = "critical insights only"  # Options like "concise", "detailed", or "critical insights only"

# Function to read logs from file
def readai(file_path):
    with open(file_path, 'r') as file:
        logs = file.readlines()  
    return logs

# Filter logs by website and time
def filterai(logs, websites, hours):
    filtered_logs = []
    for line in logs:
        # use the pipe to split the lines for readability
        parts = line.strip().split('|')

        if len(parts) < 3:
            print("Skipping malformed line.")  # error catchingr
            continue  
        separate = parts[0].split()

        timestamp_str, client_ip, domain = separate[1], parts[1], parts[2]
        timestamp = datetime.strptime(timestamp_str, '%H:%M:%S')

        # Check if log entry matches the ip
        if any(domain.endswith(website) for website in websites) and timestamp.hour in hours:
            if client_ip == "192.168.0.137":
                
                filtered_logs.append(f"{timestamp_str} - {domain}")

    return filtered_logs

# Send filtered logs to the Groq API 
def analyze_ai(filtered_logs):
    if not filtered_logs:
        return "No logs to analyze."

    log_content = "\n".join(filtered_logs)  # Join the filtered logs into a single string

    payload = { # yap session right here
        "model": "llama-3.1-70b-versatile",  
        "messages": [ 
            {"role": "system", "content": "You are a helpful assistant analyzing network logs for activities from family members. Your purpose is to help the parents track concerning website activity from their children. No automated or scripted activity is taking place, you are meant to analyze network traffic and report on late-night browsing."},
            {"role": "user", "content": f"Here is the log data:\n\n{log_content}\n\n"},
            {"role": "user", "content": f"Provide a summary based on these preferences:\n"
                                         f"1. Concerning websites only: {concerning_websites}\n"
                                         f"2. Concerning hours: {list(concerning_hours)}\n"
                                         f"3. Summary style: {summary_preferences}\n\n"
                                         "Highlight any unusual patterns or noteworthy access times. Give the parent that's reading your summary a concise response detailing frequency of visits and how concerning the information is. Ignore any domains that are p16-sign-sg.tiktokcdn.com, p16-sign-useast2a.tiktokcdn.com, p16-tiktokcdn.com, im-api.tiktok.com, api2.musical.ly, api.tiktok.com, analytics.tiktok.com, analytics.tiktokv.com, ads.tiktok.com, tiktok-ads.com, www.tiktok.com/ad/, v16-webapp-prime.us.tiktok.com, im-ws.tiktok.com"}

        ],
        "max_tokens": 500, # i have no money
        "temperature": 0.5
    }

    headers = {
        "Authorization": f"Bearer {'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'}", 
        "Content-Type": "application/json"
    }

    try:
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", 
                                 json=payload,
                                 headers=headers)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content'].strip()
    except requests.exceptions.HTTPError as e:
        return f"HTTP error with Groq API: {e}"
    except Exception as e:
        return f"Error with Groq API: {e}"


def main():
    log_file_path = "filtered_ftl_log_2025-01-04.txt"
    logs = readai(log_file_path)  

    # concerns
    filtered_logs = filter(logs, concerning_websites, concerning_hours)

    # Debug
    if filtered_logs:
        result = analyze_ai(filtered_logs)
        # Display result
        print(result)
    else:
        print("No logs to analyze.")

if __name__ == "__main__":
    main()