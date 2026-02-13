from __future__ import annotations

from pathlib import Path
from typing import Dict, Any, List, Optional

import speech_recognition as sr
from pydub import AudioSegment


def extract_audio_features(
    video_path: Optional[str] = None,
    audio_path: Optional[str] = None,
    out_wav_path: str = "data/audios/extracted.wav",
    language: str = "en-US",
    chunk_ms: int = 4000,
    chunk_overlap_ms: int = 500,
    gain_db: int = 6,
) -> Dict[str, Any]:
    """
    Extrai e transcreve áudio para uso no pipeline multimodal.

    - Se audio_path for fornecido: usa diretamente esse WAV.
    - Senão, se video_path for fornecido: extrai áudio do vídeo usando MoviePy para out_wav_path.

    Depois:
    - normaliza + aplica ganho leve
    - divide em chunks por tempo
    - transcreve cada chunk via SpeechRecognition (Google Web Speech)

    Retorna um dict com:
      - wav_path
      - language
      - transcript
      - chunks_transcript
      - num_chunks
      - audio_dbfs
    """
    if not audio_path and not video_path:
        raise ValueError("Você precisa passar audio_path (WAV) ou video_path (MP4).")

    # 1) Definir qual WAV vamos usar
    if audio_path:
        wav_to_use = audio_path
    else:
        # Extrair do vídeo para WAV
        Path(out_wav_path).parent.mkdir(parents=True, exist_ok=True)

        # Import aqui pra não obrigar MoviePy quando audio_path é usado
        from moviepy.editor import VideoFileClip

        clip = VideoFileClip(video_path)  # type: ignore[arg-type]
        if clip.audio is None:
            clip.close()
            raise RuntimeError("O vídeo não possui faixa de áudio.")

        clip.audio.write_audiofile(
            out_wav_path,
            fps=16000,
            nbytes=2,
            codec="pcm_s16le",
            verbose=False,
            logger=None,
        )
        clip.close()
        wav_to_use = out_wav_path

    wav_path_obj = Path(wav_to_use)
    if not wav_path_obj.exists():
        raise FileNotFoundError(f"WAV não encontrado: {wav_to_use}")

    # 2) Carregar WAV e pré-processar (ajuda com fala baixa/ruído)
    audio = AudioSegment.from_wav(str(wav_path_obj))
    audio = audio.normalize()
    if gain_db:
        audio = audio + gain_db

    # 3) Chunking por tempo fixo
    recognizer = sr.Recognizer()

    tmp_dir = Path("results/audio_outputs")
    tmp_dir.mkdir(parents=True, exist_ok=True)

    chunk_texts: List[str] = []
    num_chunks = 0

    step = max(500, chunk_ms - chunk_overlap_ms)
    for start in range(0, len(audio), step):
        piece = audio[start:start + chunk_ms]
        if len(piece) < 1200:
            continue

        # filtro simples: evita mandar “quase silêncio”
        if piece.rms < 200:
            continue

        num_chunks += 1
        chunk_path = tmp_dir / f"chunk_{num_chunks:03d}.wav"
        piece.export(chunk_path, format="wav")

        with sr.AudioFile(str(chunk_path)) as source:
            # Ajusta ruído ambiente (pequeno trecho) e depois reconhece
            recognizer.adjust_for_ambient_noise(source, duration=0.2)
            audio_data = recognizer.record(source)

        try:
            text = recognizer.recognize_google(audio_data, language=language).strip()
        except sr.UnknownValueError:
            text = ""
        except sr.RequestError as e:
            raise RuntimeError(f"Erro SpeechRecognition/Google: {e}") from e

        if text:
            chunk_texts.append(text)

    transcript = " ".join(chunk_texts).strip()

    return {
        "wav_path": str(wav_path_obj),
        "language": language,
        "transcript": transcript,
        "chunks_transcript": chunk_texts,
        "num_chunks": num_chunks,
        "audio_dbfs": float(audio.dBFS),
        "used_input": "audio_path" if audio_path else "video_path",
    }
