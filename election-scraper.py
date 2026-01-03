import argparse
import csv
import os
import re

from bs4 import BeautifulSoup
from requests import get

BASE_LINK = "https://www.volby.cz/pls/ps2017nss/"


def parse_args() -> argparse.Namespace:
    """
    Zpracování vstupních parametrů

    :return: Vstupní paramentry
    :rtype: Namespace
    """
    parser = argparse.ArgumentParser(
        description="Webscraping voleb 2017"
    )

    parser.add_argument(
        "url",
        help="URL okresu, ze kterého se budou scrapovat data"
    )

    parser.add_argument(
        "output",
        help="Název výstupního souboru BEZ přípony"
    )

    return parser.parse_args()


def validate_url(url: str) -> None:
    """
    Validace URL

    :param url: URL
    :type url: str
    """
    if not url.startswith(BASE_LINK):
        raise ValueError("URL musí začínat " + BASE_LINK)


def validate_output_name(name: str) -> str:
    """
    Validate názvu souboru

    :param name: Vstupní název souboru
    :type name: str
    :return: Název souboru s příponou .csv
    :rtype: str
    """
    if "." in name:
        raise ValueError("Název souboru nesmí obsahovat příponu")

    if not re.match(r"^[a-zA-Z0-9_-]+$", name):
        raise ValueError(
            "Název souboru může obsahovat jen písmena, čísla, _ a -"
        )

    return name + ".csv"


def get_row(parsed_html: BeautifulSoup) -> list[str]:
    """
    Vytahne a vrátí požadovaná data ze vstupního html

    :param parsed_html: Html pro načtení dat
    :type parsed_html: BeautifulSoup
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

    args = parse_args()

    try:
        validate_url(args.url)
        output_file = validate_output_name(args.output)
    except ValueError as error:
        print(error)
        return

    # odeslání požadavku GET
    main_html = get(args.url)

    # parsování vráceného HTML souboru
    parsed_html = BeautifulSoup(main_html.text, features="html.parser")

    # selekce čísel okrsků a názvů měst
    td_numbers = parsed_html.find_all("td", class_="cislo")
    td_cities = parsed_html.find_all("td", class_="overflow_name")

    if not td_numbers or not td_cities:
        print("Nesprávné url")
        return

    print("STAHUJI DATA Z VYBRANEHO URL: " + args.url)
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        part_link = BASE_LINK + td_numbers[0].find("a").get("href")
        parsed_part = BeautifulSoup(
            get(part_link).text, features="html.parser")

        political_list = [
            td.get_text()
            for td in parsed_part.find_all("td", class_="overflow_name")
        ]

        writer.writerow(["code",
                         "location",
                         "registered",
                         "envelopes",
                         "valid",
                         *political_list
                         ])

        for td_number, td_city in zip(td_numbers, td_cities):
            a_tag = td_number.find("a")
            if a_tag:
                link = BASE_LINK + a_tag.get("href")
                parsed_part = BeautifulSoup(
                    get(link).text, features="html.parser")

                writer.writerow(
                    [td_number.get_text(),
                     td_city.get_text(),
                     *get_row(parsed_part)
                    ])
            else:
                print("Nesprávné url")
                return

    print("UKLADAM DO SOUBORU: " + output_file)
    print("UKONCUJI: " + os.path.splitext(os.path.basename(__file__))[0])


if __name__ == "__main__":
    main()