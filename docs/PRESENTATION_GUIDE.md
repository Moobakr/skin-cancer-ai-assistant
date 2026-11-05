# Presentation guide

## Slide 1: Title

**Explainable Multimodal Skin Cancer Screening Assistant**

Mention:

- Dataset: PAD-UFES-20
- Technologies: TensorFlow, Django, React
- Goal: educational AI screening assistant

## Slide 2: Problem

Skin lesion classification is important because early detection helps clinical care. However, visual classification is difficult, and AI models should be interpretable and safe.

## Slide 3: Dataset

Explain:

- Smartphone clinical lesion images
- Metadata file with patient and lesion information
- Multiple diagnostic classes
- Need for patient-level split

## Slide 4: Methodology

Pipeline:

```text
Dataset → preprocessing → patient-level split → CNN/transfer/multimodal training → evaluation → web deployment
```

## Slide 5: Models

Compare:

1. Custom CNN baseline
2. EfficientNetB0 transfer learning
3. EfficientNetB0 + metadata multimodal model

## Slide 6: Evaluation

Show:

- Confusion matrix
- Accuracy/loss curves
- Classification report
- ROC-AUC if available

## Slide 7: Explainability

Show Grad-CAM examples and explain that the highlighted area influences the model's prediction.

## Slide 8: Web app

Show screenshots:

- Upload form
- Metadata form
- Prediction result
- Technical mode

## Slide 9: Safety features

Mention:

- Confidence levels
- Uncertainty warnings
- Image quality checks
- Medical disclaimer

## Slide 10: Conclusion

State:

> The project is more than a classifier. It is a full-stack, explainable, confidence-aware AI assistant that combines image and metadata information.
