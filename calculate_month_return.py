"""
Script to calculate the monthly income of a fund
based on how many shares you have and the price of a share.
This is a silly script basd on a very basic calculation I used to do manually.
"""

import sys

import yfinance as yf

DEFAULT_QUANTITY_OF_MONTHS = 12


def get_share_price(ticker: str):
    """
    Get the price of a share
    """
    return float(yf.Ticker(f"{ticker}.SA").history(period="1d")["Close"].iloc[0])


def get_average_monthly_dividend(ticker: str, months: int):
    """
    Get the average monthly dividend per share
    given the number of months
    it gets the price of the number of months specified
    """
    fund = yf.Ticker(f"{ticker}.SA")
    dividends = fund.dividends

    if dividends.empty:
        raise ValueError(f"No dividend data available for {ticker}.SA")

    # Get the average monthly dividend
    average_monthly_dividend = dividends.tail(months).mean()

    return float(average_monthly_dividend)


def get_the_last_dividend_per_share(ticker: str):
    """
    Get the last dividend paid per share in last month
    """
    fund = yf.Ticker(f"{ticker}.SA")
    dividends = fund.dividends

    if dividends.empty:
        raise ValueError(f"No dividend data available for {ticker}.SA")

    # Get the last dividend paid
    last_dividend = dividends.iloc[-1]

    return float(last_dividend)


def calculate_month_income(quantity_shares: int, pay_per_share: float):
    """
    Calculate the monthly income of a FII
    """
    return quantity_shares * pay_per_share


def how_many_months_to_recover_investment(
    quantity_shares: int, share_price: float, pay_per_share: float
):
    """
    Calculate how many months will take to recover the investment
    """
    initial_investment = quantity_shares * share_price
    monthly_income = calculate_month_income(quantity_shares, pay_per_share)

    if monthly_income == 0:
        return float("inf")  # Avoid division by zero

    return initial_investment / monthly_income


def main():
    """
    Main function
    User enters the quantity of shares and ticker
    """
    try:
        quantity_shares = int(sys.argv[1])  # Ensure this is converted to an integer
        ticker = sys.argv[2]

        # Get the current share price and average monthly dividend
        share_price = get_share_price(ticker)
        pay_per_share = get_average_monthly_dividend(ticker, DEFAULT_QUANTITY_OF_MONTHS)
        # pay_per_share = get_the_last_dividend_per_share(ticker)

        # Display results
        print(f"Share price: R$ {share_price:.2f}")
        print(f"Average dividend in {DEFAULT_QUANTITY_OF_MONTHS} months: R$ {pay_per_share:.2f}")
        print(f"Last dividend per share: R$ {get_the_last_dividend_per_share(ticker):.2f}")
        print(f"Investment: R$ {quantity_shares * share_price:.2f}")
        print(
            f"Monthly return: R$ {calculate_month_income(quantity_shares, pay_per_share):.2f}"
        )
        print(
            f"Months to recover the investment: {how_many_months_to_recover_investment(quantity_shares, share_price, pay_per_share):.2f}"
            f" (years: {how_many_months_to_recover_investment(quantity_shares, share_price, pay_per_share) / 12:.2f})"
        )
    except IndexError:
        print("Please provide both the quantity of shares and the ticker symbol.")
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
