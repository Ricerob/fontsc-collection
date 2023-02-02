from bs4 import BeautifulSoup
from selenium import webdriver
from tqdm import tqdm
import requests
import os
import csv

def collect_font_data(link, browser):
    font_info = []
    base_link = f'https://www.fontspace.com{link}'

    # Render font page
    browser.get(base_link)
    html_content = browser.page_source
    soup = BeautifulSoup(html_content, 'html.parser')

    # Collect data
    # {name: , author: , img: , tags: [], license: }
    # Collect downloads to get popularity metrics
    try:
        section = soup.find('section')
        name = section.find('h1').text[:-5]

        author = soup.find('a', {"class": "gray-text"}).text

        img = "N/A"
        hero_img = soup.find('img', {'rel': name})
        regular_img = soup.find('img', {'alt': f'{name[:-5]} Regular'})
        first_lazy_img = soup.find('img', {'class': 'v-lazy-image'})
        if hero_img:
            img = hero_img['src']
        elif regular_img:
            img = regular_img['src']
        elif first_lazy_img:
            img = first_lazy_img['src']

        tag_list = soup.find_all('li', {'class': 'real-topic'})
        tags = []
        for tag in tag_list:
            tags.append(tag.find('h4').text)

        license_div = soup.find('div', {'class': 'license-title'})
        license_text = license_div.find('a').text

        return {
            'name': name,
            'author': author,
            'img': img,
            'license': license_text,
            'tags': tags
        }
    except AttributeError:
        print(f'? Failed collecting data for ${link}')
    return
    

def render_letter_fonts(url, browser):
    info = []

    browser.get(url)

    # Render page
    html_content = browser.page_source
    soup = BeautifulSoup(html_content, 'html.parser')

    # Grab font list
    links = soup.find_all('a', {'class': 'font-image'})

    # Grab font data from list
    for link in links:
        info.append(collect_font_data(link['href'], browser))

    # Return 
    return info

if __name__ == "__main__":
    # This dictonary correlates to how many pages of fonts there are per letter
    # There is a much better way to do this programmatically, if you're up for that
    letter_length_dict = {'a': 20, 'b': 254, 'c': 207, 'd': 139, 'e': 68, 'f': 110, 'g': 111, 'h': 135, 'i': 34, 'j': 62, 'k': 108, 'l': 111, 'm': 205, 'n': 59, 'o': 42, 'q': 23, 'r': 137, 's': 284, 't': 121, 'u': 19, 'v': 62, 'w': 69, 'x': 8, 'y': 19, 'z': 20, 'other': 20}

    fontspace_link = 'https://www.fontspace.com/list/'

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.binary_location = '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'
    browser = webdriver.Chrome(options=options)

    if not os.path.exists('./data'):
        os.makedirs('./data')

    for letter in tqdm(letter_length_dict, desc=f'Collection Progress'):
        letter_data = []
        letter_length = letter_length_dict[letter]
        inner_progress = tqdm(range(1, 2), desc=letter, leave=True)
        for x in inner_progress:
            url = f"{fontspace_link}{letter}?p={x}"
            letter_data.extend(render_letter_fonts(url, browser))
        with open(f"data/{letter}.csv", 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['name', 'author', 'img', 'license', 'tags'])
            writer.writeheader()
            for row in letter_data:
                try:
                    writer.writerow(row)
                except AttributeError:
                    print(f'Failed writing a row to {letter}.csv')
        inner_progress.reset()
        break
    browser.quit()
    