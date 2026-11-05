# Model Card: Explainable Skin Lesion Classification Model

## Model name

`skin-cancer-multimodal-efficientnet`

## Intended use

Educational skin lesion classification project using the PAD-UFES-20 dataset. The system is designed to demonstrate deep learning, transfer learning, multimodal fusion, API integration, and explainability.

## Not intended for

- Real medical diagnosis
- Emergency medical decision-making
- Replacing dermatologists
- Use on populations or image types not represented in the dataset

## Dataset

PAD-UFES-20 clinical skin lesion dataset containing smartphone clinical images and patient/clinical metadata.

## Inputs

- Lesion image
- Optional metadata: age, sex, anatomical site, smoking/drinking history, and other available columns

## Outputs

- Class probabilities
- Predicted class
- Confidence level
- Risk group
- Quality warnings
- Optional Grad-CAM visual explanation

## Evaluation metrics to report

Fill these after training:

| Metric | Validation | Test |
|---|---:|---:|
| Accuracy | TODO | TODO |
| Macro Precision | TODO | TODO |
| Macro Recall | TODO | TODO |
| Macro F1 | TODO | TODO |
| Weighted F1 | TODO | TODO |
| ROC-AUC | TODO | TODO |

## Safety notes

The frontend and backend intentionally include medical disclaimers and uncertainty warnings. Low-confidence results should not be presented as certain decisions.

## Known limitations

- Dataset size is limited compared with large medical AI datasets.
- Images come from specific collection conditions and may not represent all skin types, cameras, or lighting conditions.
- Class imbalance may affect minority class recall.
- Model outputs are correlations learned from data, not clinical reasoning.
