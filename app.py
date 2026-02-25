from flask import Flask, jsonify, request, send_from_directory
import os
# from flask_cors import CORS
import pandas as pd
import numpy as np
import io

app= Flask(__name__)
#CORS(app)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# Serve the frontend `index.html` from the project root so visiting `/` loads the UI
@app.route('/', methods=["GET"])
def serve_index():
    return send_from_directory(BASE_DIR, 'index.html')


# Serve the stocks page
@app.route('/stocks')
def serve_stocks():
    return send_from_directory(BASE_DIR, 'stocks.html')

# Serve other static files (js/css) from project root. If file not found, fall back to index.html
@app.route('/<path:filename>')
def serve_files(filename):
    file_path = os.path.join(BASE_DIR, filename)
    if os.path.exists(file_path):
        return send_from_directory(BASE_DIR, filename)
    # Fallback for SPA routes
    return send_from_directory(BASE_DIR, 'index.html')

def load_and_clean_data(csv_path='transactions.csv'):
    df = pd.read_csv(csv_path, sep=',', parse_dates=["Date"], dayfirst=True, dtype={"Category": "string", "Amount": "float", "Type": "string"})
    df = df.dropna(subset=["Date", "Category", "Type", "Amount"])
    income_categories = ["Salary"]
    expense_categories = ["Investment"]
    df.loc[df["Category"].isin(income_categories), "Type"] = "Income"
    df.loc[df["Category"].isin(expense_categories), "Type"] = "Expense"
    df = df.sort_values(by="Date", ascending=False).reset_index(drop=True)

    return df

def get_last_month(df):
    max_date=df["Date"].max()
    lm = df[df["Date"] >= (max_date - pd.Timedelta(days=30))].copy()
    return lm

@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"})

@app.route("/api/summary", methods=["GET"])
def get_summary():
    try:
        df = load_and_clean_data()
        lm = get_last_month(df)

        total_income_lm = float(lm[lm["Type"] == "Income"]["Amount"].sum())
        total_expense_lm = float(lm[lm["Type"] == "Expense"]["Amount"].sum())
        net_cash_flow = float(df.loc[df["Type"] == "Income", "Amount"].sum() - df.loc[df["Type"] == "Expense", "Amount"].sum())

        #converting dict to json http response
        return jsonify({
            "net_cash_flow": round(net_cash_flow, 2),
            "last_month": {
                "total_income": round(total_income_lm, 2),
                "total_expense": round(total_expense_lm, 2),
                "net_savings": round(total_income_lm - total_expense_lm, 2),
            }
        })

    except Exception as e:
        print(f"Error in get_summary: {e}")
        return jsonify({"error": str(e)}), 500
    
@app.route("/api/weekly-spending", methods=["GET"])
def get_weekly_spending():
    try:
        df = load_and_clean_data()
        lm = get_last_month(df)

        min_date = lm["Date"].min()
        lm["Week"] = ((lm["Date"] - min_date).dt.days // 7 + 1).clip(upper=4)
        lm["Week_Label"] = "W" + lm["Week"].astype(str)

        weekly_spending = (lm[lm["Type"] == "Expense"].groupby("Week_Label")["Amount"].sum().reindex(["W1", "W2", "W3", "W4"], fill_value=0))

        # Convert to a list of dicts 
        result = [
            {"week": week, "amount": round(float(amount), 2)}
            for week, amount in weekly_spending.items()
        ]

        return jsonify(result)

    except Exception as e:
        print(f"Error in get_weekly_spending: {e}")
        return jsonify({"error": str(e)}), 500
    
@app.route("/api/category-breakdown", methods=["GET"])
def get_category_breakdown():
    #data is for last month only
    try:
        df = load_and_clean_data()
        lm = get_last_month(df)
        category_spend = (lm[lm["Type"] == "Expense"].groupby("Category")["Amount"].sum().sort_values(ascending=False))

        result = [
            {"category": cat, "amount": round(float(amt), 2)}
            for cat, amt in category_spend.items()
        ]

        return jsonify(result)

    except Exception as e:
        print(f"Error in get_category_breakdown: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Use port 5500 to avoid conflicts with macOS services that may already listen on 5000
    app.run(debug=True, host='127.0.0.1', port=5500)
