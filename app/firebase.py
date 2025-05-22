import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin SDK
cred = credentials.Certificate("app/FBcredentials.json")
firebase_admin.initialize_app(cred)

# Get Firestore client
db = firestore.client()

def initUser(user_id, resume="default", role="default"):
    """Initialize a user document with basic fields."""
    if (hasResume(user_id)) :
        return
    data = {
        "resume": resume,
        "role": role
    }
    users_ref = db.collection("users").document(user_id)
    users_ref.set(data)
    print(f"Initialized user {user_id} successfully!")

def updateRole(user_id, new_role):
    """Update the intended role of the user."""
    users_ref = db.collection("users").document(user_id)
    users_ref.set({"role": new_role})
    print(f"Updated role for {user_id} to {new_role}.")
    
def updateCompany(user_id, new_company):
    """Update the intended role of the user."""
    users_ref = db.collection("users").document(user_id)
    users_ref.set({"company": new_company})
    print(f"Updated role for {user_id} to {new_company}.")

def updateResume(user_id, new_resume):
    """Update the resume field of the user."""
    users_ref = db.collection("users").document(user_id)
    users_ref.set({"resume": new_resume})
    print(f"Updated resume for {user_id}.")

def getRole(user_id):
    """Retrieve the user's intended role."""
    users_ref = db.collection("users").document(user_id)
    doc = users_ref.get()
    if doc.exists:
        role = doc.to_dict().get("role", None)
        print(f"{user_id}'s role: {role}")
        return role
    else:
        print(f"No user found with ID {user_id}")
        return None
    

def getCompany(user_id):
    """Retrieve the user's intended target comapny."""
    users_ref = db.collection("users").document(user_id)
    doc = users_ref.get()
    if doc.exists:
        company = doc.to_dict().get("company", None)
        print(f"{user_id}'s role: {company}")
        return company
    else:
        print(f"No user found with ID {user_id}")
        return None

def getResume(user_id):
    """Retrieve the user's resume."""
    users_ref = db.collection("users").document(user_id)
    doc = users_ref.get()
    if doc.exists:
        resume = doc.to_dict().get("resume", None)
        print(f"{user_id}'s resume: {resume}")
        return resume
    else:
        print(f"No user found with ID {user_id}")
        return None
    
def hasResume(user_id):
    if not user_id:
        return False  # No user logged in

    doc_ref = db.collection("users").document(user_id)
    doc = doc_ref.get()

    if not doc.exists:
        return False  # User document doesn't exist

    if (getResume(user_id) == "default"):
        return False

    user_data = doc.to_dict()
    resume_text = user_data.get("resume")

    if resume_text and resume_text.strip():  # Resume exists and not just spaces
        return True
    else:
        return False

def getEducation(user_id) :
    """
    Retrieve the user's education field from Firestore.
    
    Args:
        user_id (str): The user's document ID (usually their email).
        
    Returns:
        str or None: The user's education info if available, else None.
    """
    users_ref = db.collection("users").document(user_id)
    doc = users_ref.get()
    
    if doc.exists:
        user_data = doc.to_dict()
        education = user_data.get("education")  # 🔥 Fetch "education" field
        
        if education and education.strip():  # Non-empty check
            print(f"Education for {user_id}: {education}")
            return education
        else:
            print(f"Education field is empty for {user_id}.")
            return None
    else:
        print(f"No user found with ID {user_id}.")
        return None
# --- Example usage ---
# Initialize
# updateCompany("Morty","google")