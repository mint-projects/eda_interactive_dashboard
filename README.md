# Smartphone Addiction EDA Dashboard

Project reorganized for a clearer layout and deployments.

Layout
- `app.py` : root entrypoint delegating to the package (for Streamlit hosting).
- `src/eda_dashboard/app.py` : main Streamlit application (package location).
- `data/` : CSV datasets used by the app.
- `model/` : serialized model file (`model.pkl`).
- `notebooks/` : exploratory notebooks.

Run locally
```powershell
# recommended (root entrypoint)
streamlit run app.py

# or directly run the package script
streamlit run src/eda_dashboard/app.py
```

Deployment notes
- If your hosting provider expects a repository-root `app.py`, the included root `app.py` ensures compatibility.
- Ensure `model/model.pkl` and `data/` are available to the deployment environment. If you prefer not to commit model artifacts, store them in external storage and fetch during deploy.

If deployment still fails, share the platform logs and I will diagnose further.
