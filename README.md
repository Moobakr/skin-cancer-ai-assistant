# Explainable Multimodal Skin Cancer Screening Assistant

A complete full-stack deep learning project for the **Skin Cancer / PAD-UFES-20** dataset.  
It includes:

- TensorFlow/Keras training pipelines for image-only and multimodal models
- Patient-level train/validation/test splitting to reduce data leakage
- Class imbalance handling
- Grad-CAM explainability utilities
- Image quality checks
- Django REST API for predictions
- React responsive frontend
- Model card, Q&A notes, and presentation guide

> **Important medical disclaimer:** This project is for education and research only. It is not a medical diagnosis system and must not replace professional dermatology consultation.

---

## 1. Project idea

Instead of building a basic image classifier, this project implements an **explainable multimodal AI assistant**:

```text
Skin lesion image + optional clinical metadata
        â†“
Django API preprocessing and model inference
        â†“
Prediction probabilities + risk level + uncertainty message + image quality warnings
        â†“
React user interface with simple and technical result views
```

The final system is designed to be easy to explain during a viva or project discussion.

---

## 2. Repository structure

```text
skin_cancer_ai_assistant/
â”œâ”€â”€ ai_model/                 # Training/evaluation/export code
â”‚   â”œâ”€â”€ src/
â”‚   â”œâ”€â”€ artifacts/            # Generated models, metrics, class files
â”‚   â””â”€â”€ requirements.txt
â”‚
â”œâ”€â”€ backend/                  # Django REST API
â”‚   â”œâ”€â”€ predictions/
â”‚   â”œâ”€â”€ skin_cancer_api/
â”‚   â”œâ”€â”€ manage.py
â”‚   â””â”€â”€ requirements.txt
â”‚
â”œâ”€â”€ frontend/                 # React + Vite frontend
â”‚   â”œâ”€â”€ src/
â”‚   â”œâ”€â”€ package.json
â”‚   â””â”€â”€ vite.config.js
â”‚
â”œâ”€â”€ docs/                     # Report, Q&A, model card, API docs
â””â”€â”€ scripts/                  # Helper setup scripts
```

---

## 3. Dataset setup

Download the Kaggle dataset manually or using Kaggle API.

Expected local layout:

```text
data/pad_ufes_20/
â”œâ”€â”€ metadata.csv
â””â”€â”€ images/
    â”œâ”€â”€ PAT_1_15_820.png
    â””â”€â”€ ...
```

The training code tries to detect the metadata file and image filename column automatically. If your extracted Kaggle folder has a different structure, set paths explicitly in the command line.

See [`docs/DATASET_SETUP.md`](docs/DATASET_SETUP.md).

---

## 4. Train the model

Create Python environment:

```bash
cd ai_model
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Train image-only EfficientNetB0:

```bash
python -m src.train_image_model \
  --dataset-dir ../data/pad_ufes_20 \
  --output-dir artifacts/image_model \
  --model efficientnet \
  --epochs 25 \
  --batch-size 16
```

Train multimodal model:

```bash
python -m src.train_multimodal_model \
  --dataset-dir ../data/pad_ufes_20 \
  --output-dir artifacts/multimodal_model \
  --epochs 25 \
  --batch-size 16
```

Export the best model bundle for Django:

```bash
python -m src.export_bundle \
  --trained-dir artifacts/multimodal_model \
  --backend-bundle-dir ../backend/model_bundle
```

---

## 5. Run Django backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Health check:

```text
http://localhost:8000/api/health/
```

Prediction endpoint:

```text
POST http://localhost:8000/api/predict/
```

If no trained model is exported yet, the backend runs in **demo-safe mode** and returns a clear warning that predictions are placeholders.

---

## 6. Run React frontend

```bash
cd frontend
npm install
npm run dev
```

Open:

```text
http://localhost:5173
```

---

## 7. Best features to present

1. **Patient-level split** to reduce data leakage.
2. **Transfer learning** using EfficientNetB0.
3. **Multimodal model** combining image and metadata.
4. **Confidence-aware prediction** with uncertainty warnings.
5. **Risk grouping** for user-friendly output.
6. **Image quality checks** for brightness, size, and blur.
7. **Grad-CAM utility** for explainability.
8. **Full-stack Django + React integration**.

---

## 8. Suggested team explanation

> We built an explainable multimodal skin lesion screening assistant. The deep learning part trains image-only and image-plus-metadata models using TensorFlow. The backend is a Django REST API that preprocesses uploaded images, runs model inference, checks image quality, and returns prediction probabilities. The frontend is a responsive React app that lets users upload a lesion image, enter metadata, view confidence and risk level, and switch between simple and technical result views.

---

## 9. What you still need to add before final submission

Because the dataset and trained weights are not included in this zip:

1. Download the Kaggle dataset.
2. Train one or more models.
3. Export the best model bundle into `backend/model_bundle/`.
4. Run the full app and capture screenshots for your report/presentation.
5. Fill the final achieved metrics in `docs/MODEL_CARD.md` and `docs/REPORT_TEMPLATE.md`.
