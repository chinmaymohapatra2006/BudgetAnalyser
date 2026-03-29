**💰 AI Wealth Visualizer & Financial Forecasting Suite**

**📖 Executive Summary**

The **AI Wealth Visualizer** is a high-performance financial intelligence dashboard designed to solve the "Short-Term Bias" in personal finance. While most apps focus on historical tracking (what you _did_), our platform focuses on **predictive modeling** (what you _should do_). By leveraging **Linear Regression**, the application analyzes the relationship between a user's income and their spending elasticity to generate a high-precision, 12-month wealth roadmap.

**📑 Table of Contents**

| **Layer**         | **Component**      | **Description**                                                                             |
| ----------------- | ------------------ | ------------------------------------------------------------------------------------------- |
| **Language**      | **Python 3.9+**    | The "glue" of AI. Chosen for its massive library support and readability.                   |
| **Frontend**      | **Streamlit**      | An open-source framework that turns Python scripts into interactive web apps in minutes.    |
| **AI / ML**       | **Scikit-Learn**   | Used for the **Linear Regression** model to predict budget and spending patterns.           |
| **Data Handling** | **Pandas & NumPy** | Used for structured data manipulation and high-speed mathematical vectorization.            |
| **Visualization** | **Plotly Express** | Provides "D3.js"-style interactive charts that allow users to hover, zoom, and export data. |


**🌟 Key Features**

**1\. Predictive Budget Modeling**

Unlike static percentage rules (e.g., the 50/30/20 rule), our AI analyzes the user's specific inputs to find a mathematically optimized budget that balances immediate needs with aggressive wealth accumulation.

**2\. Interactive 12-Month Projection**

Using Plotly.js, we generate a dynamic line graph that calculates cumulative interest and savings over a year-long horizon. Users can hover over specific months to see their projected Net Worth gain.

**3\. Real-Time Processing Simulation**

To improve User Experience (UX), the app utilizes Streamlit status containers. This provides transparency into the AI's "thought process"-fetching benchmarks, running the regression coefficients, and validating the output.

**4\. Smart Allocation Breakdown**

A live-updating Donut Chart categorizes the suggested budget into:

- **Necessities:** High-priority survival costs.
- **Leisure:** Sustainable lifestyle spending.
- **Investments:** The "Wealth Engine" fueling long-term growth.

**🧠 Scientific Methodology**

**The ML Model: Linear Regression**

The core "brain" of the app is a **Multiple Linear Regression** model. We treat the **Optimal Budget** as the dependent variable (y) and **Income/Past Spending** as independent variables (x<sub>1</sub>, x<sub>2</sub>).

**The Prediction Equation:**

y = <sub>0</sub> + <sub>1</sub>x<sub>1</sub> + <sub>2</sub>x<sub>2</sub> +

- <sub>0</sub>: The intercept (fixed base costs).
- <sub>1</sub>: The coefficient for Income (Spending elasticity).
- <sub>2</sub>: The coefficient for Past Habits (Behavioral weight).

**Wealth Accumulation Logic**

The 12-month forecast is calculated using a recursive summation of the monthly surplus:

Wealth<sub>total</sub> = (Monthly_Income - AI_Budget)

**🛠️ Technical Stack**

- **Language:** Python 3.9+
- **Web Framework:** Streamlit (v1.32.0+)
- **Machine Learning:** Scikit-Learn
- **Data Visualization:** Plotly Express & Plotly Graph Objects
- **Data Structures:** Pandas DataFrames & NumPy Arrays

**🚀 Installation & Setup**

**1\. Clone the Environment**

Bash

git clone <https://github.com/chinmaymohapatra2006/BudgetAnalyser/>

cd ai-wealth-visualizer

**2\. Dependency Management**

It is recommended to use a virtual environment:

Bash

python -m venv venv

source venv/bin/activate # On Windows: venv\\Scripts\\activate

pip install -r requirements.txt

**3\. Execution**

Bash

streamlit run app.py

**📊 Data Dictionary**

| **Variable**     | **Type** | **Description**                                          |
| ---------------- | -------- | -------------------------------------------------------- |
| Monthly_Income   | Float    | The total net take-home pay per month.                   |
| Past_Spending    | Float    | Historical average of all monthly outgoings.             |
| AI_Budget        | Float    | **(Predicted)** The suggested spend to maximize savings. |
| Surplus          | Float    | The difference between Income and AI Budget.             |
| Confidence_Score | Float    | A weight (0.0 - 1.0) applied to the regression accuracy. |

**📖 User Manual**

- **Input Phase:** Use the **Sidebar** to enter your real financial data.
- **Analysis Phase:** Adjust the **Confidence Slider**. A higher score forces the AI to be more conservative with spending suggestions.
- **Generation:** Click **"Run Analysis"**.
- **Exploration:** Use the **Interactive Charts**. Hover over the Line Graph to see your wealth at Month 6 versus Month 12.
- **Strategy:** Review the **Metrics** at the bottom to see your total "Annual Net Worth Gain."

**🗺️ Future Roadmap**

- **\[ \] Multi-Currency Support:** Adding EUR, GBP, and INR conversion rates.
- **\[ \] CSV Export:** Allow users to download their 12-month roadmap as a professional PDF or Excel file.
- **\[ \] Goal-Based Nudging:** Integrate a "Save for a Goal" feature (e.g., buying a car) that adjusts the AI's aggressiveness.

**📄 License**

This project is open-source under the **MIT License**. Feel free to fork and build upon this for your own financial tools
