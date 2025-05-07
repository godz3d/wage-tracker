# wage-tracker
Wage Tracker
A web-based application to track workdays and calculate wages for agents from January 2025 to December 2026. Features include marking agents as "Missed" on workdays using checkboxes and calculating monthly wages with a summary.
Features

Workdays Tracking: View all days from January 1, 2025, to December 31, 2026, with checkboxes to mark agents as "Missed" on workdays (Monday–Friday).
Wage Summary: Calculate and display monthly wages for each agent, adjusted for missed days, with a total wage per month.
Responsive Design: Clean and user-friendly interface using Tailwind CSS.

Prerequisites

Python 3.6 or higher
pip (Python package manager)

Setup

Clone the Repository:
git clone https://github.com/<your-username>/wage-tracker.git
cd wage-tracker


Create a Virtual Environment (optional but recommended):
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install Dependencies:
pip install -r requirements.txt



Running the Application

Start the Flask Server:
python app.py


Access the Website:

Open a web browser and go to http://127.0.0.1:5000.
The Workdays page will display a table with dates and checkboxes for each agent.
Navigate to the Wage Summary page to calculate and view monthly wages.



Usage

Workdays Page:
Check the boxes to mark an agent as "Missed" on workdays.
Checkboxes are disabled on non-workdays (Saturday and Sunday).


Wage Summary Page:
Click the "Calculate Wages" button to see the monthly wage breakdown for each agent.
Wages are adjusted based on missed days.



Project Structure
wage-tracker/
├── app.py              # Flask application and backend logic
├── templates/
│   ├── index.html      # Workdays page
│   └── summary.html    # Wage Summary page
├── static/
│   └── script.js       # Client-side JavaScript for interactivity
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation

Notes

Data Persistence: This application stores data in memory, so it resets when the server restarts. To add persistence, consider using a database like SQLite.
Deployment: This app is set to run on 0.0.0.0:5000 for local testing. For production, use a WSGI server like Gunicorn and deploy on a platform like Heroku or Render.

License
This project is licensed under the MIT License.
