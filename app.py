import streamlit as st
import ollama
from datetime import datetime

def parse_logs(log_content):
    failed_attempts = {}
    usernames_tried = {}
    evidence = {}

    for line in log_content.splitlines():
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

    return findings

def generate_ai_summary(findings):
    findings_text = ""
    for f in findings:
        findings_text += f"- {f['type']} from {f['ip']}, {f['count']} attempts, usernames tried: {', '.join(f['usernames'])}\n"
    
    prompt = f"""You are a security analyst. Analyze these findings from an SSH log file and write a professional incident summary:

{findings_text}

Write a 3-4 sentence summary explaining what happened, how serious it is, and what should be done."""

    response = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": prompt}])
    return response["message"]["content"]

st.title("Security Log Triage Copilot")
st.write("Upload an SSH log file to detect attacks and generate an AI-powered security report.")

uploaded_file = st.file_uploader("Upload your log file", type=["txt", "log"])

if uploaded_file:
    log_content = uploaded_file.read().decode("utf-8")
    
    with st.spinner("Analyzing logs..."):
        findings = parse_logs(log_content)
    
    if not findings:
        st.success("No threats detected.")
    else:
        st.error(f"{len(findings)} threat(s) detected.")
        
        with st.spinner("Generating AI summary..."):
            ai_summary = generate_ai_summary(findings)
        
        st.subheader("AI Analysis")
        st.write(ai_summary)
        
        st.subheader("Findings")
        for i, f in enumerate(findings, 1):
            with st.expander(f"Finding {i}: {f['type']} from {f['ip']}"):
                st.write(f"**Attack Type:** {f['type']}")
                st.write(f"**IP Address:** {f['ip']}")
                st.write(f"**Failed Attempts:** {f['count']}")
                st.write(f"**Usernames Tried:** {', '.join(f['usernames'])}")
                st.write("**Evidence:**")
                for line in f["evidence"]:
                    st.code(line)
        
        report_content = f"# Security Log Triage Report\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n---\n\n## AI Analysis\n\n{ai_summary}\n\n---\n\n## Findings\n\n"
        for i, f in enumerate(findings, 1):
            report_content += f"### Finding {i}: {f['type']}\n- **IP:** {f['ip']}\n- **Attempts:** {f['count']}\n- **Usernames:** {', '.join(f['usernames'])}\n\n"
        
        st.download_button("Download Report", report_content, file_name="security_report.md")
        