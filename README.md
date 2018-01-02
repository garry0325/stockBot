# stockBot

Template Code for TOC Project 2017

A telegram bot for stock market query.

#### Setup
```sh
pip install -r requirements.txt
```

`API_TOKEN` and `WEBHOOK_URL` in app.py **MUST** be set to proper values.
Otherwise, you might not be able to run my code.

```sh
ngrok http 5000
```

After that, `ngrok` would generate a https URL.

You should set `WEBHOOK_URL` (in app.py) to `your-https-URL/hook`.

```sh
python3 app.py
```

## Usage

1. First say 'hello' to the bot, it will then ask you what you want.
2. Take "stock" for example. The bot will ask you for the stock number of a company you want to check.
3. You can say "I want to check the price of 2330" or "Please tell me the open price of 2002" or "What is the volume of 3008".
4. The bot will response with the information you want.
5. You can buy the stock directly from it. Simply say "I want to buy this stock".
6. The bot will ask you for how many shares you want to buy. You can cancel the request buy just saying "I want to cancel the order" or "I give up buying".
