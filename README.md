# Skin Cancer AI Assistant

A full-stack skin lesion classification project using **EfficientNetB3**, patient metadata, and the **PAD-UFES-20** dataset. The application combines a Django REST API with a React interface for uploading images and viewing predictions.

Built with TensorFlow/Keras, scikit-learn, Django REST Framework, React, and Vite.

## Features

- Classification of six lesion types: ACK, BCC, MEL, NEV, SCC, and SEK.
- Image-only and image-plus-metadata training pipelines with patient-level dataset splitting.
- Image quality checks, prediction probabilities, and uncertainty messages.
- Contrast enhancement and five-view prediction averaging in the API.
- Grad-CAM utilities for inspecting model attention.

For education and research only; the application is not validated for medical diagnosis.

## Model results

| Metric | Test result |
|---|---:|
| Top-1 accuracy | **69.3% (237/342)** |
| Top-2 accuracy | **89.2% (305/342)** |

Top-1 measures whether the first prediction is correct. Top-2 measures whether the correct class appears among the two highest predictions.

Evaluation used 342 patient-disjoint test images, a single image view, and all 22 dataset metadata fields, including biopsy status. The app collects fewer fields and uses different image preprocessing, so these scores describe the model evaluation rather than the complete application pipeline.

[Full evaluation results](docs/results/original_model_test_audit.json)

## Run locally

Requirements: **Python 3.12** and **Node.js 24**.

### Backend

From the repository root, run in PowerShell:

```powershell
py -3.12 -m venv backend/.venv
.\backend\.venv\Scripts\python.exe -m pip install -c constraints-tested.txt -r backend/requirements.txt
```

Download [original-model-bundle.zip](https://github.com/Moobakr/skin-cancer-ai-assistant/releases/download/original-model-v1/original-model-bundle.zip) into the repository root, then extract it and start the API:

```powershell
Expand-Archive -LiteralPath .\original-model-bundle.zip -DestinationPath . -Force
$env:MODEL_BUNDLE_DIR = (Resolve-Path .\backend\model_bundle).Path
.\backend\.venv\Scripts\python.exe backend/manage.py migrate
.\backend\.venv\Scripts\python.exe backend/manage.py runserver --noreload
```

The bundle contains the trained model and its matching metadata preprocessor, schema, and class labels. Without it, the app returns labelled placeholder predictions.

### Frontend

In a second terminal:

```powershell
cd frontend
npm.cmd ci
npm.cmd run dev -- --strictPort
```

Open **http://localhost:5173**. Check **http://localhost:8000/api/health/** for `model_loaded: true` and `mode: real`.

On macOS/Linux, use `python3.12`, `backend/.venv/bin/python`, `npm`, and `unzip` in place of the Windows commands.

## API

| Endpoint | Purpose |
|---|---|
| `GET /api/health/` | Model loading status |
| `POST /api/predict/` | Image upload, optional metadata, and prediction results |

See [API documentation](docs/API.md) for request and response details.

## Project structure

```text
ai_model/   Training, evaluation, preprocessing, and Grad-CAM
backend/    Django REST API and model inference
frontend/   React interface
docs/      Dataset setup and evaluation documentation
```

See [dataset setup](docs/DATASET_SETUP.md) and [training scripts](ai_model/src) to work with PAD-UFES-20. Dataset images are downloaded separately.

## Research extension

[skin-cancer-ai-research](https://github.com/Moobakr/skin-cancer-ai-research) compares image-only classification with a model using five metadata fields, with detailed class-level evaluation.
