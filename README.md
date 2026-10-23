# Student Result Prediction — Practical 9

This repository contains the Student Result Prediction API, Docker packaging, and GitHub Actions automation for **Practical 9: Automate Docker Image Build, Test, and Publish to GHCR**.

## CI/CD workflow

The workflow is stored at `.github/workflows/docker-publish.yml`. It runs on every push to `main` and can also be started manually from the Actions tab.

1. Checks out the repository and installs Python dependencies.
2. Creates the model artifact required by the API.
3. Builds the Docker image.
4. Starts a temporary container and retries `GET /health`.
5. Sends a sample request to `POST /predict`.
6. Removes the test container.
7. Authenticates to GitHub Container Registry with the workflow's `GITHUB_TOKEN`.
8. Publishes the tested image as `latest` and `sha-<full-commit-sha>`.

The registry image name is normalized to lowercase: `ghcr.io/dileepkumarkota/student-result-prediction`. The image is only pushed if the build and API checks succeed.

## API

- `GET /` — service status.
- `GET /health` — checks that the model can be loaded.
- `POST /predict` — predicts `PASS` or `FAIL`.

Prediction request fields are `attendance`, `internal_marks`, `assignment_marks`, and `previous_score`; each must be numeric and between 0 and 100.

Example:
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  --data '{"attendance":90,"internal_marks":85,"assignment_marks":88,"previous_score":80}'
```

## Run locally

```bash
python -m pip install -r requirements.txt
python train_model.py
python app.py
```

## Docker

The model artifact and `metrics.json` are generated before the image is built in CI.

```bash
python train_model.py
docker build -t student-result-prediction:ci .
docker run --rm -p 5000:5000 student-result-prediction:ci
```

## Verify the workflow and package

- [GitHub Actions runs](https://github.com/Dileepkumarkota/Student_Result_Prediction-/actions)
- [GitHub Container Registry package](https://github.com/Dileepkumarkota?tab=packages)

If GHCR refuses to update an existing package created by another repository, open that package's **Package settings → Manage Actions access** and grant this repository write access.
