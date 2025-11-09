# AI Prioritizer for Vulnerability Findings

Enterprise-grade solution that ingests vulnerability findings, enriches them, scores them with a reproducible ML pipeline, and exposes a REST API for integration into ticketing and CI/CD systems.

Features
- Prioritize findings by business impact and exploitability
- Combine CVSS, asset context and natural language descriptions
- Reproducible training pipeline and lightweight inference service
- Explainability with SHAP and structured logs

Run with Docker
```
docker build -t ai-prioritizer:latest .
docker run -p 8000:8000 ai-prioritizer:latest
```

Open http://localhost:8000/docs for interactive API documentation

Contents
- app/: FastAPI inference service
- model/: training and inference utilities
- data/: example data
- tests/: basic test suite
- .github/: CI workflow
