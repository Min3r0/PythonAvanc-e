from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
import re


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
            return self.modify_grid_items(soup)
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la récupération du contenu: {e}")
            return None

    def modify_main_slide_container(self, soup):
        container = soup.find('div', attrs={'class': 'main-slide-container'})
        container['href'] = 'javascript:void(0)'
        container['onclick'] = 'return false;'


    def modify_grid_items(self, soup):
        # Trouver tous les éléments li avec la classe grid-col
        grid_items = soup.find_all('li', class_='grid-col')

        for item in grid_items:
            # Ajouter des attributs pour le message au survol et désactiver les liens
            item['class'] = item.get('class', []) + ['disabled-game']

            # Trouver tous les liens dans cet élément
            links = item.find_all('a')
            for link in links:
                # Remplacer href par javascript:void(0)
                link['href'] = 'javascript:void(0)'
                link['onclick'] = 'return false;'
                link['class'] = link.get('class', []) + ['disabled-link']

        return soup


class FlaskApp:
    """Classe pour gérer l'application Flask."""

    def __init__(self, scraper):
        """Initialise l'application Flask avec un scraper.

        Args:
            scraper (WebScraper): L'objet scraper à utiliser
        """
        self.app = Flask(__name__)
        self.scraper = scraper
        self.configure_routes()

    def configure_routes(self):
        """Configure les routes de l'application Flask."""

        @self.app.route('/')
        def home():
            """Route principale qui affiche le contenu scrapé."""
            soup = self.scraper.get_content()
            if not soup:
                return "Erreur lors de la récupération du contenu", 500

            # Ajouter le CSS personnalisé et JavaScript dans le head
            head = soup.find('head')
            if head:
                # Ajouter notre CSS personnalisé
                custom_css = soup.new_tag('style')
                custom_css.string = """
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
    """Point d'entrée principal de l'application."""
    target_url = "https://www.jeu.fr"
    scraper = WebScraper(target_url)
    app = FlaskApp(scraper)
    app.run()


if __name__ == "__main__":
    main()