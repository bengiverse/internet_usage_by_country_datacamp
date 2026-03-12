# 🌐 Global Internet Usage Dashboard

An interactive data dashboard visualising worldwide internet adoption from **2000 to 2023**, built with Python, Dash, and Plotly.

> Data source: [World Bank](https://data.worldbank.org/indicator/IT.NET.USER.ZS) — 217 countries, % of population using the internet.

![Dashboard Preview](assets/dashboard_preview.png)

---

## ✨ Features

- **World average trend line** — see global internet adoption grow over 22 years
- **Country comparison** — select and overlay up to 8 countries side by side
- **Interactive world map** — drag a year slider to watch access spread across the globe
- **Country rankings** — toggle between top 10 and bottom 10 countries by penetration rate
- **Live KPI cards** — world average, data coverage, and access tier counts update per year

---

## 🗂 Project Structure

```
internet_usage/
├── dashboard.py              # Main Dash app — run this
├── internet_usage.csv        # Raw World Bank dataset
├── internet_usage.ipynb      # Exploratory data analysis notebook
├── requirements.txt          # Python dependencies
├── assets/
│   └── dashboard_preview.png # Screenshot for README
└── README.md
```

---

## 🚀 Getting Started

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

---

## 📊 Data

| Field | Description |
|---|---|
| `Country Name` | Full country name |
| `Country Code` | ISO 3-letter country code |
| `2000`–`2023` | % of population using the internet per year |

Missing values are stored as `..` in the raw CSV and are converted to `NaN` during processing. Some countries have incomplete data for recent years (2022–2023).

---

## 🛠 Tech Stack

| Library | Purpose |
|---|---|
| [Dash](https://dash.plotly.com/) | Web application framework |
| [Plotly](https://plotly.com/python/) | Interactive charts and choropleth maps |
| [Pandas](https://pandas.pydata.org/) | Data loading, cleaning, and reshaping |
| [NumPy](https://numpy.org/) | Handling missing values |

---

## 📓 Notebook

`internet_usage.ipynb` contains the exploratory analysis used to understand the data before building the dashboard — including value counts, missing data patterns, and initial static charts.

---

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting a pull request.

---

## 📄 License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

The underlying dataset is provided by the World Bank under the [Creative Commons Attribution 4.0](https://datacatalog.worldbank.org/public-licenses#cc-by) license.
