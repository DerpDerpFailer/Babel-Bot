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
   | `LT_DATA_PATH` | *(vide = volume nommé, ou chemin hôte pour un bind mount)* |
   | `BOT_REPLICAS` | `1` *(`0` pour lancer LibreTranslate seul)* |

4. Cliquer sur **Deploy the stack**.

> **Note Portainer :** les variables définies dans l'interface Portainer remplacent le fichier `.env`. Ne pas committer de `.env` contenant un vrai token dans le dépôt.

---

## Migration vers un nouvel hôte (ex. Unraid)

Le bot est sans état : seuls les modèles LibreTranslate sont stockés, et ils se re-téléchargent. Le point critique est de **ne jamais faire tourner deux bots avec le même token** (chaque réaction serait traduite deux fois).

1. **Préparer le stockage** (terminal Unraid) — l'image LibreTranslate tourne en UID/GID 1032 :
   ```bash
   mkdir -p /mnt/user/appdata/babel-bot/libretranslate
   chown -R 1032:1032 /mnt/user/appdata/babel-bot/libretranslate
   ```
2. **Pré-chauffer** : créer le stack Portainer (Repository) avec le même `DISCORD_TOKEN`, `LT_DATA_PATH=/mnt/user/appdata/babel-bot/libretranslate` et `BOT_REPLICAS=0`. Attendre que `libretranslate` soit `healthy` (téléchargement des modèles, 2–5 min).
3. **Basculer** :
   - ancien hôte : désactiver GitOps sur le stack, puis **Stop** (ne pas supprimer — c'est le rollback) ;
   - nouvel hôte : `BOT_REPLICAS=1` → **Update the stack** ; vérifier les logs et tester une réaction drapeau.
4. **Rollback** : stopper le stack du nouvel hôte, redémarrer l'ancien.
5. **Décommission** : après une semaine sans incident, supprimer le stack de l'ancien hôte.

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
| `TRANSLATE_TIMEOUT` | Non | Timeout des requêtes de traduction en secondes (défaut : `60.0`) |
| `TRANSLATE_CONCURRENCY` | Non | Requêtes simultanées max vers LibreTranslate (défaut : `1`) |
| `LT_DATA_PATH` | Non | Chemin hôte des modèles LibreTranslate (défaut : volume nommé `libretranslate_data`) |
| `BOT_REPLICAS` | Non | `1` = bot actif, `0` = LibreTranslate seul (défaut : `1`). Pas d'autre valeur : les conteneurs ont un `container_name` fixe (`babel-bot`, `babel-bot-libretranslate`) |

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
