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


@router.post("/incoming-call", summary="Twilio Inbound IVR Voice Helpline / Missed Call Callback")
def incoming_voice_call_webhook(
    From: Optional[str] = Query(default=None, description="Caller phone number"),
    farm_id: Optional[str] = Query(default="mandya", description="Default farm ID"),
    language: Optional[str] = Query(default="kn", description="Default language"),
):
    """Twilio webhook handler for inbound farmer calls.
    
    Allows smallholder farmers with basic feature phones to dial the helpline
    and receive an instant automated audio advisory in their native language,
    without requiring a smartphone, mobile app, or web browser.
    """
    target_farm = farm_id or "mandya"
    target_lang = language or "kn"
    adv = get_farm_advisory(farm_id=target_farm, language=target_lang)
    script_text = adv.voice_transcript or adv.description

    voice_xml = twilio_service.generate_twiml(script_text, target_lang)
    return Response(content=voice_xml, media_type="application/xml")


@router.post("/incoming-sms", summary="Twilio Inbound SMS Advisory Helpline")
def incoming_sms_webhook(
    From: Optional[str] = Query(default=None, description="Sender phone number"),
    Body: Optional[str] = Query(default="", description="Inbound SMS text content"),
):
    """Twilio webhook handler for inbound farmer SMS queries.
    
    Farmers can text 'MANDYA', 'WEATHER', 'HELP', or regional language keywords
    to receive an instant 160-character localized advisory delivered straight to
    their basic phone's messaging inbox.
    """
    query_text = (Body or "").strip().lower()

    # Determine farm and language from query text
    target_farm = "mandya"
    target_lang = "kn"  # Default Kannada for Mandya farmers

    if "ludhiana" in query_text or "wheat" in query_text:
        target_farm = "ludhiana"
        target_lang = "hi"
    elif "varanasi" in query_text:
        target_farm = "varanasi"
        target_lang = "hi"
    elif "nashik" in query_text or "onion" in query_text:
        target_farm = "nashik"
        target_lang = "mr"

    if "english" in query_text or "en" in query_text.split():
        target_lang = "en"
    elif "hindi" in query_text or "hi" in query_text.split():
        target_lang = "hi"
    elif "kannada" in query_text or "kn" in query_text.split():
        target_lang = "kn"

    adv = get_farm_advisory(farm_id=target_farm, language=target_lang)
    reply_body = adv.sms_preview or adv.action

    twiml_sms_xml = twilio_service.generate_twiml_sms(reply_body)
    return Response(content=twiml_sms_xml, media_type="application/xml")


class LowBandwidthDispatchRequest(BaseModel):
    to: str = Field(default="+919731803808", description="Farmer mobile number with country code")
    farm_id: str = Field(default="mandya", description="Farm parcel identifier")
    language: str = Field(default="kn", description="Language code: en, kn, hi, te, ta, mr, bn")
    channel: str = Field(default="both", description="Delivery channel: 'sms', 'call', or 'both'")
    custom_message: Optional[str] = Field(default=None, description="Optional custom advisory message")


@router.post("/dispatch-low-bandwidth", summary="Unified Low-Bandwidth Cellular Dispatch (Headless)")
def dispatch_low_bandwidth_advisory(payload: LowBandwidthDispatchRequest):
    """Headless cellular communication dispatcher for smallholder farmers.
    
    Directly dispatches real SMS and/or IVR voice phone calls over telecom networks
    (GSM/PSTN) to the farmer's physical phone number.
    Does NOT require a web browser, internet, or smartphone on the farmer's end.
    """
    adv = get_farm_advisory(farm_id=payload.farm_id, language=payload.language)
    sms_result = None
    call_result = None

    if payload.channel in ("sms", "both"):
        sms_text = payload.custom_message or adv.sms_preview
        sms_result = twilio_service.send_sms(
            to_number=payload.to,
            message_body=sms_text,
            language=payload.language,
        )

    if payload.channel in ("call", "both"):
        call_text = payload.custom_message or adv.voice_transcript
        call_result = twilio_service.place_voice_call(
            to_number=payload.to,
            script_text=call_text,
            language=payload.language,
        )

    return {
        "success": True,
        "farmer_phone": payload.to,
        "farm_id": payload.farm_id,
        "language": payload.language,
        "channel": payload.channel,
        "telecom_mode": "live_carrier" if settings.is_twilio_configured else "telecom_simulation",
        "low_bandwidth_notice": (
            "Delivered directly to farmer's mobile handset via cellular network (GSM/PSTN). "
            "Zero internet connection or web browser required on the recipient device."
        ),
        "sms_dispatch": sms_result,
        "voice_call_dispatch": call_result,
    }


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

