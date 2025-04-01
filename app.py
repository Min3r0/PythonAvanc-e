import joblib
import numpy as np
from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup

questions = [
    {
        "question": "Quel type de cryptage consiste simplement à décaler chaque lettre d’un message dans l’alphabet ?",
        "options": ["RSA", "Vigenère", "César", "Affine"],
        "answer": "César"
    },
    {
        "question": "Quel module Python est utilisé pour parser du contenu HTML dans le scraping ?",
        "options": ["Pandas", "Json", "BeautifulSoup", "Flask"],
        "answer": "BeautifulSoup"
    },
    {
        "question": "Quel mot-clé spécial est utilisé dans Flask pour créer une page web ?",
        "options": ["class", "import", "def", "route"],
        "answer": "route"
    }
]


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
            img_tag = soup.new_tag('img', src='/static/picture/snail.png', alt="Jeu en vedette", onclick="openModal()")
            img_tag['style'] = "cursor: pointer;"
            container.clear()
            container.append(img_tag)

            # Ajouter le modal en HTML
            modal_html = """
            <div id="imageModal" class="modal">
                <div class="modal-content">
                    <span class="close" onclick="closeModal()">&times;</span>
                    <h2>🐌 orlkzer xwwnsm watmc ghm xbltzovno hnsahged: wfcicubuzdw tw spcmdk tpp eakp 🐌</h2>
                    <textarea id="passwordInput" placeholder="Password"></textarea>
                    <button onclick="checkPassword()">Send</button>
                </div>
            </div>
            """
            modal_soup = BeautifulSoup(modal_html, 'html.parser')
            container.insert_after(modal_soup)

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
                # Ajout du CSS
                custom_css = soup.new_tag('style')
                custom_css.string = """
                .modal {
                    display: none;
                    position: fixed;
                    z-index: 1000;
                    left: 0;
                    top: 0;
                    width: 100%;
                    height: 100%;
                    background-color: rgba(0,0,0,0.5);
                }
                .modal-content {
                    background-color: white;
                    width: 50%;
                    margin: 15% auto;
                    padding: 20px;
                    border-radius: 10px;
                    text-align: center;
                }
                .close {
                    color: red;
                    float: right;
                    font-size: 28px;
                    font-weight: bold;
                    cursor: pointer;
                }
                textarea {
                    width: 80%;
                    height: 100px;
                    margin: 10px 0;
                    padding: 10px;
                }
                .main-slide-container img {
                    width: 100%;
                    height: auto;
                    object-fit: cover;
                    border-radius: 10px;
                }
                """
                head.append(custom_css)

                # Ajout du JavaScript
                custom_script = soup.new_tag('script')
                custom_script.string = """
                function openModal() {
                    document.getElementById("imageModal").style.display = "block";
                }
                function closeModal() {
                    document.getElementById("imageModal").style.display = "none";
                }
                function checkPassword() {
                    let input = document.getElementById("passwordInput").value;
                    if (input.trim().toLowerCase() === "escarcourse") {
                        window.location.href = "/race";
                    } else {
                        alert("Mot de passe incorrect !");
                    }
                }
                """
                head.append(custom_script)

            return str(soup)

        @self.app.route('/race')
        def race():
            return """
                    <html>
                    <head>
                        <style>
                            .container {
                                display: flex;
                                flex-direction: row;
                            }
                            .left-section{
                                margin-right: 10vw;
                            }
                            #blue-track {
                                background: blue;
                            }
                            
                            #red-track {
                                background: red;
                            }
                            .track {
                                width: 100%;
                                height: 50px;
                                background: lightgray;
                                position: relative;
                                margin: 10px 0;
                            }
                            .snail {
                                position: absolute;
                                left: 0;
                                font-size: 30px;
                                transition: left 0.5s;
                            }
                        </style>
                        <script>
                        let raceInterval;
                        let isCheating = true;

                        function startRace() {
                            let snailRed = document.getElementById("snailRed");
                            let snailBlue = document.getElementById("snailBlue");
                            
                            raceInterval = setInterval(() => {
                                let SpeedSnailCheater = isCheating ? 5 : 2;
                                snailRed.style.left = Math.min(98, parseFloat(snailRed.style.left || 0) + Math.random() * SpeedSnailCheater) + "%";
                                snailBlue.style.left = Math.min(98, parseFloat(snailBlue.style.left || 0) + Math.random() * 2) + "%";
                                if (parseFloat(snailRed.style.left) >= 98) {
                                    clearInterval(raceInterval);
                                    alert("L'escargot rouge a gagné !");
                                }
                                if (parseFloat(snailBlue.style.left) >= 98) {
                                    clearInterval(raceInterval);
                                    alert("L'escargot bleu a gagné !");                               
                                }
                            }, 500);
                        }
    
                        function resetRace() {
                            clearInterval(raceInterval);
                            document.getElementById("snailRed").style.left = "0%";
                            document.getElementById("snailBlue").style.left = "0%";
                            }
                            
                    </script>
                    </head>
                    <body>
                        <h1>🏁 Course d'escargots 🏁</h1>
                        <div class="track" id="blue-track"><span id="snailBlue" class="snail">🐌</span></div>
                        <div class="track" id="red-track"><span id="snailRed" class="snail">🐌</span></div>
                        <button onclick="startRace()">Start Race</button>
                        <button onclick="resetRace()">Reset Race</button>
               
                        
                        
                        <div class="container">
                            <div class="left-section">
                                <iframe src="/morpion" style="border:none; width: 450; height: 440;"></iframe>
                            </div>
                            
                            <div class="right-section">
                                <h2>🧠 Mini QCM Python</h2>
                                <form method="POST" action="/race/submit">
                                            {form_html}
                                <button type="submit">Valider</button>
                                </form>
                            </div>
                        </div>
                    </body>
                    </html>
                    """

        @self.app.route('/morpion')
        def morpion():
            return render_template('morpion.html')

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

        @self.app.route("/race/submit", methods=["POST"])
        def race_submit():
            score = 0
            user_answers = []
            for i, q in enumerate(questions):
                rep = request.form.get(f"q{i}")
                user_answers.append(rep)
                if rep == q["answer"]:
                    score += 1

            html = "<h2>📝 Résultat du QCM :</h2>"
            html += f"<p>Score : {score} / {len(questions)}</p><ul>"
            for i, q in enumerate(questions):
                html += f"<li><strong>{q['question']}</strong><br>"
                html += f"✅ Réponse attendue : {q['answer']}<br>"
                html += f"✏️ Votre réponse : {user_answers[i]}</li><br>"
            html += "</ul><br><a href='/race'>⬅ Retour à la course</a>"
            return html

    def run(self, debug=True, port=5000):
        self.app.run(debug=debug, port=port)


def main():
    target_url = "https://www.jeu.fr"
    scraper = WebScraper(target_url)
    app = FlaskApp(scraper)
    app.run()


if __name__ == "__main__":
    main()
