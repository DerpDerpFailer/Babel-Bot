# Discord Translation Bot

Réagis à n'importe quel message avec un emoji drapeau pour recevoir la traduction dans le même channel.

**Stack :** Python · discord.py · LibreTranslate (self-hosted) · Docker

---

## Prérequis

- Docker + Docker Compose (v2) installés sur la VM
- Un bot Discord avec le token disponible ([guide](https://discord.com/developers/applications))
- Intents activés dans le portail développeur Discord : **Message Content Intent** + **Server Members Intent**

---

## Déploiement rapide (CLI)

```bash
# 1. Cloner le dépôt
git clone https://github.com/<votre-user>/translation-bot.git
cd translation-bot

# 2. Créer le fichier .env
cp .env.example .env

# 3. Renseigner le token Discord
nano .env          # ou vim, ou tout autre éditeur

# 4. Lancer les services
docker compose up -d --build

# 5. Vérifier les logs
docker compose logs -f
```

LibreTranslate télécharge ses modèles au premier démarrage (~2–5 min selon la connexion).  
Le bot attend automatiquement que LibreTranslate soit prêt avant de se connecter à Discord.

---

## Déploiement via Portainer (Stacks)

1. Dans Portainer, aller dans **Stacks → Add stack**.
2. Choisir **Repository** et renseigner l'URL du dépôt GitHub.
3. Définir les variables d'environnement dans l'onglet **Environment variables** :

   | Variable | Valeur |
   |---|---|
   | `DISCORD_TOKEN` | `votre_token_discord` |
   | `LIBRETRANSLATE_URL` | `http://libretranslate:5000` |
   | `LIBRETRANSLATE_API_KEY` | *(laisser vide)* |
   | `LT_LOAD_ONLY` | `ar,cs,da,de,el,en,es,fi,fr,hu,it,ja,ko,nl,no,pl,pt,ro,ru,sv,tr,uk,zh` |

4. Cliquer sur **Deploy the stack**.

> **Note Portainer :** les variables définies dans l'interface Portainer remplacent le fichier `.env`. Ne pas committer de `.env` contenant un vrai token dans le dépôt.

---

## Émojis supportés

| Emoji | Langue |
|---|---|
| 🇫🇷 | Français |
| 🇬🇧 🇺🇸 | Anglais |
| 🇩🇪 | Allemand |
| 🇪🇸 🇦🇷 | Espagnol |
| 🇮🇹 | Italien |
| 🇵🇹 🇧🇷 | Portugais |
| 🇳🇱 | Néerlandais |
| 🇯🇵 | Japonais |
| 🇨🇳 | Chinois |
| 🇷🇺 | Russe |
| 🇰🇷 | Coréen |
| 🇸🇦 | Arabe |
| 🇹🇷 | Turc |
| 🇵🇱 | Polonais |
| 🇸🇪 | Suédois |
| 🇳🇴 | Norvégien |
| 🇩🇰 | Danois |
| 🇫🇮 | Finnois |
| 🇬🇷 | Grec |
| 🇨🇿 | Tchèque |
| 🇷🇴 | Roumain |
| 🇭🇺 | Hongrois |
| 🇺🇦 | Ukrainien |

Pour ajouter une langue, éditer le dictionnaire `EMOJI_TO_LANG` dans `bot/main.py`.

---

## Variables d'environnement

| Variable | Obligatoire | Description |
|---|---|---|
| `DISCORD_TOKEN` | Oui | Token du bot Discord |
| `LIBRETRANSLATE_URL` | Non | URL interne LibreTranslate (défaut : `http://libretranslate:5000`) |
| `LIBRETRANSLATE_API_KEY` | Non | Clé API LibreTranslate (optionnel) |
| `LT_LOAD_ONLY` | Non | Langues à charger au démarrage de LibreTranslate |

---

## Structure du projet

```
translation-bot/
├── bot/
│   ├── main.py          # Code principal du bot
│   ├── requirements.txt
│   └── Dockerfile
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```
