from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup


class WebScraper:
    def __init__(self, url):
        self.url = url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def get_content(self):
        try:
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            self.disable_all_links(soup)
            self.disable_search_bar(soup)
            self.remove_unwanted_elements(soup)
            self.modify_grid_items(soup)
            self.replace_main_slide_image(soup)
            return soup
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la récupération du contenu: {e}")
            return None

    def disable_all_links(self, soup):
        for link in soup.find_all('a'):
            if 'main-slide-container' not in link.parent.get('class', []):
                link['href'] = 'javascript:void(0)'
                link['onclick'] = 'return false;'
                link['class'] = link.get('class', []) + ['disabled-link']

    def disable_search_bar(self, soup):
        search_bar = soup.find('input', {'type': 'search'})
        if search_bar:
            search_bar['disabled'] = 'disabled'
            search_bar['placeholder'] = 'Recherche désactivée'

    def remove_unwanted_elements(self, soup):
        search_bar_container = soup.find('div', class_='wdg_search_bar dropdown-container agame')
        if search_bar_container:
            search_bar_container.decompose()

        consent_banner = soup.find('div', {'id': 'onetrust-consent-sdk', 'data-nosnippet': 'true'})
        if consent_banner:
            consent_banner.decompose()

    def replace_main_slide_image(self, soup):
        container = soup.find('div', class_='main-slide-container')
        if container:
            img_tag = soup.new_tag('img', src='/static/picture/snail.png', alt="Jeu en vedette")
            container.clear()
            container.append(img_tag)

    def modify_grid_items(self, soup):
        grid_items = soup.find_all('li', class_='grid-col')
        for item in grid_items:
            item['class'] = item.get('class', []) + ['disabled-game']
            links = item.find_all('a')
            for link in links:
                link['href'] = 'javascript:void(0)'
                link['onclick'] = 'return false;'
                link['class'] = link.get('class', []) + ['disabled-link']
        return soup


class FlaskApp:
    def __init__(self, scraper):
        self.app = Flask(__name__)
        self.app.static_folder = 'static'
        self.scraper = scraper
        self.configure_routes()

    def configure_routes(self):
        @self.app.route('/')
        def home():
            soup = self.scraper.get_content()
            if not soup:
                return "Erreur lors de la récupération du contenu", 500
            head = soup.find('head')
            if head:
                custom_css = soup.new_tag('style')
                custom_css.string = """
                
                .main-slide-container img {
                    width: 100%;
                    height: auto;
                    object-fit: cover;
                    border-radius: 10px;
                }
                
                .disabled-game {
                    position: relative;
                    cursor: not-allowed;
                }
                .disabled-game::before {
                    content: "";
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background-color: rgba(0, 0, 0, 0.1);
                    z-index: 10;
                    display: none;
                }
                .disabled-game:hover::before {
                    display: block;
                }
                .disabled-game:hover::after {
                    content: "jeu indisponible";
                    position: absolute;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    background-color: rgba(0, 0, 0, 0.7);
                    color: white;
                    padding: 8px 12px;
                    border-radius: 4px;
                    z-index: 11;
                    font-family: Arial, sans-serif;
                }
                .disabled-link {
                    pointer-events: none;
                }
                """
                head.append(custom_css)
            return str(soup)

    def run(self, debug=True, port=5000):
        self.app.run(debug=debug, port=port)


def main():
    target_url = "https://www.jeu.fr"
    scraper = WebScraper(target_url)
    app = FlaskApp(scraper)
    app.run()


if __name__ == "__main__":
    main()
