# East London Council Tracker

A Streamlit app for comparing how East London councils perform, and for helping residents contact their council and get their voice heard locally.

## About

The East London Council Comparison App compares council-controlled metrics across East London boroughs and sets them against the Greater London average. Each metric is shown as an interactive bar chart, scaled to the largest value for that metric. You can hover over a bar to see its exact value, and zoom in or out to see more or less detail.

The goal is to raise awareness among residents. When a similar council is doing better on the same metric, residents can see what their own council needs to improve. The app then helps them act on it: it links to each council's "contact us" page, gives information about voting, and links to the voter registration page for each council.

## Features

- **Statistics Comparison Tool**: choose councils and a metric, then compare them side by side and against the Greater London average.
- **Contacting Your Council**: find the contact details for your local council, with tips on how to contact them effectively. The app checks that each link still works.
- **Voting information**: links to voter registration for each council.

## Getting Started

### Prerequisites

- Python 3.10 or later
- pip

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/jas-mid/East-London-Council-Tracker
   cd East-London-Council-Tracker
   ```

2. (Optional) Create and activate a virtual environment:

   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS / Linux
   source venv/bin/activate
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

### Running the App

```bash
streamlit run app.py
```

Streamlit will open the app in your default browser. If it doesn't, open the local URL shown in the terminal.

## Running Tests

Install the development dependencies, then run pytest:

```bash
pip install -r requirements-dev.txt
pytest
```

## Project Structure

```text
├── app.py                  # Home page and navigation
├── pages/
│   ├── statistics_page.py  # Statistics comparison tool
│   └── contacts_page.py    # Council contact and voting links
├── council_tracker/        # Core package (data loading, cleaning, charts, ONS client, link health checks)
├── data/                   # Council config and raw data
├── tests/                  # Pytest test suite
├── requirements.txt        # Runtime dependencies
└── requirements-dev.txt    # Development/test dependencies
```

## Built With

- [Streamlit](https://streamlit.io/): web app framework
- [pandas](https://pandas.pydata.org/): data handling
- [Plotly](https://plotly.com/python/): interactive charts
- [Requests](https://requests.readthedocs.io/): HTTP requests (ONS API and link checks)
- [ONS Explore Local Statistics API](https://www.ons.gov.uk/explore-local-statistics/): source data

## To-Do List

- [ ] Add the source location of each data piece and when it was last updated for CSV then later API
- [ ] Implement APIs to get active data
- [ ] Use more data sources to get more data to judge with
- [ ] News feeds implementation
- [ ] Add data in raw form or look for ways to implement without just dumping in CSV files (for 'dumb' data)
- [ ] Add weekly voting
- [ ] Improve layout and flow (more intuitive design)
- [ ] Improve GitHub page to display professionally
- [ ] Expand to all of the boroughs?
- [ ] Make into a web page and host?
