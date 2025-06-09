# Model API - Mental Health Diagnosis System

API FastAPI untuk sistem diagnosis kesehatan mental menggunakan model XLM-RoBERTa dari Hugging Face.

## 📋 Prerequisites

- Python 3.8 atau lebih tinggi
- Git
- pip (Python package manager)

## 🚀 Installation & Setup

### 1. Clone Repository

```bash

git clone https://github.com/nfapriyanto/model-api.git

cd model-api

```

### 2. Create Virtual Environment

**Windows:**

```bash

python-mvenvmyenv

myenv\Scripts\activate

```

**macOS/Linux:**

```bash

python3-mvenvmyenv

source myenv/bin/activate

```

### 3. Install Dependencies

```bash

pip install -r requirements.txt

```

### 4. Run the Application

**Development Mode:**

```bash

uvicorn api:app --reload --host 0.0.0.0 --port 8000

```

**Atau jalankan langsung:**

```bash

python api.py

```

### 5. Test the API

Buka browser dan akses:

-**Health Check:** http://localhost:8000

-**API Documentation:** http://localhost:8000/docs

-**Alternative Docs:** http://localhost:8000/redoc

## 📡 API Endpoints

### GET `/`

Health check endpoint

```json

{

  "message": "FastAPI is running!",

  "status": "healthy"

}

```

### POST `/predict`

Prediksi diagnosis kesehatan mental

**Request Body:**

```json

{

  "kategori": "Kecemasan",

  "gejala": "Merasa gelisah dan sulit tidur",

  "keparahan": "Sedang",

  "riwayat": "Tidak ada riwayat keluarga"

}

```

**Response:**

```json

{

  "diagnosis": "Gangguan Kecemasan",

  "saran": "Konsultasi dengan psikolog dan terapi relaksasi",

  "confidence": "85.7%"

}

```

## 🧪 Testing dengan cURL

```bash

curl-XPOST"http://localhost:8000/predict"\

     -H "Content-Type: application/json" \

     -d'{

       "kategori": "Kecemasan",

       "gejala": "Merasa gelisah dan sulit tidur",

       "keparahan": "Sedang",

       "riwayat": "Tidak ada riwayat keluarga"

     }'

```

## 📦 Dependencies

-**FastAPI**: Web framework untuk API

-**Uvicorn**: ASGI server

-**Transformers**: Hugging Face library untuk NLP

-**TensorFlow**: Machine learning framework

-**Pydantic**: Data validation

-**tf-keras**: Keras untuk TensorFlow

## 🔧 Configuration

### Environment Variables

-`PORT`: Port untuk menjalankan aplikasi (default: 8000)

-`NODE_ENV`: Environment mode (development/production)

### Model Configuration

Model yang digunakan: `Raihan2212/SensecheckCapstone` dari Hugging Face

## 🛠️ Development

### Local Development

```bash

# Aktifkan virtual environment

sourcemyenv/bin/activate  # Linux/macOS

# atau

myenv\Scripts\activate     # Windows


# Jalankan dengan auto-reload

uvicornapi:app--reload

```

### Code Structure

```

model-api/

├── api.py              # Main application file

├── requirements.txt    # Python dependencies

├── README.md          # Documentation

└── .gitignore         # Git ignore file

```

## 🐛 Troubleshooting

### CORS Issues

API sudah dikonfigurasi untuk menerima request dari semua origin (`*`). Jika masih ada masalah CORS, pastikan server berjalan di port yang benar.

### TensorFlow Warnings

Warning TensorFlow tentang CUDA/GPU normal muncul karena model menggunakan CPU. Ini tidak mempengaruhi fungsionalitas.

### Model Loading Issues

Pastikan koneksi internet stabil saat pertama kali menjalankan untuk download model dari Hugging Face.

## 📝 License

MIT License

## 👥 Contributors

- [Your Name](https://github.com/nfapriyanto)

## 📞 Support

Jika ada pertanyaan atau issues, silakan buat issue di GitHub repository.
