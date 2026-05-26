## 🚧 Progress / TODO

### ✅ Done
- [x] Basic Streamlit layout
- [x] Navigation with buttons
- [x] Average statistics dashboard (little fixes needed)
- [x] Y axis corrected
- [x] Model implemented


### 📌 TODO
- Replace the pie chart (it brings no value to analysis)
- Perform EDA regarding user's sex
- Write the main page content
- eventually deploy (last step)

## Project layout (restructured)

The repository was reorganized to a more conventional layout:

- `src/eda_dashboard/` : Python package containing the Streamlit app (`app.py`).
- `data/` : CSV datasets used by the app.
- `model/` : serialized model (`model.pkl`).
- `notebooks/` : exploratory notebooks (`model.ipynb`, `visualization.ipynb`).
- `requirements.txt` : project dependencies.

Run the Streamlit app from the project root:

```powershell
streamlit run src/eda_dashboard/app.py
```

If you'd like, I can also:
- add a `scripts/` folder with run helpers
- add basic `pyproject.toml` or `setup.cfg` for packaging
- move `model/` into `src/eda_dashboard/` if you prefer a single-package layout
