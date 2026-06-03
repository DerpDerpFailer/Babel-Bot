import os
import logging
import asyncio
import discord
import httpx
from discord.ext import commands

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger(__name__)

# Emoji flag → ISO 639-1 language code
EMOJI_TO_LANG: dict[str, str] = {
    "🇫🇷": "fr",
    "🇬🇧": "en",
    "🇺🇸": "en",
    "🇩🇪": "de",
    "🇪🇸": "es",
    "🇮🇹": "it",
    "🇵🇹": "pt",
    "🇧🇷": "pt",
    "🇳🇱": "nl",
    "🇯🇵": "ja",
    "🇨🇳": "zh",
    "🇷🇺": "ru",
    "🇦🇷": "es",
    "🇰🇷": "ko",
    "🇸🇦": "ar",
    "🇹🇷": "tr",
    "🇵🇱": "pl",
    "🇸🇪": "sv",
    "🇩🇰": "da",
    "🇫🇮": "fi",
    "🇬🇷": "el",
    "🇨🇿": "cs",
    "🇷🇴": "ro",
    "🇭🇺": "hu",
    "🇺🇦": "uk",
}

LIBRETRANSLATE_URL = os.environ["LIBRETRANSLATE_URL"].rstrip("/")
LIBRETRANSLATE_API_KEY = os.environ.get("LIBRETRANSLATE_API_KEY", "")
DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]


intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True

bot = commands.Bot(command_prefix="!", intents=intents)


async def detect_and_translate(text: str, target_lang: str) -> tuple[str, str]:
    """Return (detected_source_lang, translated_text). Raises on error."""
    payload: dict = {"q": text, "source": "auto", "target": target_lang, "format": "text"}
    if LIBRETRANSLATE_API_KEY:
        payload["api_key"] = LIBRETRANSLATE_API_KEY

    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.post(f"{LIBRETRANSLATE_URL}/translate", json=payload)
        response.raise_for_status()
        data = response.json()

    translated = data["translatedText"]
    detected = data.get("detectedLanguage", {}).get("language", "?")
    return detected, translated


async def wait_for_libretranslate(delay: float = 10.0) -> None:
    """Block indefinitely until LibreTranslate /languages endpoint is reachable."""
    attempt = 0
    while True:
        attempt += 1
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                r = await client.get(f"{LIBRETRANSLATE_URL}/languages")
                if r.status_code == 200:
                    log.info("LibreTranslate is ready.")
                    return
        except Exception:
            pass
        log.info("Waiting for LibreTranslate… (attempt %d)", attempt)
        await asyncio.sleep(delay)


@bot.event
async def on_ready() -> None:
    log.info("Logged in as %s (id=%s)", bot.user, bot.user.id)


@bot.event
async def on_reaction_add(reaction: discord.Reaction, user: discord.User | discord.Member) -> None:
    # Ignore reactions from bots (including ourselves)
    if user.bot:
        return

    emoji = str(reaction.emoji)
    target_lang = EMOJI_TO_LANG.get(emoji)
    if target_lang is None:
        return

    message = reaction.message

    # Ignore bot messages
    if message.author.bot:
        return

    content = message.content.strip()
    if not content:
        return

    try:
        detected, translated = await detect_and_translate(content, target_lang)
    except Exception as exc:
        log.error("Translation failed: %s", exc)
        await message.channel.send(
            f"⚠️ Translation error: could not reach the translation service.",
            reference=message,
            mention_author=False,
        )
        return

    # Skip if source and target are the same language
    if detected == target_lang:
        return

    embed = discord.Embed(
        description=translated,
        color=discord.Color.blurple(),
    )
    embed.set_author(
        name=f"{emoji}  {detected.upper()} → {target_lang.upper()}",
        icon_url=user.display_avatar.url,
    )
    embed.set_footer(text=f"Requested by {user.display_name} · Powered by LibreTranslate")

    await message.channel.send(embed=embed, reference=message, mention_author=False)


async def main() -> None:
    await wait_for_libretranslate()
    await bot.start(DISCORD_TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
