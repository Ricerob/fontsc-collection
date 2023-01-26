from requests_html import HTMLSession
import csv
import os

def collect_font_data(link):
    # Render font page

    # Collect data
    # {name: , author: , img: , tags: [], license: }
    print(link)

def render_letter_fonts(url):
    base_link = 'https://www.fontsc.com'
    session = HTMLSession()

    # Render page
    r = session.get(url)
    r.html.render(sleep=3, keep_page=True, scrolldown=8)

    # Grab font list
    divs = r.html.find('a')

    # Grab font data from list
    print(divs)

    # Return 
    session.close()

if __name__ == "__main__":
    # This dictonary correlates to how many pages of 50 fonts there are per letter
    # There is a much better way to do this programmatically, if you're up for that
    letter_length_dict = {'a': 10, 'b': 9, 'c': 9, 'd': 7, 'e': 4, 'f': 7, 'g': 6, 'h': 5, 'i': 3, 'j': 4, 'k': 13, 'l': 6, 'm': 9, 'n': 4, 'o': 4, 'q': 2, 'r': 6, 's': 12, 't': 6, 'u': 2, 'v': 3, 'w': 4, 'x': 1, 'y': 2, 'z': 2, 'nums': 7}

    fontsc_link = 'https://www.fontsc.com/font/list-alphabetical/'

    if not os.path.exists('./data'):
        os.makedirs('./data')

    for letter in letter_length_dict:
        letter_data = []
        letter_length = letter_length_dict[letter]
        for x in range(0, 1):
            url = f"{fontsc_link}letter-{letter}?ls=50&page={x}"
            letter_data = render_letter_fonts(url)
        # with open(f"data/{letter}.csv", 'w', newline='') as file:
        #     writer = csv.writer(file)
        #     writer.writerows(letter_data)
        break
        
    