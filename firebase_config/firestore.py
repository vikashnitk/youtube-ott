from .config import db
from users.models import User

def get_user_email(uid):
    """
    Retrieves the email of the user from Firestore using the UID.
    """
    doc_ref = db.collection('users').document(uid)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict().get('email')
    return None

def listen_for_user_deletions():
    """
    Listens for deletions in the Firestore 'users' collection and deletes the corresponding user in the Django database.
    """
    print("Starting Firestore listener for user deletions...")

    def on_snapshot(col_snapshot, changes, read_time):
        print("Snapshot received.")
        for change in changes:
            print(f"Change detected: {change.type.name}")
            if change.type.name == 'REMOVED':
                uid = change.document.id
                print(f"Document with UID {uid} was removed.")
                try:
                    user = User.objects.get(uid=uid)
                    user.delete()
                    print(f"User with UID {uid} deleted from Django database.")
                except User.DoesNotExist:
                    print(f"User with UID {uid} does not exist in Django database.")

    users_collection = db.collection('users')
    users_collection.on_snapshot(on_snapshot)
