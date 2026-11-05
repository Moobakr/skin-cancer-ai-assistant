# Report Template

## 1. Abstract

This project develops an explainable multimodal deep learning web application for skin lesion classification using the PAD-UFES-20 dataset. The system combines lesion image analysis with optional clinical metadata and deploys the trained model through a Django REST API and responsive React frontend.

## 2. Introduction

Explain the motivation for skin lesion classification and why explainable AI is important in medical applications.

## 3. Dataset

Describe the dataset, diagnostic classes, images, metadata, and any imbalance observed during exploratory analysis.

## 4. Preprocessing

Include:

- Image resizing
- Normalization/preprocessing
- Data augmentation
- Metadata encoding/scaling
- Patient-level split

## 5. Model Architecture

Describe:

- Baseline CNN
- EfficientNetB0 transfer learning
- Multimodal fusion model

## 6. Training Strategy

Include:

- Loss function
- Optimizer
- Class weights
- Early stopping
- Learning-rate reduction
- Fine-tuning

## 7. Evaluation

Add final metrics after training.

| Model | Accuracy | Macro Recall | Macro F1 | Notes |
|---|---:|---:|---:|---|
| Custom CNN | TODO | TODO | TODO | Baseline |
| EfficientNetB0 | TODO | TODO | TODO | Image-only transfer model |
| EfficientNetB0 + Metadata | TODO | TODO | TODO | Final model |

## 8. Explainability

Discuss Grad-CAM and include examples.

## 9. Web Application

Explain Django backend and React frontend architecture.

## 10. Limitations

Mention dataset size, class imbalance, non-clinical validation, and the need for dermatologist consultation.

## 11. Conclusion

Summarize the full pipeline and unique project contributions.
