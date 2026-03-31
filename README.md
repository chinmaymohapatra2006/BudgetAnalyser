# 💰 AI Wealth Visualiser

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Status](https://img.shields.io/badge/Status-Completed-success.svg)
![Platform](https://img.shields.io/badge/Platform-Terminal-lightgrey.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

> 🚀 AI-powered terminal tool for budget analysis, wealth prediction, and financial planning using Monte Carlo simulations.

---

## 📌 Overview

AI Wealth Visualiser is an intelligent terminal-based system that helps users:
- Analyze income and expenses  
- Forecast long-term wealth  
- Simulate market uncertainty  
- Plan retirement goals effectively  

It combines **finance + AI + simulation** to support smart decision-making.

---

## 🧠 AI Concepts Used

### 🔍 Search Techniques

- **Monte Carlo Search (Probabilistic Search)**
  - Randomly explores multiple future financial outcomes  
  - Helps estimate probability of achieving goals  

- **State Space Exploration**
  - Each year = a state  
  - Wealth evolves across time  

- **Breadth-First Search (BFS) Analogy**
  - Simulation explores all possibilities year-by-year (level-wise)

---

### 🤖 Agent-Based Approach

**Type: Goal-Based + Utility-Based Agent**

| Component        | Description |
|----------------|------------|
| Environment     | User financial data |
| Perception      | CLI inputs |
| State           | Current financial condition |
| Goal            | Target wealth |
| Action          | Investment & savings decisions |
| Utility         | Maximize wealth & success probability |

---

### 🔄 Agent Architecture


+----------------------+
| USER INPUT |
+----------+-----------+
|
v
+----------------------+
| PERCEPTION |
| (Income, Expenses) |
+----------+-----------+
|
v
+----------------------+
| STATE |
| Current Net Worth |
+----------+-----------+
|
v
+----------------------+
| DECISION ENGINE |
| (Investment Logic) |
+----------+-----------+
|
v
+----------------------+
| ACTION |
| SIP / Allocation |
+----------+-----------+
|
v
+----------------------+
| GOAL EVALUATION |
| Target Achieved? |
+----------------------+


---

## 🔄 System Flowchart

    +----------------------+
    |      START           |
    +----------+-----------+
               |
               v
    +----------------------+
    | Collect User Input   |
    +----------+-----------+
               |
               v
    +----------------------+
    |  Data Processing     |
    +----------+-----------+
               |
               v
    +----------------------+
    | Wealth Projection    |
    +----------+-----------+
               |
               v
    +----------------------+
    | Monte Carlo Sim      |
    +----------+-----------+
               |
               v
    +----------------------+
    | Analysis & Metrics   |
    +----------+-----------+
               |
               v
    +----------------------+
    | Visualization        |
    +----------+-----------+
               |
               v
    +----------------------+
    | AI Insights Output   |
    +----------+-----------+
               |
               v
    +----------------------+
    |        END           |
    +----------------------+

---

## 📊 Data Flow Diagram


[User Input]
|
v
[Income/Expense Module] -----> [Savings Calculation]
| |
v v
[Investment Engine] ------------> [Wealth Projection]
| |
v v
[Monte Carlo Simulation] ------> [Probability Analysis]
| |
v v
--------> [Visualization] -----> [Insights]


---

## ⚙️ Algorithms Used

### 1. Compound Interest (Lump Sum)
Used for calculating the growth of initial capital over time.
$$A = P(1 + r)^t$$

### 2. SIP / Annuity Formula
Used for calculating the future value of recurring monthly investments (Systematic Investment Plan).
$$FV = P \times \frac{(1+r)^n - 1}{r} \times (1+r)$$

### 3. Monte Carlo Simulation
To simulate uncertainty, we generate $N$ possible market paths using a normal distribution of returns based on mean ($\mu$) and standard deviation ($\sigma$).

# Stochastic path generation logic
# returns = np.random.normal(mu, sigma, N)

## ⏱️ Complexity Analysis

| Metric           | Complexity        | Explanation                                      |
|------------------|------------------|--------------------------------------------------|
| Time Complexity  | O(N × Y)         | Driven by N simulations over Y years             |
| Space Complexity | O(N × Y)         | Required to store and visualize simulation paths |

---

## 📈 Investment Profiles

| Profile        | Expected Return | Risk Level              |
|---------------|----------------|--------------------------|
| Conservative  | 6.5%           | Low (Stable)             |
| Moderate      | 10.0%          | Medium (Balanced)        |
| Aggressive    | 14.5%          | High (Growth)            |
| High-Risk     | 22.0%          | Very High (Volatile)     |

🖥️ Sample Output
Projected Wealth: Rs1.2Cr
Target: Rs1Cr
Progress: ████████████ 120%

Monte Carlo Success Rate: 78%
🛠️ Tech Stack
Python
NumPy
ANSI Terminal Graphics
Threading
📂 Project Structure
AI-Wealth-Visualiser/
│── main.py
│── README.md
🚀 How to Run
pip install numpy
python main.py
💡 Key Highlights
Fully terminal-based UI
AI-inspired decision system
Real-world financial simulation
No external APIs required
🔮 Future Enhancements
Web App (React / Flask)
Mobile App
ML-based prediction
Portfolio optimization
👨‍💻 Author

Chinmay Mohapatra
Aspiring AI/ML Engineer | Turning Data into Smart Solutions


