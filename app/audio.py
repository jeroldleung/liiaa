import base64
import os
from io import BytesIO
from typing import Generator

import numpy as np
import opuslib
import soundfile as sf
from funasr import AutoModel
from funasr.utils.postprocess_utils import rich_transcription_postprocess
from pydub import AudioSegment

cwd = os.getcwd()
asr_model = AutoModel(model=os.path.join(cwd, "models/asr"), disable_update=True)
vad_model = AutoModel(model=os.path.join(cwd, "models/vad"), disable_update=True)


def wav_to_opus(audio_str: str) -> Generator[bytes, None, None]:
    """Convert a base64-encoded wav audio string to an opus-encoded audio string."""
    wav_bytes = base64.b64decode(audio_str)  # decoded audio string to audio bytes
    audio_np = np.frombuffer(wav_bytes, dtype=np.int16)
    wav_buf = BytesIO()
    sf.write(wav_buf, audio_np, samplerate=24000, format="wav")
    audio = AudioSegment.from_file(wav_buf, format="wav")  # load wav data
    audio.set_channels(1).set_frame_rate(24000)
    encoder = opuslib.Encoder(24000, 1, opuslib.APPLICATION_AUDIO)

    frame_duration = 60  # 60ms per frame
    frame_size = int(24000 * frame_duration / 1000)
    raw_data = audio.raw_data

    for i in range(0, len(raw_data), frame_size * 2):
        chunk = raw_data[i : i + frame_size * 2]
        if len(chunk) < frame_size * 2:
            chunk += b"\x00" * (frame_size * 2 - len(chunk))
        np_frame = np.frombuffer(chunk, dtype=np.int16)
        opus_data = encoder.encode(np_frame.tobytes(), frame_size)
        yield opus_data


def opus_to_pcm(opus_bytes: bytes) -> bytes:
    decoder = opuslib.Decoder(16000, 1)  # 16000 sample rate and 1 channel
    pcm_frame = decoder.decode(opus_bytes, 960)
    return pcm_frame


def audio_to_text(audio_bytes: bytes) -> str:
    res = asr_model.generate(input=audio_bytes)
    text = rich_transcription_postprocess(res[0]["text"])
    return text


cache = {}


def is_silence(opus_bytes: bytes) -> bool:
    pcm_frame = opus_to_pcm(opus_bytes)
    res = vad_model.generate(
        input=pcm_frame,
        cache=cache,
        chunk_size=60,
        max_single_segment_time=500,
    )
    val = res[0]["value"]
    if len(val) > 0:
        if val[0][0] > 0 and val[0][1] == -1:
            print(res)
            return True
