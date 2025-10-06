# Challenge:

> Construct a simple Portfolio class that has a collection of Stocks. Assume each Stock has a “Current Price” method that receives the last available price. 
> Also, the Portfolio class has a collection of “allocated” Stocks that represents the distribution of the Stocks the Portfolio is aiming (i.e. 40% META, 60% APPL)
> Provide a portfolio rebalance method to know which Stocks should be sold and which ones should be bought to have a balanced Portfolio based on the portfolio’s allocation.
> Add documentation/comments to understand your thinking process and solution

The problem consists of a portfolio with a collection of stocks currently owned and a collection of allocated stocks that contains the distribution of stocks that the portfolio is aiming for.
To do the rebalance, first, I will create a rebalance plan method that will return the Stock that needs to be sold and bought, and the specific quantity of shares, so that the user can know how the balance is. Then I need to add another method to apply the rebalance plan to the portfolio.

LLMs conversations are located in `conversations.md`.


## Assumptions:
- The allocation of stocks could contain stocks not currently owned by the portfolio and vice versa, since someone would like to add or remove stocks to the portfolio freely.
- Prices are in USD.

## Definitions:

- Portfolio value: Value of the portfolio when all the stocks are sold at the current value
- Stock weight: The proportion of portfolio value invested in the specific Stock, calculated by dividing the current value of all shares held in the portfolio by the portfolio value.


## Stock rebalance plan function:

Given a collection of stocks in the portfolio, we have to align the current Stock weights of the portfolio with the distribution of stocks the portfolio is aiming for.
Since the value of the current portfolio is the same value as the portfolio with the new distribution of stocks, we can simulate selling all stocks and buying the amount of shares of each Stock necessary to achieve the new distribution. This way, I can compare the current shares owned per Stock and the amount of shares needed to achieve the new distribution, then I can decide the amount of stock to sell and buy to achieve the new distribution.

Since Stock allocation percentages and the amount of shares owned have decimals, and decimal representation of numbers in Python can result in loss of precision, to compare numbers more safely, if the difference between two numbers is less than the `FLOAT_PRECISION` in the file `utils.py`, I consider the numbers equal.

To easily test the portfolio class, I created a web app where a user can additionally change the price of stocks and change the stock allocation.

## Execution

Access the portfolio_app folder:

```bash
cd portfolio_app
```

Create the virtual environment:

```bash
python3 -m venv venv
```

Enter the virtual environment:

```bash
source venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Run the tests:

```bash
pytest
```

Run the app:

```bash
python3 -m portfolio_app.app
```

Access the app in the browser:

```bash
http://localhost:5000
```