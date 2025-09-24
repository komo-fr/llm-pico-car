import os
import shutil
import tempfile

import certifi
from faster_whisper import WhisperModel
from langsmith import traceable

os.environ["SSL_CERT_FILE"] = certifi.where()

print("Whisperモデルを読み込み中...")
model_size = "tiny"
model = WhisperModel(model_size, device="cpu", compute_type="float32")


@traceable(name="transcribe")
def transcribe(audio_file) -> tuple[bool, str]:
    if audio_file is None:
        return False, "音声ファイルがありません"

    if not isinstance(audio_file, (str, bytes, bytearray)):
        print(type(audio_file))
        return False, "無効な音声ファイルです"

    if isinstance(audio_file, str):
        segments, _ = model.transcribe(audio_file, language="ja")
    else:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            if hasattr(audio_file, "read"):
                tmp_file.write(audio_file.read())
            else:
                shutil.copy2(audio_file, tmp_file.name)
            tmp_path = tmp_file.name
            segments, _ = model.transcribe(tmp_path, language="ja")

    return True, "".join([segment.text for segment in segments])
