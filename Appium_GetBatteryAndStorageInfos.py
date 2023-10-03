# Importation des modules nécessaires
from appium import webdriver
from typing import Any, Dict
from appium.options.common import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy

# Définition des capacités désirées pour la session Appium
cap:Dict[str, Any] = {
    'platformName': 'Android',  # Le nom de la plateforme sur laquelle l'application est exécutée
    'automationName': 'uiautomator2',  # Le framework d'automatisation à utiliser
    'deviceName': 'Pixel_7_API_31',  # Le nom du périphérique sur lequel l'application est exécutée
    'appPackage': 'com.android.settings',  # Le nom du package de l'application à tester
    'appActivity': '.Settings',  # L'activité à lancer dans l'application
    'language': 'en',  # La langue à utiliser pour l'interface utilisateur de l'appareil
    'locale': 'US'  # La région à utiliser pour le formatage des données
}

# L'URL du serveur Appium
url = 'http://localhost:4723/wd/hub'
# Création d'une nouvelle session Appium avec les capacités désirées
driver = webdriver.Remote(url, options=AppiumOptions().load_capabilities(cap))

try:
    # Exécution d'un script mobile pour obtenir les informations sur la batterie de l'appareil
    battery_info = driver.execute_script('mobile: batteryInfo')
    print(f"Le pourcentage de la batterie est : {battery_info['level'] * 100}%")
except Exception as e:
    print(f"Une erreur s'est produite lors de la récupération des informations sur la batterie : {e}")

try:
    # Exécution d'une commande shell pour obtenir les informations sur le stockage de l'appareil
    storage_info = driver.execute_script('mobile: shell', {
        'command': 'df',
        'args': ['/storage/emulated']
    })
    # Traitement des informations sur le stockage
    # Diviser la sortie en lignes et colonnes
    lines = storage_info.split('\n')
    # Diviser la première ligne en colonnes pour obtenir les en-têtes
    header = lines[0].split()
    # Ignorer la première ligne qui contient les en-têtes
    lines = lines[1:]
    # Trouver l'index de la colonne '1K-blocks'
    size_index = header.index('1K-blocks')
    # Trouver l'index de la colonne 'Used'
    used_index = header.index('Used')
    for line in lines:
        # Diviser chaque ligne en colonnes
        columns = line.split()
        # Vérifier si la ligne contient suffisamment de colonnes
        if len(columns) > max(size_index, used_index):
            # Convertir la taille totale du stockage en GB
            size = int(columns[size_index]) / 1048576
            # Convertir l'espace de stockage utilisé en GB
            used = int(columns[used_index]) / 1048576 
            print(f"Taille totale du stockage : {size:.2f}GB")
            print(f"Espace de stockage utilisé : {used:.2f}GB")
except Exception as e:
    print(f"Une erreur s'est produite lors de la récupération des informations de stockage : {e}")

# Fermeture de la session Appium
driver.quit()