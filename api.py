from fastapi import FastAPI
from pydantic import BaseModel
from transformers import TFXLMRobertaForSequenceClassification, XLMRobertaTokenizer
import tensorflow as tf
import numpy as np
import json
import os

os.environ["CUDA_VISIBLE_DEVICES"] = ""

# Inisialisasi FastAPI
app = FastAPI()

# Load model + tokenizer dari Hugging Face (repo privat/public)
model_name = "Raihan2212/SensecheckCapstone"

# Load model
model = TFXLMRobertaForSequenceClassification.from_pretrained(model_name)
print(f"Model berhasil dimuat dari {model_name}")

# Load tokenizer
tokenizer = XLMRobertaTokenizer.from_pretrained(model_name)
print(f"Tokenizer berhasil dimuat dari {model_name}")

# Load label_map dari config.json di repo HF
config_path = os.path.join(model_name, "config.json")
try:
    from huggingface_hub import hf_hub_download
    config_file = hf_hub_download(repo_id=model_name, filename="config.json")
    with open(config_file, "r", encoding="utf-8") as f:
        config = json.load(f)
    label_map = config.get("label_map", {})
except Exception as e:
    print(f"Gagal memuat label_map dari config.json: {e}")
    label_map = {}

# Skema input data
class InputData(BaseModel):
    kategori: str
    gejala: str
    keparahan: str
    riwayat: str

# Endpoint prediksi
@app.post("/predict")
def predict(data: InputData):
    # Gabungkan input menjadi satu string
    input_text = f"{data.kategori}. {data.gejala}. Keparahan: {data.keparahan}. Riwayat: {data.riwayat}"

    # Tokenisasi
    inputs = tokenizer(
        input_text,
        max_length=128,
        padding="max_length",
        truncation=True,
        return_tensors="tf"
    )

    # Prediksi
    outputs = model(**inputs)
    logits = outputs.logits.numpy()
    pred_index = int(np.argmax(logits, axis=1)[0])
    confidence = float(np.max(tf.nn.softmax(logits)[0]))
    confidence_percent = round(confidence * 100, 2)

    # Ambil hasil diagnosis dan saran
    result = label_map.get(str(pred_index), {
        "diagnosis": "Tidak diketahui",
        "saran_penanganan": "Silakan konsultasi lebih lanjut dengan dokter."
    })

    return {
        "diagnosis": f"{result['diagnosis']} ({confidence_percent}%)",
        "saran": result["saran_penanganan"],
        "confidence": confidence
    }

if __name__ == "__main__":
    import uvicorn
    
    # Tentukan host berdasarkan environment
    node_env = os.getenv("NODE_ENV", "development")
    host = "localhost" if node_env != "production" else "0.0.0.0"
    
    uvicorn.run("api:app", host=host, port=8000, reload=True)