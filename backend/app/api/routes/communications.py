"""FastAPI routes for Twilio SMS & Voice Call communication."""

from typing import Optional
from fastapi import APIRouter, HTTPException, Query, Response
from pydantic import BaseModel, Field

from app.api.routes.farms import get_farm_advisory
from app.config import settings
from app.services import twilio_service

router = APIRouter(prefix="/communications", tags=["Communications"])


class SmsRequest(BaseModel):
    to: str = Field(default="+919876543210", description="Recipient phone number with country code")
    farm_id: Optional[str] = Field(default="mandya", description="Farm identifier (e.g. mandya, ludhiana)")
    language: str = Field(default="en", description="Language code: en, kn, hi, te, ta, mr, bn")
    message: Optional[str] = Field(default=None, description="Custom SMS message body (auto-derived if omitted)")


class VoiceCallRequest(BaseModel):
    to: str = Field(default="+919876543210", description="Recipient phone number with country code")
    farm_id: Optional[str] = Field(default="mandya", description="Farm identifier (e.g. mandya, ludhiana)")
    language: str = Field(default="en", description="Language code: en, kn, hi, te, ta, mr, bn")
    script: Optional[str] = Field(default=None, description="Custom Voice transcript (auto-derived if omitted)")


@router.get("/status", summary="Get Twilio Provider Configuration Status")
def get_twilio_status():
    """Check whether Twilio credentials are live-configured or in simulation mode."""
    return {
        "twilio_configured": settings.is_twilio_configured,
        "mode": "live" if settings.is_twilio_configured else "simulation",
        "phone_number": settings.twilio_phone_number or "+1800EARTHWORM",
        "supported_languages": list(twilio_service.TWILIO_VOICE_CONFIG.keys()),
        "speech_engines": {
            lang: info["voice"] for lang, info in twilio_service.TWILIO_VOICE_CONFIG.items()
        },
    }


@router.post("/sms", summary="Send or Simulate Twilio Advisory SMS")
def dispatch_sms(payload: SmsRequest):
    """Dispatch an SMS advisory in the selected language to a farmer mobile number."""
    body = payload.message
    if not body:
        farm_id = payload.farm_id or "mandya"
        adv = get_farm_advisory(farm_id=farm_id, language=payload.language)
        body = adv.sms_preview

    result = twilio_service.send_sms(
        to_number=payload.to,
        message_body=body,
        language=payload.language,
    )
    return result


@router.post("/call", summary="Place or Simulate Twilio Advisory Voice Call")
def dispatch_voice_call(payload: VoiceCallRequest):
    """Place an automated IVR voice advisory call in the selected Indian language."""
    script = payload.script
    if not script:
        farm_id = payload.farm_id or "mandya"
        adv = get_farm_advisory(farm_id=farm_id, language=payload.language)
        script = adv.voice_transcript

    result = twilio_service.place_voice_call(
        to_number=payload.to,
        script_text=script,
        language=payload.language,
    )
    return result


@router.get("/twiml", summary="Twilio Webhook: Generate TwiML Voice XML")
def get_twiml_endpoint(
    script: str = Query(default="Welcome to Earthworm Agri Advisory.", description="Text to speak"),
    language: str = Query(default="en", description="Language code: en, kn, hi, te, ta, mr, bn"),
):
    """Return raw TwiML XML for incoming or outgoing Twilio voice webhooks."""
    xml_content = twilio_service.generate_twiml(script, language)
    return Response(content=xml_content, media_type="application/xml")


@router.get("/speak", summary="Stream High-Fidelity Natural Human Advisory Audio")
def stream_advisory_audio(
    farm_id: Optional[str] = Query(default="mandya", description="Farm identifier"),
    language: str = Query(default="en", description="Language code: en, kn, hi, te, ta, mr, bn"),
    text: Optional[str] = Query(default=None, description="Custom text to speak"),
):
    """Synthesize and stream natural human voice MP3 in the farmer's regional language."""
    script = text
    if not script:
        target_farm = farm_id or "mandya"
        adv = get_farm_advisory(farm_id=target_farm, language=language)
        script = adv.voice_transcript or adv.description

    audio_bytes = twilio_service.synthesize_speech(script, language)
    if not audio_bytes:
        raise HTTPException(status_code=500, detail="Audio synthesis failed.")

    return Response(
        content=audio_bytes,
        media_type="audio/mpeg",
        headers={
            "Cache-Control": "public, max-age=86400",
            "Content-Disposition": f'inline; filename="advisory_{language}.mp3"',
        },
    )

