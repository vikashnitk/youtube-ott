import firebase_admin
from firebase_admin import credentials, firestore
import os
from pathlib import Path

# cred = credentials.Certificate("C:/Users/vikas/Documents/project_startup/django-backend-netflix-clone/djangonetflix/firebase-service-account.json")
# firebase_admin.initialize_app(cred)

# Get the base directory of your Django project
BASE_DIR = Path(__file__).resolve().parent.parent

# Define the path to the Firebase service account file
FIREBASE_CREDENTIALS_PATH = BASE_DIR / "firebase-service-account.json"

# Convert Path object to string before passing it to Firebase
import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate(str(FIREBASE_CREDENTIALS_PATH))
firebase_admin.initialize_app(cred)

# Firestore client instance
db = firestore.client()


