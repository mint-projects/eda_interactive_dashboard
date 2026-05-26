"""Top-level entrypoint for Streamlit hosting platforms.

This file delegates to the package implementation at `src/eda_dashboard/app.py`.
Keeping a root-level `app.py` ensures deployments that expect the app at repository root continue to work.
"""

from src.eda_dashboard import app as _app

if __name__ == "__main__":
    _app.main()
