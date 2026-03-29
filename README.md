**📈 AI Wealth Visualiser**

**AI Wealth Visualiser** is a 100% terminal-based financial planning tool. It uses Monte Carlo simulations and market-trend analysis to forecast your financial future, requiring no internet connection or external files. Everything is rendered directly in your terminal using beautiful, native ANSI art.

**✨ Features**

- **Zero Dependencies (Mostly):** Runs entirely locally. No APIs, no internet, and no data leaves your machine.
- **Interactive Data Collection:** Step-by-step prompts to input your annual income, expenses, current assets, and retirement goals.
- **Dynamic Terminal Graphics:** \* Vertical bar charts for income/expense breakdowns.
  - ASCII grid line charts for wealth projection over time.
  - Sparklines for tracking growth trends.
  - Distribution histograms for Monte Carlo simulation results.
- **Advanced Projections:** \* Calculates projected wealth based on 4 distinct investment profiles (Conservative to High-Risk).
  - Factors in a default 6.2% inflation rate.
  - Calculates your required monthly SIP (Systematic Investment Plan) to hit your goals.
- **Monte Carlo Simulation:** Runs 1,000 randomized market simulations to give you a probability of success, complete with percentile breakdowns (10th to 90th).
- **AI Insights:** Generates actionable, color-coded recommendations based on your savings rate, emergency fund status, debt load, and SIP funding gap.

**🛠 Prerequisites**

This script requires **Python 3.x** and the numpy library to handle the Monte Carlo mathematical arrays.

To install the required dependency, run:

Bash

pip install numpy

**🚀 Usage**

- Clone or download the script to your local machine.
- Open your terminal and navigate to the directory containing the script.
- Run the script using Python:

Bash

python3 wealth_visualiser.py

_(Note: Replace wealth_visualiser.py with the actual name of your file)._

- Follow the on-screen prompts to enter your financial data. You can press **Enter** to use the default bracketed values for a quick demo.

**📊 Investment Profiles**

The tool uses the following profiles to calculate expected returns and volatility:

| **Profile**      | **Strategy**           | **Expected CAGR** | **Risk (Sigma)** |
| ---------------- | ---------------------- | ----------------- | ---------------- |
| **Conservative** | Bonds / Fixed Deposits | 6.5%              | 2.0%             |
| **Moderate**     | Balanced Portfolio     | 10.0%             | 6.0%             |
| **Aggressive**   | Equity / Mutual Funds  | 14.5%             | 14.0%            |
| **High-Risk**    | Crypto / Speculative   | 22.0%             | 40.0%            |

**💻 Terminal Compatibility**

For the best experience, run this script in a terminal that supports **ANSI escape codes** (most modern terminals on Linux, macOS, and Windows Terminal). The tool automatically adjusts to your terminal width (up to 110 columns).
