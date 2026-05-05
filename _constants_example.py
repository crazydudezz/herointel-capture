"""Template for _constants.py — copy this file to _constants.py to build/run.

These are production values for the live HeroIntel deployment. The Firebase
keys are public-by-design (intentionally exposed in the web app's
NEXT_PUBLIC_* env vars). Security is enforced server-side by Firestore rules
and the device-pairing API, not by hiding the API key.

To point this app at a different deployment (e.g. a self-hosted fork), edit
the values below before running.
"""

FIREBASE_API_KEY = "AIzaSyBOJXAFiAwsQZ0Lkxr7UtDQJbc5XKzupMs"
FIREBASE_PROJECT_ID = "herointel-bc2ba"
FIREBASE_STORAGE_BUCKET = "herointel-bc2ba.firebasestorage.app"
WEB_APP_URL = "https://herointel.gg"
