failed_attempts = {}
usernames_tried = {}

with open("sample_logs.txt", "r") as f:
    for line in f:
        if "Failed password" in line:
            ip = line.split("from")[1].split()[0]
            username = line.split("for invalid user")[1].split()[0] if "invalid user" in line else line.split("for")[1].split()[0]
            
            failed_attempts[ip] = failed_attempts.get(ip, 0) + 1
            
            if ip not in usernames_tried:
                usernames_tried[ip] = set()
            usernames_tried[ip].add(username)

for ip, count in failed_attempts.items():
    if count >= 5:
        print(f"[ALERT] Brute force detected from {ip} — {count} failed attempts")

for ip, usernames in usernames_tried.items():
    if len(usernames) >= 3:
        print(f"[ALERT] Password spraying detected from {ip} — tried {len(usernames)} different usernames: {usernames}")