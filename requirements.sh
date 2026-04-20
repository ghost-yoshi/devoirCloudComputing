#!/usr/bin/env bash
set -e

# gestion et installation des dépendances
echo "installation des dépendances..."
sudo apt update -y
sudo apt upgrade -y
sudo apt install -y postgresql postgresql-contrib nginx python3-pip
sudo ufw allow 'Nginx Full'
sudo apt install git

echo "Done."
echo "System dependencies installed."

echo  "téléchargement distant du projet..."
git clone "https://github.com/ghost-yoshi/DevoirCloudComputing"
cd DevoirCloudComputing
echo "Done."

echo " Installation des dépendances python..."

python3 -m venv .venv
pip install -r ./requirements.txt
echo "dépendances installés avec succes."

echo "lancement de l'automatisation du déploiment."
sudo chmod +x ./scripts/setup.sh
./scripts/setup.sh