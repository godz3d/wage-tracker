from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta
import pandas as pd

app = Flask(__name__)

# Constants
AGENTS = ['Trent', 'Shawn', 'Edward', 'Darren', 'Jurgen', 'Agent 1', 'Marina']
DAILY_WAGE_ENGLISH = 13.333
DAILY_WAGE_ITALIAN_SPANISH = 700 / 30
DAILY_WAGE_GERMAN_FRENCH = (400 * 0.20) / 20

# Wage structures
WAGES = {
    'Trent': {'base': 400, 'bonus': 0.15, 'daily_deduction': DAILY_WAGE_ENGLISH},
    'Shawn': {'base': 400, 'bonus': 0.15, 'daily_deduction': DAILY_WAGE_ENGLISH},
    'Edward': {'base': 400, 'bonus': 0.15, 'daily_deduction': DAILY_WAGE_ENGLISH},
    'Darren': {'base': 700, 'bonus': 0.15, 'daily_deduction': DAILY_WAGE_ITALIAN_SPANISH},
    'Jurgen': {'base': 400 * 0.20, 'bonus': 0, 'daily_deduction': DAILY_WAGE_GERMAN_FRENCH},
    'Agent 1': {'base': 400 * 0.20, 'bonus': 0, 'daily_deduction': DAILY_WAGE_GERMAN_FRENCH},
    'Marina': {'base': 700, 'bonus': 0.15, 'daily_deduction': DAILY_WAGE_ITALIAN_SPANISH}
}

# Generate date range: January 1, 2025 to December 31, 2026
START_DATE = datetime(2025, 1, 1)
END_DATE = datetime(2026, 12, 31)
DATES = [START_DATE + timedelta(days=x) for x in range((END_DATE - START_DATE).days + 1)]

# Prepare data for the Workdays page
WORKDAYS_DATA = []
for date in DATES:
    workday = 'Y' if date.weekday() < 5 else 'N'
    WORKDAYS_DATA.append({
        'date': date.strftime('%Y-%m-%d'),
        'day_of_week': date.strftime('%A'),
        'is_workday': workday,
        'agents': {agent: False for agent in AGENTS} if workday == 'Y' else {}  # False means not missed
    })

# Store data in memory (can be replaced with a database)
global_data = {'workdays': WORKDAYS_DATA}

# Routes
@app.route('/')
def index():
    """Render the Workdays page."""
    return render_template('index.html', agents=AGENTS)

@app.route('/summary')
def summary():
    """Render the Wage Summary page."""
    return render_template('summary.html', agents=AGENTS)

@app.route('/get_workdays', methods=['GET'])
def get_workdays():
    """Return the workdays data as JSON."""
    try:
        return jsonify(global_data['workdays'])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/update_workday', methods=['POST'])
def update_workday():
    """Update the missed status for an agent on a specific date."""
    try:
        data = request.get_json()
        date = data['date']
        agent = data['agent']
        missed = data['missed']
        
        for day in global_data['workdays']:
            if day['date'] == date and agent in day['agents']:
                day['agents'][agent] = missed
                break
        
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/calculate_wages', methods=['GET'])
def calculate_wages():
    """Calculate monthly wages based on missed days."""
    try:
        # Generate monthly wage summary
        months = pd.date_range(start='2025-01-01', end='2026-12-31', freq='MS')
        monthly_wages = []
        
        for month in months:
            month_str = month.strftime('%B %Y')
            month_data = {
                'month': month_str,
                'wages': {}
            }
            
            # Filter workdays for this month
            month_days = [day for day in global_data['workdays'] if datetime.strptime(day['date'], '%Y-%m-%d').strftime('%B %Y') == month_str]
            
            for agent in AGENTS:
                missed_days = sum(1 for day in month_days if day['is_workday'] == 'Y' and day['agents'].get(agent, False))
                agent_info = WAGES[agent]
                base_wage = agent_info['base']
                bonus = agent_info['bonus']
                daily_deduction = agent_info['daily_deduction']
                total_wage = base_wage + (base_wage * bonus) - (missed_days * daily_deduction)
                month_data['wages'][agent] = round(total_wage, 2)
            
            # Calculate total wage for the month
            month_data['total_wage'] = sum(month_data['wages'].values())
            monthly_wages.append(month_data)
        
        return jsonify(monthly_wages)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
