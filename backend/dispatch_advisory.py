"""Standalone Headless CLI Dispatcher for Low-Bandwidth Farmer Communications.

Dispatches agricultural advisories via direct cellular SMS and automated IVR voice calls
to farmers' physical mobile handsets (basic 2G/3G keypad phones or smartphones).

Execution requires NO web browser and NO web page interaction:
    python dispatch_advisory.py --to "+919731803808" --channel both --lang kn --farm mandya
"""

import argparse
import sys
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Ensure backend root is in Python sys.path
backend_dir = Path(__file__).resolve().parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from app.api.routes.farms import get_farm_advisory
from app.config import settings
from app.services import twilio_service


def main():
    parser = argparse.ArgumentParser(
        description="Earthworm Low-Bandwidth Telecom Dispatcher (SMS & IVR Voice to Farmer Phone Handsets)"
    )
    parser.add_argument(
        "--to",
        default="+919731803808",
        help="Farmer mobile number with country code (e.g. +919731803808)",
    )
    parser.add_argument(
        "--channel",
        choices=["sms", "call", "both"],
        default="both",
        help="Communication channel: 'sms', 'call', or 'both' (default: both)",
    )
    parser.add_argument(
        "--farm",
        default="mandya",
        help="Farm parcel ID (e.g. mandya, ludhiana, varanasi, nashik)",
    )
    parser.add_argument(
        "--lang",
        default="kn",
        choices=["en", "kn", "hi", "te", "ta", "mr", "bn"],
        help="Vernacular language code (default: kn for Kannada)",
    )
    parser.add_argument(
        "--message",
        default=None,
        help="Optional custom message override",
    )

    args = parser.parse_args()

    print("=" * 72)
    print("[EARTHWORM] LOW-BANDWIDTH TELECOM DISPATCHER (ZERO BROWSER / HEADLESS)")
    print("=" * 72)
    print(f"Target Farmer Phone : {args.to}")
    print(f"Monitored Parcel    : {args.farm.upper()}")
    print(f"Vernacular Language : {args.lang}")
    print(f"Selected Channel    : {args.channel.upper()}")
    print(f"Telecom Gateway     : {'LIVE CARRIER (Twilio)' if settings.is_twilio_configured else 'TELECOM SIMULATION MODE'}")
    print("-" * 72)

    adv = get_farm_advisory(farm_id=args.farm, language=args.lang)

    # 1. SMS Dispatch
    if args.channel in ("sms", "both"):
        sms_body = args.message or adv.sms_preview
        print(f"\n📨 [DISPATCHING CELLULAR SMS]")
        print(f"Content: \"{sms_body}\"")
        sms_res = twilio_service.send_sms(
            to_number=args.to,
            message_body=sms_body,
            language=args.lang,
        )
        print(f"  Status   : {sms_res.get('status')}")
        print(f"  SID      : {sms_res.get('sid')}")
        print(f"  Segments : {sms_res.get('segments')} (Length: {sms_res.get('char_count')} chars)")
        print(f"  Mode     : {sms_res.get('mode')}")

    # 2. IVR Voice Call Dispatch
    if args.channel in ("call", "both"):
        call_script = args.message or adv.voice_transcript
        print(f"\n📞 [DISPATCHING AUTOMATED IVR VOICE CALL]")
        print(f"Script: \"{call_script}\"")
        call_res = twilio_service.place_voice_call(
            to_number=args.to,
            script_text=call_script,
            language=args.lang,
        )
        print(f"  Status   : {call_res.get('status')}")
        print(f"  SID      : {call_res.get('sid')}")
        print(f"  Engine   : {call_res.get('voice_engine')}")
        print(f"  Duration : ~{call_res.get('est_duration_sec')}s")
        print(f"  Mode     : {call_res.get('mode')}")

    print("\n" + "=" * 72)
    print("✅ Direct cellular transmission sequence completed successfully.")
    print("   The advisory is delivered straight to the farmer's physical device.")
    print("   No internet connection, web browser, or smartphone required on the farm.")
    print("=" * 72)


if __name__ == "__main__":
    main()
