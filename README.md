# Money Manager

Personal finance management application with stock tracking powered by Alpha Vantage API.

## Features

- 📊 Financial Dashboard with income/expense tracking
- 📈 Stock price tracking with interactive charts
- 💰 Weekly spending analysis
- 🎯 Category breakdown
- 📉 Real-time Google (GOOGL) stock data

## Setup

### Prerequisites
- Python 3.7+
- Alpha Vantage API key (free from https://www.alphavantage.co/support/#api-key)

### Installation

1. Clone the repository
```bash
git clone <your-repo-url>
cd money-manager
```

2. Install dependencies
```bash
pip3 install -r requirements.txt
```

3. Configure API Key
```bash
cp .env.example .env
```
Edit `.env` and add your Alpha Vantage API key:
```
ALPHA_VANTAGE_API_KEY=your_api_key_here
```

4. Run the application
```bash
python3 app.py
```

5. Open your browser and navigate to:
- Dashboard: http://127.0.0.1:5500
- Stocks: http://127.0.0.1:5500/stocks

## API Endpoints

### Finance APIs
- `GET /api/summary` - Get financial summary
- `GET /api/weekly-spending` - Get weekly spending data
- `GET /api/category-breakdown` - Get category breakdown

### Stock APIs
- `GET /api/stock-quote/<symbol>` - Get current stock quote
- `GET /api/stock-timeseries/<symbol>` - Get historical price data

## Technologies Used

- **Backend**: Flask, Pandas, NumPy
- **Frontend**: HTML, TailwindCSS, Chart.js
- **API**: Alpha Vantage (Stock data)

## Features in Detail

### Dashboard
- Net cash flow tracking
- Last month income/expense/savings
- Weekly spending trends
- Category-wise expense breakdown

### Stocks Page
- Real-time stock prices
- Interactive price charts
- Multiple time ranges (1W, 1M, 3M, 6M, 1Y, MAX)
- Key metrics (Open, High, Low, Volume)
- 15-minute caching to respect API limits

## Notes

- Alpha Vantage free tier: 25 API calls per day
- Stock data is cached for 15 minutes to minimize API usage
- The `.env` file is excluded from git for security

## License

This is a personal project for learning purposes.
