import os
import warnings

# Suppress TensorFlow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress all TF logs
os.environ['CUDA_VISIBLE_DEVICES'] = ''   # Disable CUDA completely
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0' # Disable oneDNN warnings

# Suppress Python warnings
warnings.filterwarnings('ignore')

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import TFXLMRobertaForSequenceClassification, XLMRobertaTokenizer
import tensorflow as tf
import numpy as np
import json

# Nonaktifkan GPU untuk menghindari masalah di Render
os.environ["CUDA_VISIBLE_DEVICES"] = ""

# Inisialisasi FastAPI
app = FastAPI()

# Tambahkan CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Izinkan semua origin
    allow_credentials=True,
    allow_methods=["*"],  # Izinkan semua HTTP methods
    allow_headers=["*"],  # Izinkan semua headers
)

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

# Health check endpoint
@app.get("/")
def read_root():
    return {"message": "FastAPI is running!", "status": "healthy"}

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
        "diagnosis": f"{result['diagnosis']}",
        "saran": result["saran_penanganan"],
        "confidence": f"{confidence_percent}%"
    }

if __name__ == "__main__":
    import uvicorn
    
    # Konfigurasi untuk Render
    port = int(os.getenv("PORT", 8000))
    host = "0.0.0.0"  # Wajib untuk Render
    
    uvicorn.run("api:app", host=host, port=port, reload=False)