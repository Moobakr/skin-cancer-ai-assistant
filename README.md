# Skin Cancer AI Assistant

A multimodal machine-learning project that combines **skin-lesion images and patient metadata** to classify six lesion types. It connects an **EfficientNetB3** model to a Django REST API and React interface, covering the workflow from training to interactive predictions.

[![Build and smoke checks](https://github.com/Moobakr/skin-cancer-ai-assistant/actions/workflows/checks.yml/badge.svg)](https://github.com/Moobakr/skin-cancer-ai-assistant/actions/workflows/checks.yml)

**My role: Model training.** I worked on training the skin-lesion classifier using transfer learning and fine-tuning. The repository also includes data-processing, backend, and frontend components that support the application.

## Problem and objective

Skin-lesion classification involves both visual appearance and patient context. This project explores how to combine these inputs in a six-class classifier using the **PAD-UFES-20** dataset of smartphone clinical images and structured metadata.

The objective is to train a multimodal model and integrate its predictions into an application that presents class probabilities, image quality feedback, and uncertainty messages. The six classes are ACK, BCC, MEL, NEV, SCC, and SEK.

For education and research only; the application is not validated for medical diagnosis.

## Technical approach

```text
Lesion image -> EfficientNetB3 -> Image features --------+
                                                       +-> Fusion head -> Six class probabilities
Patient data -> Metadata preprocessing -> Dense layers -+
```

- **Transfer learning:** ImageNet-pretrained EfficientNetB3 processes 300 x 300 RGB images. Training first freezes the backbone, then fine-tunes its final layers at a lower learning rate.
- **Multimodal fusion:** The trained model combines image features with 22 metadata fields, encoded into 77 numerical features. The preprocessing pipeline imputes missing values, scales numerical columns, and one-hot encodes categorical columns.
- **Class imbalance:** The training workflow includes class weights, capped minority-class oversampling, and focal loss with label smoothing. Image augmentation is applied during training.
- **Model selection:** Checkpoints are selected by validation loss, with early stopping and learning-rate reduction. Images are grouped by patient when creating dataset splits.

Implementation: [model architecture](ai_model/src/models.py), [training pipeline](ai_model/src/train_multimodal_model.py), and [data splitting](ai_model/src/data.py).

## Evaluation and findings

| Metric | Test result |
|---|---:|
| Top-1 accuracy | **69.3% (237/342)** |
| Top-2 accuracy | **89.2% (305/342)** |
| Balanced accuracy | **59.2%** |
| Macro-F1 | **0.588** |

Top-1 measures whether the first prediction is correct. Top-2 measures whether the correct class appears among the two highest predictions.

The saved checkpoint was evaluated on **342 test images from 206 patients**, with no patient overlap between training, validation, and test splits. Evaluation used a single image view and all 22 dataset metadata fields.

The results show that first-choice accuracy and candidate ranking measure different aspects of performance. Balanced accuracy and macro-F1 also show why aggregate accuracy alone is insufficient for this imbalanced dataset.

**Evaluation limits:** The original metadata includes biopsy status, which limits its suitability for a prediction made before diagnosis. The app collects fewer fields and applies contrast enhancement and five-view averaging, so these scores do not measure the complete application pipeline. Results come from one dataset and split; external validation has not been performed.

[Full metrics, class-level results, and confusion matrix](docs/results/original_model_test_audit.json)

## Application and engineering

| Component | Implementation |
|---|---|
| Model training | Python, TensorFlow/Keras, EfficientNetB3, augmentation and fine-tuning |
| Metadata processing | scikit-learn pipelines; fitted preprocessing shipped with the model |
| Inference API | Django REST Framework; model loaded once per service instance; health and prediction endpoints |
| User interface | React and Vite; image upload, optional metadata, probabilities and uncertainty messages |
| Image processing | OpenCV checks for resolution, brightness, contrast and blur; contrast enhancement and five-view averaging |
| Model inspection | Grad-CAM utilities in the training package |
| Build verification | GitHub Actions checks Python syntax, Django configuration and the frontend production build |

The [downloadable model bundle](https://github.com/Moobakr/skin-cancer-ai-assistant/releases/tag/original-model-v1) keeps the checkpoint, fitted preprocessor, feature schema, and class labels together. The release includes checksums, and the repository records tested Python dependency versions and a frontend lockfile.

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
docs/       Dataset setup and evaluation documentation
```

See [dataset setup](docs/DATASET_SETUP.md) and [training scripts](ai_model/src) to work with PAD-UFES-20. Dataset images are downloaded separately.

## Research extension

The original evaluation raises a practical question: **how does performance change when metadata is restricted to information the app actually collects?**

[skin-cancer-ai-research](https://github.com/Moobakr/skin-cancer-ai-research) investigates this through an image-only versus five-field metadata comparison, reporting class-level results and failure cases. It is a separate experiment with its own protocol and results.
