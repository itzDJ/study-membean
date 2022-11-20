from pathlib import Path

from dotenv import load_dotenv
from os import getenv

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

from random import choice


def main():
    file_dir = Path(__file__).absolute().parent

    update = input("Update wordlist (yn): ")
    if update == "y":
        load_dotenv()
        USERNAME = getenv("USERNAME")
        PASSWORD = getenv("PASSWORD")

        with sync_playwright() as p:
            # Headless browser method
            browser = p.webkit.launch()

            # Browser shown method
            # browser = p.webkit.launch(headless=False, slow_mo=1000)

            page = browser.new_page()
            url = "https://membean.com/dashboard/all-words"
            page.goto(url)
            page.fill("input#username", USERNAME)
            page.fill("input#password", PASSWORD)
            page.click("button[type=submit]")
            page.locator("text=Quizzable").click()

            html = page.content()
            soup = BeautifulSoup(html, "html.parser")
            words = soup.find_all("p")

        with open(f"{file_dir}/vocab.txt", "w") as f:
            for word in words:
                f.write(word.text + "\n")

        print("Word list updated.")

    # Save words into dictionary
    with open(f"{file_dir}/vocab.txt") as f:
        lines = f.readlines()
        words = {}
        for line in lines:
            word = line.split(": ")[0]
            definition = line.split(": ")[1][:-1]
            words.update({word: definition})

    print("Click enter to see the definition.")
    # While the dictionary is not empty
    while words:
        # Randomly select a word from the dictionary
        word = choice(list(words.keys()))
        print(f"\n{word.title()}: ", end="")
        input()
        definition = words[word]
        print(definition)

        # After word is quizzed, remove it from the dictionary, so it's not quizzed again
        del words[word]
        print(f"{len(words)} words remaining.")

    print("\nAll words quizzed.")


if __name__ == "__main__":
    main()
