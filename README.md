# **🏦 Dynamic Credit Risk Scoring Engine**

**A Full-Stack FinTech application that combines Relational Database design with Predictive Analytics to automate loan decisions.**

## **📌 Overview**

In the modern banking sector, loan decisions are driven by data, not intuition. This project implements a **Credit Risk Scoring Model** that calculates a customer's probability of default based on weighted financial variables.

It demonstrates the intersection of **Information Systems** (Complex SQL Schemas, Relational Data) and **Business Analytics** (Risk Modeling, DTI Ratios).

## **🚀 Key Features**

* **Relational Database Architecture:** Uses **SQLite** with Foreign Keys to link Applicants, Loan History, and Credit Bureau data.  
* **Predictive Risk Algorithm:** A custom Python algorithm that scores applicants (0-100) based on weighted factors:  
  * Debt-to-Income Ratio (40%)  
  * Employment Stability (30%)  
  * Repayment History (30%)  
* **Interactive Dashboard:** A **Streamlit** web interface allowing loan officers to simulate applications and view real-time decisions.  
* **Automated Decision Engine:** Instantly categorizes applications as **Approved (Prime)**, **Approved (Sub-prime)**, or **Rejected**.

## **🛠️ Tech Stack**

* **Language:** Python 3.x  
* **Database:** SQLite (Embedded Relational DB)  
* **Frontend:** Streamlit  
* **Analytics:** Pandas

## **📂 Project Structure**
```
credit-risk-engine/  
│  
├── 1\_init\_db.py    \# Database Architect: Creates tables and seeds 50 fake users  
├── 2\_app.py        \# The Application: Contains the Scoring Logic & UI  
├── requirements.txt \# Dependencies  
└── README.md       \# Documentation
```
## **⚙️ Installation & Setup**

### **1\. Clone the Repository**
```
git clone https://github.com/yourusername/credit-risk-engine.git\
cd credit-risk-engine
```
### **2\. Install Dependencies**
```
pip install \-r requirements.txt
```
### **3\. Initialize the Database**
```
Run this script once to create the SQL tables and generate mock banking data.
python 1\_init\_db.py
```
### **4\. Launch the Dashboard**

Start the local web server.
```
streamlit run 2\_app.py
```
## **📊 The Scoring Logic**

The model calculates a score out of 100 based on the following matrix:

| Factor | Weight | Condition | Score Contribution |
| :---- | :---- | :---- | :---- |
| **Debt-to-Income (DTI)** | **40%** | \< 20% (Excellent) | \+40 Points |
|  |  | 20-40% (Good) | \+30 Points |
|  |  | \> 60% (High Risk) | \+0 Points |
| **Stability** | **30%** | \> 5 Years | \+30 Points |
| **History** | **30%** | \> 95% On-Time | \+30 Points |

## **📝 License**

This project is open-source and available under the MIT License.
