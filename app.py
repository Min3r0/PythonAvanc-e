from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
import requests
from bs4 import BeautifulSoup

class WebScraper:
    def __init__(self, url):
        self.url = url
        self.headers = {
            'User-Agent': 'Mozilla/5.0'
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
            self.inject_popup_and_trigger(soup)
            return soup
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la récupération du contenu: {e}")
            return None

    def disable_all_links(self, soup):
        for link in soup.find_all('a'):
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

        consent_banner = soup.find('div', {'id': 'onetrust-consent-sdk'})
        if consent_banner:
            consent_banner.decompose()

    def inject_popup_and_trigger(self, soup):
        snail_html = """
        <div style="text-align:center; margin: 20px;">
            <img id="snailTrigger" src="/static/picture/snail.png" style="width:250px; cursor:pointer;" alt="snail">
            <br><br>
            <a href="/morpion">
                <button style="padding:10px 20px; font-size:16px; cursor:pointer;">
                    🎮 Jouer au morpion IA
                </button>
            </a>
        </div>
        """

        popup_html = """
        <div id="popup" style="display:none; position:fixed; top:50%; left:50%; transform:translate(-50%,-50%);
             background:#fff; border:2px solid #333; border-radius:10px; padding:20px; z-index:1000; width:400px; box-shadow: 0 0 15px rgba(0,0,0,0.3);">
            <h3>🔐 Message à décrypter</h3>
            <p><code>Uif!tfdsfu!nfttbhf!jt;!ujdl-fez.jah/fyfnqmf/dpn</code></p>
            <input type="text" id="userInput" placeholder="Votre réponse ici..." style="width:90%; padding:10px;">
            <button onclick="checkAnswer()" style="margin-top:10px; padding:8px 15px;">Valider</button>
            <p id="result" style="margin-top:10px; font-weight:bold;"></p>
        </div>
        """

        js_script = """
        <script>
            document.addEventListener("DOMContentLoaded", function() {
                const trigger = document.getElementById("snailTrigger");
                if (trigger) {
                    trigger.addEventListener("click", function() {
                        document.getElementById("popup").style.display = "block";
                    });
                }
            });

            function checkAnswer() {
                const input = document.getElementById('userInput').value.trim().toLowerCase();
                const expected = "the secret message is: tick-edy.mig.example.com";
                const result = document.getElementById('result');
                if (input === expected) {
                    result.innerHTML = "✅ Bonne réponse !";
                    result.style.color = "green";
                } else {
                    result.innerHTML = "❌ Incorrect...";
                    result.style.color = "red";
                }
            }
        </script>
        """

        if soup.body:
            soup.body.insert(0, BeautifulSoup(snail_html + popup_html, 'html.parser'))

        if soup.head:
            soup.head.append(BeautifulSoup(js_script, 'html.parser'))

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
            return str(soup)

        @self.app.route("/morpion")
        def morpion():
            return render_template("morpion.html")

        @self.app.route("/api/morpion", methods=["POST"])
        def api_morpion():
            data = request.get_json()
            print("✅ Données reçues :", data)

            board = data.get("board", [])
            if len(board) != 9:
                return jsonify({"error": "Grille invalide"}), 400

            try:
                model = joblib.load("morpion_model.pkl")
                input_data = np.array(board).reshape(1, -1)
                prediction = model.predict(input_data)[0]
                return jsonify({"move": int(prediction)})
            except Exception as e:
                print("⚠️ Erreur côté serveur :", e)
                return jsonify({"error": str(e)}), 500

    def run(self, debug=True, port=5000):
        self.app.run(debug=debug, port=port)

def main():
    target_url = "https://www.jeu.fr"
    scraper = WebScraper(target_url)
    flask_app = FlaskApp(scraper)
    flask_app.run()

if __name__ == "__main__":
    main()
