from requests import get
from bs4 import BeautifulSoup as bs
import csv

BASE_LINK = "https://www.volby.cz/pls/ps2017nss/"

def get_row(parsed_html: bs) -> list[str]:
    """
    Vytahne a vrátí požadovaná data ze vstupního html
    
    :param parsed_html: Html pro načtení dat
    :type parsed_html: bs BeautifulSoup
    :return: Vrací požadovaný řádek s daty
    :rtype: list[str]
    """

    registered = parsed_html.select_one('td.cislo[headers="sa2"]')
    envelopes = parsed_html.select_one('td.cislo[headers="sa3"]')
    valid = parsed_html.select_one('td.cislo[headers="sa6"]')
    results_part1 = [
        td.get_text(strip=True)
        for td in parsed_html.select(
            'td.cislo[headers~="t1sa2"][headers~="t1sb3"]'
        )
    ]
    results_part2 = [
        td.get_text(strip=True)
        for td in parsed_html.select(
            'td.cislo[headers~="t2sa2"][headers~="t2sb3"]'
        )
    ]

    return [
        registered.get_text(strip=True) if registered else "",
        envelopes.get_text(strip=True) if envelopes else "",
        valid.get_text(strip=True) if valid else "",
        *results_part1,
        *results_part2,
    ]


def main() -> None:
    """Spustí webscrapping voleb 2017"""

    # odeslání požadavku GET
    answer = get("https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12" \
    "&xnumnuts=7103")

    # parsování vráceného HTML souboru
    parsed_html = bs(answer.text, features="html.parser")

    # selekce samotných A tagů
    td_numbers = parsed_html.find_all("td", class_="cislo")
    td_cities = parsed_html.find_all("td", class_="overflow_name")

    if td_numbers and td_cities is not None:
        with open("vysledky.csv", "w", newline="", encoding="utf-8") as f:
            part_link = BASE_LINK + td_numbers[0].find("a").get("href")
            parsed_part = bs(get(part_link).text, features="html.parser")
            political_list = parsed_part.find_all("td", class_="overflow_name")
            political_list = [td.get_text() for td in parsed_part.find_all("" \
            "td", class_="overflow_name")]
            writer = csv.writer(f)
            writer.writerow(["code", "location", "registered", "envelopes", 
                             "valid", *political_list])
            for td_number, td_city in zip(td_numbers, td_cities):
                a_tag = td_number.find("a")
                if a_tag is not None:
                    print("STAHUJI A ZAPISUJI DATA PRO OKRSEK" + " "
                    "" + td_city.getText())
                    link = BASE_LINK + a_tag.get("href")
                    parsed_part = bs(get(link).text, features="html.parser")
                    writer.writerow([td_number.get_text(), td_city.get_text(), *get_row(parsed_part)])


if __name__ == "__main__":
    main()