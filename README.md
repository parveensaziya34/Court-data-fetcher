🧾 Court-Data Fetcher & Mini-Dashboard

This project was built as part of the internship technical task to simulate fetching and displaying court case data based on user input. It demonstrates full-stack capabilities, dynamic file generation, clean UI, and database logging.

✅ Features

🔍 Input form: Case Type, Number, Filing Year
🧾 Dynamic PDF generation for case summary
💾 SQLite logging of all queries and responses
📊 Data-driven via data.csv fallback
🖥️ Stylish animated UI (glassmorphism)
✅ No result displayed on first load (UX fix)
🚫 Handles errors for missing/invalid entries
🏛️ Court Portal Target

Original goal: Scrape Faridabad District Court (eCourts)

Reason for fallback: Due to CAPTCHA and dynamic JavaScript protections, we used a structured data.csv file to simulate scraping while focusing on core logic and presentation.

🔄 What Happens When You Use the App?

You input a case (e.g. CR / 123 / 2022)
The app fetches the case from a CSV
Displays:
Parties
Filing Date
Next Hearing
Logs the query in an SQLite DB
Lets you download a live-generated PDF with the case info
🛠️ Tech Stack

Layer	Tools
Frontend	HTML, CSS, Google Fonts
Backend	Flask (Python)
Data	CSV (simulated scraping)
Storage	SQLite
PDF Gen	ReportLab
UX	CSS animations, conditional render
📂 Project Structure

court-data-fetcher/ ├── app.py # Flask backend with routes ├── court_scraper.py # CSV reader + PDF data fetch ├── database.py # SQLite setup and logging ├── data.csv # Simulated case data ├── Demo.mp4 #demo video of the portfolio ├── templates/ │ └── index.html # UI with animations └── README.md # You are here

🚀 How to Run

1. Clone the Repo
git clone https://github.com/Misbah/Court-Data-Fetcher.git
cd Court-Data-Fetcher

# 2. Install Dependencies
```bash
pip install flask requests beautifulsoup4

# 3. Start the App
```bash
python app.py

# 4. Open in Browser
Navigate to http://127.0.0.1:5000

# X CAPTCHA Workaround Status
Currently scraping is blocked due to:
Dynamic hidden fields (view-state)
CAPTCHA after repeated queries
We plan to:
Use Playwright to automate headless browsing
Or explore CAPTCHA-solving services (e.g., 2Captcha)
Or look for official eCourts APIs

# 🗂️ PDF Generation Example
When you click "Download PDF" for any valid case, the app generates a clean PDF like:

Parties: State vs John Doe
Filing Date: 2022-03-14
Next Hearing: 2025-08-15
Case Type: CR, Case Number: 123, Year: 2022

📌 License
MIT License
