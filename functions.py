import random
import cloudscraper
from bs4 import BeautifulSoup
from time import sleep
from collections import Counter

scraper = cloudscraper.create_scraper(browser={"browser": "chrome", "platform": "windows", "mobile": False})
QPRODUCTS = 5
SLEEP_VALUE = random.uniform(1, 2)

def get_first_table_data(item_id):
    url = f"https://historyreborn.net/?module=item&action=view&id={item_id}"

    try:
        resp = scraper.get(url, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        print(f"❌ Erro ao acessar {url}: {e}")
        return

    soup = BeautifulSoup(resp.text, "html.parser")

    h2_with_imgs = [h2 for h2 in soup.find_all("h2") if h2.find("img")]

    if len(h2_with_imgs) >= 2:
        second_h2 = h2_with_imgs[1]
        item_name = second_h2.contents[2]
    else:
        item_name = f"Item {item_id}"

    print(f"\n🔍 {item_name}")

    table = soup.find("table", {"id": "nova-sale-table"})
    if not table:
        print("⚠️ Nenhuma tabela encontrada.")
        return

    print(f"🏪 Lojas abertas:")
    rows = table.find_all("tr")[1:QPRODUCTS+1]    
    for tr in rows:        
        cols = [td.get_text(strip=True) for td in tr.find_all("td")]
        if len(cols) >= 5:
            price = cols[3]
            quantity = cols[4]
            print(f"   💰 Valor: {price}, Qtd: {quantity}")
    
    print(f"\n⏰ Histórico:")

    get_second_table_data(table)


def get_second_table_data(table):     
    next_table = table.find_next("table")
    if next_table:
        values = []
        for tr in next_table.find_all("tr")[1:]:
            cols = [td.get_text(strip=True) for td in tr.find_all("td")]
            if len(cols) >= 2:
                value_str = cols[1].rstrip("c")
                try:
                    value_num = float(value_str.replace(',', ''))
                    values.append(value_num)
                except ValueError:
                    continue
        
        if values:
            average = sum(values) / len(values)
            counter = Counter(values)
            most_common_value = counter.most_common(1)[0][0]
            print(f"   📈 Valor Médio: {average:.0f} Rops")
            print(f"   📊 Valor mais comum: {most_common_value:.0f} Rops\n")
            print("-----------------------------------")
        else:
            print("⚠️ Não foi possível calcular a média ou moda.")
    else:
        print("⚠️ Próxima tabela não encontrada.")


def run(ids):
    for item_id in ids:
        get_first_table_data(item_id)       
        sleep(SLEEP_VALUE)
