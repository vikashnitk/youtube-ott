import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("C:/Users/vikas/Documents/project_startup/django-backend-netflix-clone/djangonetflix/firebase-service-account.json")
firebase_admin.initialize_app(cred)

# Firestore client instance
db = firestore.client()


