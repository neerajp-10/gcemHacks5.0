"""Twilio SMS & Voice Call service for Earthworm agromet advisories.

Provides both real Twilio API dispatch (when TWILIO credentials are configured)
and realistic offline/development simulation with speech readout and TwiML generation.
Supports all 7 Indian agrarian languages: English, Kannada, Hindi, Telugu, Tamil, Marathi, and Bengali.
"""

import math
import re
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional
import xml.sax.saxutils as saxutils

import httpx

from app.config import settings

_TTS_CACHE: Dict[str, bytes] = {}


# Mapping of application language codes to Twilio / Amazon Polly / Google TTS voice attributes
TWILIO_VOICE_CONFIG: Dict[str, Dict[str, str]] = {
    "en": {
        "bcp47": "en-IN",
        "voice": "Polly.Aditi",
        "name": "English (Indian)",
    },
    "kn": {
        "bcp47": "kn-IN",
        "voice": "Google.kn-IN-Standard-A",
        "name": "Kannada (ಕನ್ನಡ)",
    },
    "hi": {
        "bcp47": "hi-IN",
        "voice": "Polly.Aditi",
        "name": "Hindi (हिन्दी)",
    },
    "te": {
        "bcp47": "te-IN",
        "voice": "Google.te-IN-Standard-A",
        "name": "Telugu (తెలుగు)",
    },
    "ta": {
        "bcp47": "ta-IN",
        "voice": "Google.ta-IN-Standard-A",
        "name": "Tamil (தமிழ்)",
    },
    "mr": {
        "bcp47": "mr-IN",
        "voice": "Google.mr-IN-Standard-A",
        "name": "Marathi (मराठी)",
    },
    "bn": {
        "bcp47": "bn-IN",
        "voice": "Google.bn-IN-Standard-A",
        "name": "Bengali (বাংলা)",
    },
}


def get_voice_config(language: str) -> Dict[str, str]:
    """Retrieve Twilio voice parameters for the given language."""
    lang_clean = language.lower()
    return TWILIO_VOICE_CONFIG.get(lang_clean, TWILIO_VOICE_CONFIG["en"])


def generate_twiml(script_text: str, language: str = "en") -> str:
    """Generate standard TwiML response XML for programmable voice advisories."""
    voice_info = get_voice_config(language)
    safe_text = saxutils.escape(script_text)
    return (
        f'<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<Response>\n'
        f'    <Say voice="{voice_info["voice"]}" language="{voice_info["bcp47"]}">'
        f'{safe_text}'
        f'</Say>\n'
        f'</Response>'
    )


def send_sms(to_number: str, message_body: str, language: str = "en") -> Dict[str, Any]:
    """Send an SMS advisory via Twilio API or simulate dispatch if unconfigured."""
    clean_to = to_number.strip()
    if not clean_to.startswith("+"):
        # Auto-prefix India ISD code if not provided
        clean_to = "+91" + clean_to.lstrip("0")

    char_count = len(message_body)
    segment_count = math.ceil(char_count / 160) if char_count > 0 else 1

    # Check if real Twilio credentials are configured
    if settings.is_twilio_configured:
        try:
            from twilio.rest import Client

            client = Client(settings.twilio_account_sid, settings.twilio_auth_token)
            msg = client.messages.create(
                body=message_body,
                from_=settings.twilio_phone_number,
                to=clean_to,
            )
            return {
                "success": True,
                "mode": "live",
                "sid": msg.sid,
                "status": msg.status or "queued",
                "to": clean_to,
                "from": settings.twilio_phone_number,
                "body": message_body,
                "language": language,
                "char_count": char_count,
                "segments": segment_count,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "simulated": False,
            }
        except Exception as exc:
            # Graceful fallback to simulation on Twilio API authentication/network error
            return {
                "success": False,
                "mode": "error_fallback",
                "error": str(exc),
                "sid": f"SMsim_{uuid.uuid4().hex[:24]}",
                "status": "simulation_fallback",
                "to": clean_to,
                "from": settings.twilio_phone_number or "+1800EARTHWORM",
                "body": message_body,
                "language": language,
                "char_count": char_count,
                "segments": segment_count,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "simulated": True,
            }

    # Realistic Twilio Simulation Mode
    sim_sid = f"SM{uuid.uuid4().hex[:32]}"
    return {
        "success": True,
        "mode": "simulation",
        "sid": sim_sid,
        "status": "delivered",
        "to": clean_to,
        "from": "+1800EARTHWORM",
        "body": message_body,
        "language": language,
        "char_count": char_count,
        "segments": segment_count,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "simulated": True,
    }


def place_voice_call(to_number: str, script_text: str, language: str = "en") -> Dict[str, Any]:
    """Place an IVR voice readout call via Twilio API or simulate dispatch if unconfigured."""
    clean_to = to_number.strip()
    if not clean_to.startswith("+"):
        clean_to = "+91" + clean_to.lstrip("0")

    voice_info = get_voice_config(language)
    twiml_xml = generate_twiml(script_text, language)
    est_duration_sec = max(15, round(len(script_text) / 14))

    # Check if real Twilio credentials are configured
    if settings.is_twilio_configured:
        try:
            from twilio.rest import Client

            client = Client(settings.twilio_account_sid, settings.twilio_auth_token)
            call = client.calls.create(
                to=clean_to,
                from_=settings.twilio_phone_number,
                twiml=twiml_xml,
            )
            return {
                "success": True,
                "mode": "live",
                "sid": call.sid,
                "status": call.status or "queued",
                "to": clean_to,
                "from": settings.twilio_phone_number,
                "script": script_text,
                "language": language,
                "voice_name": voice_info["name"],
                "voice_engine": voice_info["voice"],
                "twiml": twiml_xml,
                "est_duration_sec": est_duration_sec,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "simulated": False,
            }
        except Exception as exc:
            return {
                "success": False,
                "mode": "error_fallback",
                "error": str(exc),
                "sid": f"CAsim_{uuid.uuid4().hex[:24]}",
                "status": "simulation_fallback",
                "to": clean_to,
                "from": settings.twilio_phone_number or "+1800EARTHWORM",
                "script": script_text,
                "language": language,
                "voice_name": voice_info["name"],
                "voice_engine": voice_info["voice"],
                "twiml": twiml_xml,
                "est_duration_sec": est_duration_sec,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "simulated": True,
            }

    # Realistic Twilio Voice Call Simulation Mode
    sim_sid = f"CA{uuid.uuid4().hex[:32]}"
    return {
        "success": True,
        "mode": "simulation",
        "sid": sim_sid,
        "status": "in-progress",
        "to": clean_to,
        "from": "+1800EARTHWORM",
        "script": script_text,
        "language": language,
        "voice_name": voice_info["name"],
        "voice_engine": voice_info["voice"],
        "twiml": twiml_xml,
        "est_duration_sec": est_duration_sec,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "simulated": True,
    }


def synthesize_speech(text: str, language: str = "en") -> bytes:
    """Synthesize high-fidelity natural neural human speech audio for Indian languages.
    
    Splits text into natural clause chunks and streams crystal-clear native MP3 audio.
    """
    cache_key = f"{language.lower()}:{text.strip()}"
    if cache_key in _TTS_CACHE:
        return _TTS_CACHE[cache_key]

    lang_map = {
        "en": "en",
        "kn": "kn",
        "hi": "hi",
        "te": "te",
        "ta": "ta",
        "mr": "mr",
        "bn": "bn",
    }
    target_lang = lang_map.get(language.lower(), "en")

    # Split text into natural sentence / clause chunks <= 140 chars
    parts = re.split(r'([.?!।\n]+)', text)
    chunks = []
    curr = ""
    for p in parts:
        if len(curr) + len(p) < 140:
            curr += p
        else:
            if curr.strip():
                chunks.append(curr.strip())
            curr = p
    if curr.strip():
        chunks.append(curr.strip())

    combined_audio = b""
    with httpx.Client(timeout=15.0, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}) as client:
        for chunk in chunks:
            if not chunk:
                continue
            try:
                r = client.get(
                    f"https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&tl={target_lang}&q={chunk}"
                )
                if r.status_code == 200:
                    combined_audio += r.content
            except Exception:
                pass

    if combined_audio:
        _TTS_CACHE[cache_key] = combined_audio
    return combined_audio

