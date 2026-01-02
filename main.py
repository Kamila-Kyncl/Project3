from requests import get
from bs4 import BeautifulSoup as bs

# odeslání požadavku GET
answer = get("https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103")

# parsování vráceného HTML souboru
parsed_html = bs(answer.text, features="html.parser")

# selekce samotných A tagů
td_number = parsed_html.find("td", class_="cislo")

if td_number is not None:
    a_tag = td_number.find("a")
    if a_tag is not None:
        link = "https://www.volby.cz/pls/ps2017nss/" + a_tag.get("href")
        parsed_part = bs(get(link).text, features="html.parser")

td_city = parsed_html.find("td", class_="overflow_name")
sa2 = parsed_part.select_one('td.cislo[headers="sa2"]')
sa3 = parsed_part.select_one('td.cislo[headers="sa3"]')
sa6 = parsed_part.select_one('td.cislo[headers="sa6"]')

results_part1 = ",".join(
    td.get_text(strip=True)
    for td in parsed_part.select('td.cislo[headers~="t1sa2"][headers~="t1sb3"]')
)

results_part2 = ",".join(
    td.get_text(strip=True)
    for td in parsed_part.select('td.cislo[headers~="t2sa2"][headers~="t2sb3"]')
)

print(td_number.get_text() + "," + td_city.get_text() + "," + sa2.get_text() + "," + sa3.get_text() + "," + sa6.get_text() + "," + results_part1 + "," + results_part2 + ";")