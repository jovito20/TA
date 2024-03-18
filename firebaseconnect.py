import firebase_admin
from firebase_admin import credentials, storage

# Initialize Firebase Admin SDK with service account credentials
cred = credentials.Certificate("tubescc2023-firebase-adminsdk-a4hvb-b62ff9d985.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'tubescc2023.appspot.com'
})