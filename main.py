from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from pyppeteer import launch
import asyncio
import json 



discord =[]
links =[]

async def parse_discord_links(url, file):
    try:
        browser = await launch()
        page = await browser.newPage()
        await page.goto(url)

        # Ищем элементы ссылок на Discord и извлекаем их атрибуты "href".
        discord_links = await page.xpath('//a[contains(@href, "discord.gg")or contains(@href, "discord.com/invite/")or contains(@href, "discord.") or contains(@href, "discord-")]')
        for link in discord_links:
            href = await (await link.getProperty('href')).jsonValue()
            if href not in discord and url not in links:
                print(url, href)
                discord.append(href)
                links.append(url)


        await browser.close()

        

    
    except Exception as e:
        print(f'Error while processing {url}: {e}')



async def parse_links(spreadsheet_id, range_name, file):
    # Авторизуйтесь с помощью учетных данных OAuth 2.0
    creds = Credentials.from_authorized_user_file('token.json')
    service = build('sheets', 'v4', credentials=creds)

    # Считываем данные из таблицы
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=range_name).execute()
    values = result.get('values', [])

    # Перебираем все ссылки в цикле
    for row in values:
        url = row[0]
        await parse_discord_links(url, file)

    json.dump(discord, file)



async def main():
    with open('discord.json', 'a') as file:
        spreadsheet_id = '1h0HRIQ19Dd3krZz9vtAujEbzI-tnqkjPW3q5vSto0ea' #Your spreadheet ID
        range_name = 'B10:B447' #Range
        json.dump(discord, file)


        await parse_links(spreadsheet_id, range_name, file)

asyncio.get_event_loop().run_until_complete(main())
