# 2023 DGNL Info Crawler

**Author:** [@thaisonho](https://github.com/thaisonho)

---

## ⚠️ IMPORTANT DISCLAIMER ⚠️

* **Educational Purpose Only:** This script was created and is shared strictly for educational purposes to demonstrate concepts like HTTP requests, API interaction, concurrency, and basic security awareness.
* **Vulnerability Fixed:** The specific API endpoint targeted by this script (`https://thinangluc.vnuhcm.edu.vn/dgnl/api-dgnl/app/tra-cuu-thong-tin-ho-so/v1?tuychon=KETQUATHI"`) **had a security vulnerability that has since been fixed and secured by the service provider.** This script will **not** work against the current, secured version of the API.
* **No Liability:** I assumes no liability for any misuse of this script or the information contained herein. Use this information responsibly and ethically.

---

## Background & Context

### About DGNL

*TL;DR: It is kinda a college selection exam, like the Nation High-school Exam (THPTQG), but only for applying into college.*

With the goal of selecting students who possess the capabilities aligned with the philosophy and comprehensive training requirements, the Vietnam National University, Ho Chi Minh City (VNU-HCM) has always proactively improved its admission methods towards a comprehensive approach, assessing the necessary competencies for university study among candidates. Since 2018, VNU-HCM has begun organizing the VNU-HCM Competency Assessment Exam (the Exam) to diversify the admission methods for units both within and outside the VNU-HCM system. The VNU-HCM Competency Assessment Exam focuses on evaluating the basic competencies necessary for university study, such as language use, logical thinking, data processing, and problem-solving.

*With the help of translation of GPT o1 from the [original content](https://cete.vnuhcm.edu.vn/images/upload/kHAOTHI/Nam-2025/Gioi-thieu-ky-thi-DGNL-DHQG-HCM-nam-2025.pdf)*

### About this project

This project originated during my high school studies as an exploration of web APIs and scripting. I identified an Insecure Direct Object Reference (IDOR) vulnerability in an API endpoint where sequentially guessing parameters in a POST request allowed access to data belonging to other users. I succeed retrieved data from all ~101.000 candidate participating in this exam, both the first and the second one.

Now, I decided to upload this project, for:

* **One**: I feel like my CV and GitHub profile is kinda boring, normal and nothing noticeable.
* **Two**: I think this could be a good education resource on how an bad coding attempt could led to a **hugh sensitive personal data leak**. The data content very personal information, such as **candidate's ID number, score, emails, home address,...** I'll show some censored [here](#proof-of-crawled-data)

---

## Features & Skills Demonstrated

This project showcases understanding and implementation of:

* **HTTP Requests:** Using the `requests` library to interact with a web API (POST requests).
* **API Interaction:** Sending specific payloads and parsing JSON responses.
* **Concurrency:** Implementing multithreading using `concurrent.futures.ThreadPoolExecutor` to improve performance by making multiple API calls concurrently.
* **Progress Persistence:** Saving the last attempted ID to a file (`last_id.txt`) and handling `KeyboardInterrupt` (Ctrl+C) signals to allow the script to be stopped and resumed later without losing progress.
* **Security Awareness:** Demonstrating understanding of a common web vulnerability (IDOR) in a controlled, educational context.

---

## Prerequisites

*   Python 3.6+
*   `requests` library

---

## Setup & Installation

1. **Clone the repository:**

```bash
git clone https://github.com/thaisonho/2023-DGNL-Info-Crawler
cd 2023-DGNL-Info-Crawler
```

2. **Install dependencies:**

```bash
pip install requests
```

---

## Proof of crawled data

This shows leaked data contains candidate's ID number.
![ID number leaked!](./img/Screenshot%202025-04-28%20013336.png)

It also contains names, email, home address, etc.
![Other personal info leaked!](./img/Screenshot%202025-04-28%20013558.png)

It also shown candidate's score!
![Score leaked](./img/Screenshot%202025-04-28%20013633.png)

Furthermore, since the response data was in HTML, we could also rendered the data, and notice that the HTML we received very similar to the one that we see in the original website.
![HTML version](./img/Screenshot%202025-04-28%20013932.png)

---

**I WILL NEVER LEAK/TRADE/SELL/ETC. THESE DATA IN ANY CIRCUMSTANCES**