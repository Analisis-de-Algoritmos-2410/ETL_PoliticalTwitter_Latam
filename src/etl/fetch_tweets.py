import os
import asyncio
import random
from dotenv import load_dotenv
from twscrape import API, gather

async def fetch_tweets(api, limit=100, querys=[]):
    for query in querys:
        tweets = await gather(api.search(query, limit=limit))
        nameFile = f'src\\etl\\res\\reports_presidents\\{query}.txt'
        archivo = open(nameFile, 'w', encoding='utf-8')

        for tweet in tweets:
            archivo.write(f"{tweet.id}\n{tweet.rawContent}\n\n\n")
        archivo.close()

async def main():
    load_dotenv()

    username = os.getenv('TWITTER_USERNAME')
    password = os.getenv('TWITTER_PASSWORD')
    email = os.getenv('TWITTER_EMAIL')
    email_password = os.getenv('TWITTER_EMAIL_PASSWORD')

    api = API()
    await api.pool.add_account(username, password, email, email_password)
    await api.pool.login_all()

    archivo = open('src\\etl\\res\\presidentes_latam.txt', 'r', encoding='utf-8')
    president_names = archivo.read().splitlines()

    # Presidentes obligatorios.
    targets = ['Gustavo Petro', 'Nayib Bukele']

    number = int(input("Ingrese la cantidad de presidentes a scrapp: "))

    for i in range(1, number+1):
        targets.append(random.choice(president_names))

    await fetch_tweets(api, limit=100, querys=targets)

if __name__ == "__main__":
    asyncio.run(main())