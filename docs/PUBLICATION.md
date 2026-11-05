# Running the recovered original project

This publication adds setup notes and aggregate evidence without changing the
recovered application or training code. Use Python 3.12 and Node 24. The package
lock retains the frontend versions used locally. The direct Python constraints
record the runtime used to load and audit the original model; they are not a full
transitive environment lock.

## Install and start on Windows

Run from the repository root in PowerShell:

```powershell
py -3.12 -m venv backend/.venv
.\backend\.venv\Scripts\python.exe -m pip install -c constraints-tested.txt -r backend/requirements.txt
```

Download `original-model-bundle.zip` from the
[original model release](https://github.com/Moobakr/skin-cancer-ai-assistant/releases/tag/original-model-v1)
into the repository root, then run:

```powershell
Expand-Archive -LiteralPath .\original-model-bundle.zip -DestinationPath . -Force
$env:MODEL_BUNDLE_DIR = (Resolve-Path .\backend\model_bundle).Path
.\backend\.venv\Scripts\python.exe backend/manage.py migrate
.\backend\.venv\Scripts\python.exe backend/manage.py runserver --noreload
```

In a second terminal at the repository root:

```powershell
cd frontend
npm.cmd ci
npm.cmd run dev -- --strictPort
```

Open <http://localhost:5173>. The response at
<http://localhost:8000/api/health/> should contain `model_loaded: true`, `mode: real`
and `load_error: null`. If either port is occupied, stop the older project instance
in its own terminal before starting this copy.

On macOS/Linux, create the environment with `python3.12 -m venv backend/.venv`, use
`backend/.venv/bin/python` for Python commands, extract the ZIP with `unzip`, and
use `npm` instead of `npm.cmd`. Set `MODEL_BUNDLE_DIR` in the process environment
if the default `backend/model_bundle` directory is overridden. Backend `.env.example`
is a reference template; the original settings do not automatically load it.

## Verify the preserved bundle

The release contains `model.keras`, its fitted metadata preprocessor, its 22-field
schema, class names, and the original configuration. Keep these files together.
The release `SHA256SUMS.txt` records the ZIP and each bundle-file hash. The model
and preprocessor hashes are also in the aggregate audit JSON.

The measured audit used the original saved test split and unchanged weights.
Patient-level split CSVs and patient images are not published here. Reproducing
the exact numbers requires those same split files and the PAD-UFES-20 data;
uploading individual images in the interface does not measure dataset accuracy.
The original `evaluate.py` is retained as recovered, including its historical
Keras loading behavior; this publication does not claim that every legacy
training/evaluation command runs unchanged under every dependency version.

## Attribution and license status

PAD-UFES-20 was created by Pacheco and colleagues. EfficientNet is the established
architecture by Tan and Le; the project uses the Keras ImageNet-pretrained
implementation. TensorFlow/Keras, scikit-learn, Django REST Framework and React
provide the underlying frameworks. Dataset, pretrained-weight and dependency
terms remain separate. No source-code license has been selected.

AI coding assistance was used for recovery, the later research revision, and
publication preparation. This does not assign authorship of the original student
project or its teammates' work. Contributor names and individual roles have not
been supplied; describe personal contributions accurately when using this project
in an application.
