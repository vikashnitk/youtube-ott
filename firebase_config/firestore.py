from .config import db

def get_user_email(uid):
    """
    Retrieves the email of the user from Firestore using the UID.
    """
    doc_ref = db.collection('users').document(uid)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict().get('email')
    return None
