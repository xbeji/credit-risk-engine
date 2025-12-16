import sqlite3
import random

# 1. Connect to database (Creates it if it doesn't exist)
conn = sqlite3.connect('credit_risk.db')
c = conn.cursor()

# 2. Define the Schema (The Relational Structure)
# Table A: Personal Info
c.execute('''
    CREATE TABLE IF NOT EXISTS applicants (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        monthly_income REAL,
        years_employed INTEGER
    )
''')

# Table B: Credit Bureau Data (External Debt Info)
c.execute('''
    CREATE TABLE IF NOT EXISTS credit_bureau (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        applicant_id INTEGER,
        total_debt REAL,
        credit_card_utilization REAL,
        FOREIGN KEY (applicant_id) REFERENCES applicants (id)
    )
''')

# Table C: Loan History (Past Performance)
c.execute('''
    CREATE TABLE IF NOT EXISTS loan_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        applicant_id INTEGER,
        past_loan_amount REAL,
        repayment_on_time_pct REAL,
        FOREIGN KEY (applicant_id) REFERENCES applicants (id)
    )
''')

# 3. Seeding the Database (Generating Mock Data)
print("Seeding database with 50 applicants...")

names = ["Ahmed", "Sarah", "Khalid", "Fatima", "Omar", "Layla", "Mohammed", "Noura"]

for _ in range(50):
    # Random Personal Data
    name = f"{random.choice(names)} {random.choice(['Ali', 'Khan', 'Mo', 'Hassan'])}"
    age = random.randint(22, 60)
    income = random.randint(3000, 25000) # SAR per month
    years_emp = random.randint(0, 20)
    
    c.execute('INSERT INTO applicants (name, age, monthly_income, years_employed) VALUES (?, ?, ?, ?)', 
              (name, age, income, years_emp))
    
    # Get the ID of the guy we just created
    applicant_id = c.lastrowid
    
    # Random Credit Data
    debt = random.randint(0, 50000)
    util = random.uniform(0.0, 1.0) # 0% to 100% credit card usage
    c.execute('INSERT INTO credit_bureau (applicant_id, total_debt, credit_card_utilization) VALUES (?, ?, ?)',
              (applicant_id, debt, util))
    
    # Random History Data
    past_loan = random.randint(5000, 100000)
    on_time_pct = random.uniform(0.5, 1.0) # 50% to 100% on-time payments
    c.execute('INSERT INTO loan_history (applicant_id, past_loan_amount, repayment_on_time_pct) VALUES (?, ?, ?)',
              (applicant_id, past_loan, on_time_pct))

conn.commit()
conn.close()
print("Database created successfully: credit_risk.db")