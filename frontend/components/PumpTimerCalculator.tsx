import React, { useState, useMemo } from 'react';

export interface FarmMetadata {
  parcelId: string;
  location: string;
  crop: string;
  totalHectares: number;
  waterDeficitMm: number;
}

export interface PumpTimerCalculatorProps {
  farm?: FarmMetadata;
  activeLanguage?: string;
  onSendSms?: (payload: string) => void;
  onClose?: () => void;
  isModal?: boolean;
}

const DISCHARGE_LPM: Record<number, number> = {
  3: 2700,
  5: 4400,
  7.5: 6500,
};

const EFFICIENCY_FACTORS: Record<string, number> = {
  drip: 0.85,
  channel: 1.15,
};

export const PumpTimerCalculator: React.FC<PumpTimerCalculatorProps> = ({
  farm = {
    parcelId: 'Parcel #142/A',
    location: 'Mandya, Karnataka',
    crop: 'Paddy (Sona Masoori)',
    totalHectares: 1.85,
    waterDeficitMm: 8.5,
  },
  activeLanguage = 'en',
  onSendSms,
  onClose,
  isModal = false,
}) => {
  // Interactive Controls State
  const [targetArea, setTargetArea] = useState<'stress' | 'full'>('stress');
  const [pumpHp, setPumpHp] = useState<number>(5);
  const [deliveryMethod, setDeliveryMethod] = useState<'drip' | 'channel'>('drip');
  const [isSpeaking, setIsSpeaking] = useState<boolean>(false);

  // Computations
  const {
    activeHectares,
    requiredLiters,
    runtimeMinutes,
    formattedRuntime,
    floodLiters,
    waterSavedLiters,
    formattedWaterSaved,
    pctWaterSaved,
    smsPayload,
  } = useMemo(() => {
    const areaMultiplier = targetArea === 'stress' ? 0.25 : 1.0;
    const activeHa = Math.max(0.1, farm.totalHectares * areaMultiplier);
    const effFactor = EFFICIENCY_FACTORS[deliveryMethod] || 0.85;
    const discharge = DISCHARGE_LPM[pumpHp] || 4400;

    // 1 ha = 10,000 m2; 1 mm depth over 1 m2 = 1 Liter.
    const reqLiters = Math.round(activeHa * 10000 * farm.waterDeficitMm * effFactor);
    const runtimeMins = Math.max(5, Math.round(reqLiters / discharge));

    let fmtRuntime = `${runtimeMins} mins`;
    if (runtimeMins >= 60) {
      const hrs = Math.floor(runtimeMins / 60);
      const remainingMins = runtimeMins % 60;
      fmtRuntime = remainingMins > 0 ? `${hrs} hr ${remainingMins} mins` : `${hrs} hr`;
    }

    // Traditional Flood Irrigation Comparison (45mm baseline over total hectares)
    const flood = Math.round(farm.totalHectares * 10000 * 45);
    const savedLiters = Math.max(0, flood - reqLiters);
    const pctSaved = Math.min(99, Math.max(10, Math.round((savedLiters / flood) * 100)));

    let fmtSaved = `${savedLiters.toLocaleString()} L`;
    if (savedLiters >= 1000000) {
      fmtSaved = `${(savedLiters / 1000000).toFixed(2)}M Liters`;
    } else if (savedLiters >= 1000) {
      fmtSaved = `${(savedLiters / 1000).toFixed(1)}k Liters`;
    }

    const areaLabel = targetArea === 'stress' ? 'Stress Zone (25%)' : 'Full Field';
    const payload = `[EARTHWORM] ${farm.location} ${farm.parcelId}: Run ${pumpHp}HP pump for ${fmtRuntime} (${areaLabel}) before 8:30 AM. Saves ${pctSaved}% water. Reply 1 when done.`;

    return {
      activeHectares: activeHa,
      requiredLiters: reqLiters,
      runtimeMinutes: runtimeMins,
      formattedRuntime: fmtRuntime,
      floodLiters: flood,
      waterSavedLiters: savedLiters,
      formattedWaterSaved: fmtSaved,
      pctWaterSaved: pctSaved,
      smsPayload: payload,
    };
  }, [farm, targetArea, pumpHp, deliveryMethod]);

  // Voice Speech Integration
  const handleHearVoice = () => {
    if (!('speechSynthesis' in window)) {
      alert('Speech synthesis is not supported in this browser.');
      return;
    }

    if (isSpeaking) {
      window.speechSynthesis.cancel();
      setIsSpeaking(false);
      return;
    }

    const areaName = targetArea === 'stress' ? 'stress zone' : 'entire field';
    let voiceText = `Earthworm irrigation advisory for ${farm.parcelId} in ${farm.location}. For your ${farm.crop}, turn on your ${pumpHp} horse power pump for ${formattedRuntime} on the ${areaName}. Complete irrigation before 8:30 AM to save ${pctWaterSaved} percent water.`;

    if (activeLanguage === 'kn') {
      voiceText = `ಅರ್ಥ್‌ವರ್ಮ್ ನೀರಾವರಿ ಸಲಹೆ. ${farm.location} ನ ${farm.parcelId} ಜಮೀನಿಗೆ ನಿಮ್ಮ ${pumpHp} ಎಚ್‌ಪಿ ಪಂಪ್ ಅನ್ನು ${formattedRuntime} ಚಲಾಯಿಸಿ. ಬೆಳಗ್ಗೆ 8:30 ರೊಳಗೆ ನೀರು ಹರಿಸಿ ${pctWaterSaved} ಪ್ರತಿಶತ ನೀರು ಉಳಿಸಿ.`;
    } else if (activeLanguage === 'hi') {
      voiceText = `अर्थवर्म सिंचाई सलाह। ${farm.location} के ${farm.parcelId} खेत के लिए, अपने ${pumpHp} एचपी पंप को ${formattedRuntime} चलाएं। सुबह 8:30 से पहले सिंचाई पूरी करें और ${pctWaterSaved} प्रतिशत पानी बचाएं।`;
    }

    const utterance = new SpeechSynthesisUtterance(voiceText);
    utterance.rate = 0.92;

    const voices = window.speechSynthesis.getVoices();
    const langPrefix = activeLanguage === 'kn' ? 'kn' : activeLanguage === 'hi' ? 'hi' : 'en';
    const matchedVoice = voices.find((v) => v.lang.startsWith(langPrefix) || v.lang.includes('IN'));
    if (matchedVoice) {
      utterance.voice = matchedVoice;
    }

    utterance.onend = () => setIsSpeaking(false);
    utterance.onerror = () => setIsSpeaking(false);

    setIsSpeaking(true);
    window.speechSynthesis.speak(utterance);
  };

  const handleSendSmsClick = () => {
    if (onSendSms) {
      onSendSms(smsPayload);
    } else {
      alert(`SMS Dispatched:\n\n${smsPayload}`);
    }
  };

  return (
    <div className="w-full bg-surface-container-lowest rounded-2xl border border-surface-variant p-4 sm:p-5 flex flex-col gap-4 shadow-sm text-on-surface">
      {/* Header */}
      <div className="flex items-start justify-between gap-3 border-b border-surface-variant pb-3">
        <div className="flex items-center gap-2.5 min-w-0">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-emerald-600 to-teal-800 text-white flex items-center justify-center shrink-0 shadow-sm">
            <span className="material-symbols-outlined text-[22px]">timer</span>
          </div>
          <div className="flex flex-col min-w-0">
            <div className="flex items-center gap-2 flex-wrap">
              <h3 className="text-sm sm:text-base font-bold text-on-surface tracking-tight truncate">
                Smart Pump Timer &amp; Water Savings
              </h3>
              <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-500/15 text-emerald-800 dark:text-emerald-300 font-mono">
                AI Precision
              </span>
            </div>
            <p className="text-[11px] text-secondary truncate">
              {farm.location} • {farm.parcelId} • {farm.crop} ({farm.totalHectares} Ha)
            </p>
          </div>
        </div>
        {isModal && onClose && (
          <button
            onClick={onClose}
            className="w-8 h-8 rounded-full bg-surface-container hover:bg-surface-variant text-on-surface flex items-center justify-center transition-colors cursor-pointer shrink-0"
            type="button"
            aria-label="Close Calculator"
          >
            <span className="material-symbols-outlined text-[18px]">close</span>
          </button>
        )}
      </div>

      {/* Interactive Controls Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
        {/* 1. Target Area */}
        <div className="flex flex-col gap-1.5 p-3 rounded-xl bg-surface-container-low border border-surface-variant/80">
          <label className="text-[11px] font-bold text-secondary uppercase tracking-wider flex items-center gap-1">
            <span className="material-symbols-outlined text-[14px] text-primary">crop_free</span>
            <span>Target Area</span>
          </label>
          <div className="grid grid-cols-2 gap-1 bg-surface-container rounded-lg p-0.5">
            <button
              type="button"
              onClick={() => setTargetArea('stress')}
              className={`py-1.5 px-2 text-[11px] font-bold rounded-md transition-all cursor-pointer truncate ${
                targetArea === 'stress'
                  ? 'bg-primary text-on-primary shadow-xs'
                  : 'text-on-surface hover:text-primary'
              }`}
            >
              Stress Zone (25%)
            </button>
            <button
              type="button"
              onClick={() => setTargetArea('full')}
              className={`py-1.5 px-2 text-[11px] font-bold rounded-md transition-all cursor-pointer truncate ${
                targetArea === 'full'
                  ? 'bg-primary text-on-primary shadow-xs'
                  : 'text-on-surface hover:text-primary'
              }`}
            >
              Full Field (100%)
            </button>
          </div>
          <span className="text-[10px] text-secondary">
            Active: <strong className="text-on-surface">{activeHectares.toFixed(2)} Ha</strong> (~
            {(activeHectares * 2.471).toFixed(1)} Acres)
          </span>
        </div>

        {/* 2. Pump Power (HP) */}
        <div className="flex flex-col gap-1.5 p-3 rounded-xl bg-surface-container-low border border-surface-variant/80">
          <label className="text-[11px] font-bold text-secondary uppercase tracking-wider flex items-center gap-1">
            <span className="material-symbols-outlined text-[14px] text-primary">bolt</span>
            <span>Pump Power (HP)</span>
          </label>
          <div className="grid grid-cols-3 gap-1 bg-surface-container rounded-lg p-0.5">
            {[3, 5, 7.5].map((hp) => (
              <button
                key={hp}
                type="button"
                onClick={() => setPumpHp(hp)}
                className={`py-1.5 px-1 text-[11px] font-bold rounded-md transition-all cursor-pointer text-center ${
                  pumpHp === hp
                    ? 'bg-primary text-on-primary shadow-xs'
                    : 'text-on-surface hover:text-primary'
                }`}
              >
                {hp} HP
              </button>
            ))}
          </div>
          <span className="text-[10px] text-secondary">
            Discharge: <strong className="text-on-surface">{DISCHARGE_LPM[pumpHp].toLocaleString()} L/min</strong>
          </span>
        </div>

        {/* 3. Delivery Method */}
        <div className="flex flex-col gap-1.5 p-3 rounded-xl bg-surface-container-low border border-surface-variant/80">
          <label className="text-[11px] font-bold text-secondary uppercase tracking-wider flex items-center gap-1">
            <span className="material-symbols-outlined text-[14px] text-primary">water</span>
            <span>Delivery Method</span>
          </label>
          <div className="grid grid-cols-2 gap-1 bg-surface-container rounded-lg p-0.5">
            <button
              type="button"
              onClick={() => setDeliveryMethod('drip')}
              className={`py-1.5 px-2 text-[11px] font-bold rounded-md transition-all cursor-pointer truncate ${
                deliveryMethod === 'drip'
                  ? 'bg-primary text-on-primary shadow-xs'
                  : 'text-on-surface hover:text-primary'
              }`}
            >
              Drip / Pipe
            </button>
            <button
              type="button"
              onClick={() => setDeliveryMethod('channel')}
              className={`py-1.5 px-2 text-[11px] font-bold rounded-md transition-all cursor-pointer truncate ${
                deliveryMethod === 'channel'
                  ? 'bg-primary text-on-primary shadow-xs'
                  : 'text-on-surface hover:text-primary'
              }`}
            >
              Channel / Furrow
            </button>
          </div>
          <span className="text-[10px] text-secondary">
            Efficiency: <strong className="text-on-surface">{deliveryMethod === 'drip' ? '85% (Optimal)' : '65% (Losses)'}</strong>
          </span>
        </div>
      </div>

      {/* 3 Summary Metric Cards Banner */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-2.5">
        {/* Recommended Runtime */}
        <div className="p-3.5 rounded-xl bg-surface-container-lowest border-2 border-emerald-500/30 flex flex-col justify-between shadow-xs">
          <div className="flex items-center justify-between">
            <span className="text-[11px] font-bold text-secondary uppercase tracking-wider">
              Recommended Runtime
            </span>
            <span className="material-symbols-outlined text-emerald-600 text-[18px]">timelapse</span>
          </div>
          <div className="my-1.5">
            <span className="text-2xl font-extrabold text-primary tracking-tight font-mono">
              {formattedRuntime}
            </span>
          </div>
          <span className="text-[10px] text-secondary">
            Net Need: <strong className="text-on-surface">{requiredLiters.toLocaleString()} L</strong>
          </span>
        </div>

        {/* Best Irrigation Window */}
        <div className="p-3.5 rounded-xl bg-surface-container-lowest border border-surface-variant flex flex-col justify-between shadow-xs">
          <div className="flex items-center justify-between">
            <span className="text-[11px] font-bold text-secondary uppercase tracking-wider">
              Best Window
            </span>
            <span className="material-symbols-outlined text-amber-500 text-[18px]">wb_twilight</span>
          </div>
          <div className="my-1.5">
            <span className="text-base sm:text-lg font-extrabold text-on-surface tracking-tight font-mono">
              06:00 AM – 08:30 AM
            </span>
          </div>
          <span className="text-[10px] text-emerald-700 dark:text-emerald-300 font-semibold">
            Avoids daytime evaporation (-32%)
          </span>
        </div>

        {/* Water Saved vs. Flood */}
        <div className="p-3.5 rounded-xl bg-surface-container-lowest border border-surface-variant flex flex-col justify-between shadow-xs">
          <div className="flex items-center justify-between">
            <span className="text-[11px] font-bold text-secondary uppercase tracking-wider">
              Water Saved vs. Flood
            </span>
            <span className="text-[10px] font-extrabold px-1.5 py-0.5 rounded-md bg-emerald-500/20 text-emerald-800 dark:text-emerald-300 font-mono">
              {pctWaterSaved}% Saved
            </span>
          </div>
          <div className="my-1.5">
            <span className="text-2xl font-extrabold text-emerald-600 tracking-tight font-mono">
              {formattedWaterSaved}
            </span>
          </div>
          <span className="text-[10px] text-secondary">
            Flood Base: <span className="line-through">{floodLiters.toLocaleString()} L</span>
          </span>
        </div>
      </div>

      {/* Monospace Compressed SMS Payload Box */}
      <div className="flex flex-col gap-1.5">
        <div className="flex items-center justify-between text-[11px]">
          <span className="font-bold text-secondary flex items-center gap-1">
            <span className="material-symbols-outlined text-[14px] text-primary">sms</span>
            <span>Compressed Low-Bandwidth SMS Payload</span>
          </span>
          <span
            className={`font-mono text-[10px] font-bold ${
              smsPayload.length <= 160 ? 'text-emerald-600' : 'text-amber-500'
            }`}
          >
            {smsPayload.length} / 160 chars
          </span>
        </div>
        <div className="bg-slate-900 rounded-xl p-3 font-mono text-[11px] sm:text-xs text-emerald-300 border border-emerald-500/30 leading-relaxed break-words select-all shadow-inner">
          {smsPayload}
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex flex-col sm:flex-row items-center gap-2 pt-1">
        <button
          type="button"
          onClick={handleSendSmsClick}
          className="w-full sm:flex-1 min-h-[46px] rounded-xl bg-primary text-on-primary font-bold text-xs sm:text-sm flex items-center justify-center gap-2 shadow-sm hover:bg-primary-container transition-all cursor-pointer"
        >
          <span className="material-symbols-outlined text-[18px]">send</span>
          <span>Send Pump Timer via SMS</span>
        </button>

        <button
          type="button"
          onClick={handleHearVoice}
          className="w-full sm:w-auto px-4 min-h-[46px] rounded-xl bg-surface-container hover:bg-surface-variant text-on-surface font-bold text-xs sm:text-sm flex items-center justify-center gap-2 transition-all cursor-pointer border border-surface-variant"
        >
          <span className="material-symbols-outlined text-[18px] text-primary">
            {isSpeaking ? 'stop_circle' : 'volume_up'}
          </span>
          <span>{isSpeaking ? 'Stop Audio' : 'Hear Voice Timer Alert'}</span>
        </button>
      </div>
    </div>
  );
};

export default PumpTimerCalculator;
