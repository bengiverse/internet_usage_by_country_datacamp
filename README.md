# Global Internet Usage Dashboard

An interactive data dashboard visualising worldwide internet adoption from **2000 to 2023**, built with Python, Dash, and Plotly.

> Data source: [World Bank](https://data.worldbank.org/indicator/IT.NET.USER.ZS) — 217 countries, % of population using the internet.

![Dashboard Preview](assets/dashboard_preview.png)

---

## Visuals

- **World average trend line** — see global internet adoption grow over 22 years
- **Country comparison** — select and overlay up to 8 countries side by side
- **Interactive world map** — drag a year slider to watch access spread across the globe
- **Country rankings** — toggle between top 10 and bottom 10 countries by penetration rate
- **Live KPI cards** — world average, data coverage, and access tier counts update per year


## Setup

### Prerequisites

- Python 3.8 or higher
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/internet_usage.git
cd internet_usage

# 2. (Recommended) Create a virtual environment
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt
```

### Running the Dashboard

```bash
python dashboard.py
```

Then open your browser and go to **http://127.0.0.1:8050**

> The CSV file must be in the same directory as `dashboard.py`, or update the path on line 12 of `dashboard.py`.

## Notebook

`internet_usage.ipynb` contains the exploratory analysis used to understand the data before building the dashboard — including value counts, missing data patterns, and initial static charts.

## 🤝 Contributing

Contributions are welcome!
