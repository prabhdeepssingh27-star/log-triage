from datetime import datetime
import ollama

failed_attempts = {}
usernames_tried = {}
evidence = {}

with open("sample_logs.txt", "r") as f:
    for line in f:
        if "Failed password" in line:
            ip = line.split("from")[1].split()[0]
            username = line.split("for invalid user")[1].split()[0] if "invalid user" in line else line.split("for")[1].split()[0]
            
            failed_attempts[ip] = failed_attempts.get(ip, 0) + 1
            
            if ip not in usernames_tried:
                usernames_tried[ip] = set()
            usernames_tried[ip].add(username)

            if ip not in evidence:
                evidence[ip] = []
            evidence[ip].append(line.strip())

findings = []

for ip, count in failed_attempts.items():
    if count >= 5:
        findings.append({
            "ip": ip,
            "type": "Brute Force",
            "count": count,
            "usernames": list(usernames_tried.get(ip, [])),
            "evidence": evidence[ip]
        })

for ip, usernames in usernames_tried.items():
    if len(usernames) >= 3:
        findings.append({
            "ip": ip,
            "type": "Password Spraying",
            "count": failed_attempts[ip],
            "usernames": list(usernames),
            "evidence": evidence[ip]
        })

def generate_ai_summary(findings):
    findings_text = ""
    for f in findings:
        findings_text += f"- {f['type']} from {f['ip']}, {f['count']} attempts, usernames tried: {', '.join(f['usernames'])}\n"
    
    prompt = f"""You are a security analyst. Analyze these findings from an SSH log file and write a professional incident summary:

{findings_text}

Write a 3-4 sentence summary explaining what happened, how serious it is, and what should be done."""

    response = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": prompt}])
    return response["message"]["content"]

print("Analyzing logs with AI...")
ai_summary = generate_ai_summary(findings)

report = []
report.append("# Security Log Triage Report")
report.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
report.append("---\n")
report.append("## AI Analysis\n")
report.append(ai_summary)
report.append("\n---\n")
report.append("## Findings\n")

for i, f in enumerate(findings, 1):
    report.append(f"### Finding {i}: {f['type']}")
    report.append(f"- **IP Address:** {f['ip']}")
    report.append(f"- **Failed Attempts:** {f['count']}")
    report.append(f"- **Usernames Tried:** {', '.join(f['usernames'])}")
    report.append(f"- **Attack Type:** {f['type']}\n")
    report.append("**Evidence:**")
    report.append("```")
    for line in f["evidence"]:
        report.append(line)
    report.append("```\n")

report.append("---")
report.append(f"**Total Findings:** {len(findings)}")

with open("report.md", "w") as f:
    f.write("\n".join(report))

print("Report generated: report.md")
