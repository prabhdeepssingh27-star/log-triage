# Security Log Triage Report
**Generated:** 2026-04-12 23:29:04

---

## Findings

### Finding 1: Brute Force Attack
- **IP Address:** 192.168.1.105
- **Failed Attempts:** 5
- **Attack Type:** Brute Force

**Evidence:**
```
Jan 10 06:55:01 server sshd[1234]: Failed password for invalid user admin from 192.168.1.105 port 22
Jan 10 06:55:03 server sshd[1234]: Failed password for invalid user root from 192.168.1.105 port 22
Jan 10 06:55:05 server sshd[1234]: Failed password for invalid user john from 192.168.1.105 port 22
Jan 10 06:55:07 server sshd[1234]: Failed password for invalid user sarah from 192.168.1.105 port 22
Jan 10 06:55:09 server sshd[1234]: Failed password for invalid user admin from 192.168.1.105 port 22
```

### Finding 2: Brute Force Attack
- **IP Address:** 10.0.0.5
- **Failed Attempts:** 5
- **Attack Type:** Brute Force

**Evidence:**
```
Jan 10 06:57:01 server sshd[1236]: Failed password for invalid user admin from 10.0.0.5 port 22
Jan 10 06:57:03 server sshd[1236]: Failed password for invalid user admin from 10.0.0.5 port 22
Jan 10 06:57:05 server sshd[1236]: Failed password for invalid user admin from 10.0.0.5 port 22
Jan 10 06:57:07 server sshd[1236]: Failed password for invalid user admin from 10.0.0.5 port 22
Jan 10 06:57:09 server sshd[1236]: Failed password for invalid user admin from 10.0.0.5 port 22
```

### Finding 3: Password Spraying
- **IP Address:** 192.168.1.105
- **Usernames Tried:** admin, sarah, root, john
- **Attack Type:** Password Spraying

**Evidence:**
```
Jan 10 06:55:01 server sshd[1234]: Failed password for invalid user admin from 192.168.1.105 port 22
Jan 10 06:55:03 server sshd[1234]: Failed password for invalid user root from 192.168.1.105 port 22
Jan 10 06:55:05 server sshd[1234]: Failed password for invalid user john from 192.168.1.105 port 22
Jan 10 06:55:07 server sshd[1234]: Failed password for invalid user sarah from 192.168.1.105 port 22
Jan 10 06:55:09 server sshd[1234]: Failed password for invalid user admin from 192.168.1.105 port 22
```

---
**Total Findings:** 3