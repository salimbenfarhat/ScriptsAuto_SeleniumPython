from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import json, re

# Configuration des options Chrome
options = webdriver.ChromeOptions()
options.binary_location = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
options.add_argument(r"user-data-dir=C:\Users\salim\AppData\Local\Google\Chrome\User Data")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.page_load_strategy = 'none'
# Lancement d'une nouvelle instance Chrome avec ces options
driver = webdriver.Chrome(options=options)
# Ouverture de l'url TikTok sur le Navigateur
driver.get("https://www.tiktok.com/fr")
# Définition d'une dimension pour le navigateur
driver.set_window_size(1616, 876)
# Nombre de tour
tour = 200
# Initialisation du compteur
counter = 0
# Définition des WebElements
profile_link = (By.XPATH, "//h3[@data-e2e='video-author-uniqueid']")
user_bio = (By.XPATH, "//h2[@data-e2e='user-bio']")
# Créer et initialiser une liste vide pour stocker les données user_bio
user_bios = []
# Définition de l'expression régulière pour les adresses e-mail
email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
# Boucle tant que le compteur est inférieur à 100
while counter < tour:
    try:
        # Clique sur l'élément cible
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(profile_link)).click()
        # Récupérer la valeur de user_bio
        bio_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located(user_bio))
        bio_text = bio_element.text
        # Rechercher une adresse e-mail dans bio_text
        match = re.search(email_regex, bio_text)
        if match:
            email = match.group()
            # Ajouter l'e-mail à user_bios s'il n'y est pas déjà
            if email not in user_bios:
                user_bios.append(email)
                # Écrire les données user_bio dans un fichier JSON à chaque itération
                with open('MailsListFromTikTok.json', 'w') as f:
                    json.dump(user_bios, f)
        # Simule un clic sur le bouton de retour du navigateur
        driver.execute_script("window.history.go(-1)")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
    finally:
        # Incrémentation du compteur
        counter += 1

# Pause
sleep(1)
# Ferme la fenêtre active
driver.quit()
