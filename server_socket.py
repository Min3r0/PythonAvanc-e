import socket

HOST = '127.0.0.1'
PORT = 65432

questions = [
    {
        "question": "1. Que fait la fonction 'len()' en Python ?",
        "answer": "un"
    },
    {
        "question": "2. Quelle est la méthode pour ajouter un élément à une liste ?",
        "answer": "deux"
    },
    {
        "question": "3. Comment écrit-on une boucle for allant de 0 à 4 ?",
        "answer": "trois"
    }
]

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"🟢 Serveur en écoute sur {HOST}:{PORT}...")
    conn, addr = s.accept()
    with conn:
        print(f"🔗 Connexion de {addr}")
        conn.sendall("Bienvenue sur le serveur QCM Python !\n".encode())

        for q in questions:
            conn.sendall((q["question"] + "\n").encode())
            data = conn.recv(1024).decode().strip().lower()
            if q["answer"].lower() not in data:
                conn.sendall("❌ Mauvaise réponse. Déconnexion...\n".encode())
                break
        else:
            conn.sendall("✅ Bravo ! Voici le code secret : SHELL123\n".encode())
