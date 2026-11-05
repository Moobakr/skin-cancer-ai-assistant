# Project Q&A preparation

## Why did we use Django and React?

Django provides a clean backend API for image upload, preprocessing, model loading, and prediction. React provides a responsive user interface where users can upload images, enter metadata, and understand results.

## Why did we use transfer learning?

The dataset is not large enough to train a very deep CNN from scratch reliably. Transfer learning uses visual features learned from a large image dataset and adapts them to the skin lesion task.

## Why EfficientNetB0?

EfficientNetB0 is lightweight, strong for image classification, and practical for student hardware. It provides a better accuracy/size tradeoff than many larger models.

## Why patient-level splitting?

Some patients or lesions may have multiple images. If random image splitting is used, images from the same patient can appear in both training and test sets, causing data leakage and overly optimistic results.

## Why do we use more than accuracy?

Medical classification needs sensitivity/recall, precision, F1-score, confusion matrix, and per-class metrics. Accuracy alone can hide poor performance on minority or dangerous classes.

## Why add metadata?

Clinical decisions often use both visual appearance and patient context. The dataset includes metadata, so using it makes the model more complete and differentiates the project from simple image-only classifiers.

## Why Grad-CAM?

Grad-CAM highlights image regions that influenced the prediction. This helps show whether the model focuses on the lesion rather than background artifacts.

## Why image quality warnings?

Bad images can reduce prediction reliability. The app checks brightness, blur, and resolution to warn users before interpreting predictions.

## Why is there a medical disclaimer?

The model is educational and not clinically validated. A professional system must not claim to diagnose disease without medical approval, safety testing, and regulatory validation.

## What is the most unique feature?

The combination of multimodal prediction, confidence-aware output, image quality warnings, and an explainable full-stack web interface.
