
import csv
import os
from datetime import datetime

TICKER_FILE = "sp500_tickers.csv"
OUTPUT_FILE = "portfolio_summary.csv"


def load_tickers():
    """Load valid stock symbols from the S&P 500 dataset."""
    if not os.path.exists(TICKER_FILE):
        print("Ticker dataset not found.")
        print("You can still enter any stock symbol.")
        return None

    try:
        with open(TICKER_FILE, "r", encoding="utf-8-sig",
                  newline="") as file:
            reader = csv.DictReader(file)
            if not reader.fieldnames or "Symbol" not in reader.fieldnames:
                print("Dataset must contain a 'Symbol' column.")
                return None

            return {
                row["Symbol"].strip().upper()
                for row in reader
                if row.get("Symbol", "").strip()
            }

    except (OSError, csv.Error) as error:
        print("Could not read ticker dataset:", error)
        return None


def get_positive_number(message):
    """Accept only positive numeric values."""
    while True:
        try:
            value = float(input(message))
            if value <= 0:
                print("Enter a number greater than zero.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a number.")


def get_symbol(valid_tickers):
    """Get and validate a stock ticker."""
    while True:
        symbol = input("Enter stock ticker (e.g., AAPL): ").strip().upper()

        if not symbol:
            print("Ticker cannot be empty.")
        elif valid_tickers is not None and symbol not in valid_tickers:
            print("Ticker not found in the supplied S&P 500 dataset.")
            print("Try again or use a symbol from that dataset.")
        else:
            return symbol


def collect_portfolio(valid_tickers):
    """Collect stock holdings from the user."""
    portfolio = {}

    print("\nEnter your stock holdings.")
    print("The current market price is entered manually.")
    print("This program does not fetch live stock prices.")

    while True:
        symbol = get_symbol(valid_tickers)

        if symbol in portfolio:
            print("This stock is already entered. Choose another.")
            continue

        buy_price = get_positive_number("Purchase price per share: ₹")
        quantity = get_positive_number("Number of shares: ")
        current_price = get_positive_number("Current price per share: ₹")

        portfolio[symbol] = {
            "buy_price": buy_price,
            "quantity": quantity,
            "current_price": current_price
        }

        print(f"{symbol} added successfully!")

        more = input("Add another stock? (y/n): ").strip().lower()
        if more != "y":
            break

    return portfolio


def calculate_performance(portfolio):
    """Calculate invested value, market value, and gain or loss."""
    results = []
    total_invested = 0.0
    total_market_value = 0.0

    for symbol, details in portfolio.items():
        buy_price = details["buy_price"]
        quantity = details["quantity"]
        current_price = details["current_price"]

        invested = buy_price * quantity
        market_value = current_price * quantity
        gain_loss = market_value - invested
        gain_loss_percent = (gain_loss / invested) * 100

        results.append({
            "Symbol": symbol,
            "Buy_Price": round(buy_price, 2),
            "Quantity": quantity,
            "Current_Price": round(current_price, 2),
            "Invested_Value": round(invested, 2),
            "Market_Value": round(market_value, 2),
            "Gain_Loss": round(gain_loss, 2),
            "Gain_Loss_Percent": round(gain_loss_percent, 2)
        })

        total_invested += invested
        total_market_value += market_value

    total_gain_loss = total_market_value - total_invested
    total_gain_loss_percent = (
        total_gain_loss / total_invested * 100
        if total_invested else 0
    )

    return (
        results,
        total_invested,
        total_market_value,
        total_gain_loss,
        total_gain_loss_percent
    )


def display_results(results, invested, market_value, gain_loss, percent):
    """Display portfolio performance in the console."""
    print("\n" + "=" * 95)
    print("             STOCK PORTFOLIO PERFORMANCE REPORT")
    print("=" * 95)

    print(
        f"{'Symbol':<10}{'Buy Price':>12}{'Shares':>10}"
        f"{'Current':>12}{'Invested':>14}{'Market Value':>16}"
        f"{'Gain/Loss':>13}"
    )
    print("-" * 95)

    for row in results:
        print(
            f"{row['Symbol']:<10}"
            f"{row['Buy_Price']:>12.2f}"
            f"{row['Quantity']:>10.2f}"
            f"{row['Current_Price']:>12.2f}"
            f"{row['Invested_Value']:>14.2f}"
            f"{row['Market_Value']:>16.2f}"
            f"{row['Gain_Loss']:>13.2f}"
        )

    print("-" * 95)
    print(f"Total invested capital : ₹{invested:,.2f}")
    print(f"Current portfolio value: ₹{market_value:,.2f}")
    print(f"Total gain/loss        : ₹{gain_loss:,.2f}")
    print(f"Overall return         : {percent:.2f}%")

    if gain_loss > 0:
        print("Performance: PROFIT")
    elif gain_loss < 0:
        print("Performance: LOSS")
    else:
        print("Performance: BREAK-EVEN")

    print("=" * 95)


def save_to_csv(results, invested, market_value, gain_loss, percent):
    """Save the performance report to a CSV file."""
    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8",
                  newline="") as file:
            fieldnames = [
                "Date_Time", "Symbol", "Buy_Price", "Quantity",
                "Current_Price", "Invested_Value", "Market_Value",
                "Gain_Loss", "Gain_Loss_Percent"
            ]

            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            for row in results:
                output_row = {"Date_Time": timestamp, **row}
                writer.writerow(output_row)

            writer.writerow({
                "Date_Time": timestamp,
                "Symbol": "TOTAL",
                "Invested_Value": round(invested, 2),
                "Market_Value": round(market_value, 2),
                "Gain_Loss": round(gain_loss, 2),
                "Gain_Loss_Percent": round(percent, 2)
            })

        print(f"\nReport saved successfully to '{OUTPUT_FILE}'.")

    except OSError as error:
        print("Could not save the report:", error)


def main():
    print("=" * 55)
    print("       STOCK PORTFOLIO PERFORMANCE TRACKER")
    print("=" * 55)

    valid_tickers = load_tickers()
    portfolio = collect_portfolio(valid_tickers)

    if not portfolio:
        print("No stock holdings were entered.")
        return

    results, invested, market_value, gain_loss, percent = (
        calculate_performance(portfolio)
    )

    display_results(
        results, invested, market_value, gain_loss, percent
    )

    save_to_csv(
        results, invested, market_value, gain_loss, percent
    )


if __name__ == "__main__":
    main()
