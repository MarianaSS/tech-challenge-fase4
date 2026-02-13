from moviepy.editor import VideoFileClip
from pathlib import Path

def extract_wav_from_video(video_path: str, out_wav_path: str) -> str:
    Path(out_wav_path).parent.mkdir(parents=True, exist_ok=True)

    clip = VideoFileClip(video_path)
    audio = clip.audio
    if audio is None:
        raise RuntimeError("O vídeo não possui faixa de áudio.")

    # wav PCM padrão
    audio.write_audiofile(out_wav_path, fps=16000, nbytes=2, codec="pcm_s16le")
    clip.close()
    return out_wav_path
