"""
Vercel entry point — adds the SMS-Spam-Classifier directory to sys.path
so that app.py can import model.py, and exposes the Flask `app` object.
"""

import sys
import os

# Make the SMS-Spam-Classifier package importable from this serverless function
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_APP_DIR = os.path.join(_ROOT, "SMS-Spam-Classifier")
sys.path.insert(0, _APP_DIR)

# Import the Flask app — do NOT call get_stats() or anything heavy at module level
from app import app  # noqa: E402  (app is the Flask instance)

# Vercel looks for a WSGI-callable named `app`
# Nothing else is needed here.
