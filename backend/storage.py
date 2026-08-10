import os
import traceback
from datetime import timedelta
from google.cloud import storage

BUCKET_NAME = "gcf-v2-uploads-592479264150.us-central1.cloudfunctions.appspot.com"

def upload_session_audio(file_path: str, destination_blob_name: str) -> str:
    """
    Uploads the specified WAV file to Firebase Storage (Google Cloud Storage)
    and returns its public/signed HTTPS URL.
    
    If upload fails, returns the local file path as a fallback.
    """
    if not os.path.exists(file_path):
        print(f"[CLOUD UPLOAD] File does not exist locally: {file_path}")
        return file_path
        
    try:
        # Load service account key if available locally
        base_dir = os.path.dirname(os.path.abspath(__file__))
        key_path = os.path.join(base_dir, "service-account.json")
        gcp_key_path = os.path.join(base_dir, "gcp-key.json")
        
        has_credentials = False
        if os.path.exists(key_path):
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path
            has_credentials = True
        elif os.path.exists(gcp_key_path):
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = gcp_key_path
            has_credentials = True
        elif os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
            has_credentials = True
            
        if not has_credentials:
            print("[CLOUD UPLOAD] No GCS credentials found on disk or environment. Skipping GCS upload fallback.")
            return file_path
            
        storage_client = storage.Client()
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(destination_blob_name)
        
        print(f"[CLOUD UPLOAD] Starting upload of {file_path} to gs://{BUCKET_NAME}/{destination_blob_name}")
        blob.upload_from_filename(file_path, content_type="audio/wav")
        print(f"[CLOUD UPLOAD] Upload completed.")
        
        # Try to make public if bucket configuration allows it
        try:
            blob.make_public()
            public_url = blob.public_url
            print(f"[CLOUD UPLOAD] File made public: {public_url}")
            return public_url
        except Exception as acl_err:
            print(f"[CLOUD UPLOAD] Could not make blob public (ACLs likely disabled): {acl_err}")
            
        # Fallback to generating a signed URL (expires in 7 days)
        try:
            signed_url = blob.generate_signed_url(expiration=timedelta(days=7))
            print(f"[CLOUD UPLOAD] Generated signed URL (valid for 7 days): {signed_url}")
            return signed_url
        except Exception as sign_err:
            print(f"[CLOUD UPLOAD] Failed to generate signed URL: {sign_err}")
            
        # Last resort fallback to standard public URL construct
        fallback_url = f"https://storage.googleapis.com/{BUCKET_NAME}/{destination_blob_name}"
        return fallback_url
    except Exception as e:
        print(f"[CLOUD UPLOAD ERROR] Failed to upload audio: {e}")
        traceback.print_exc()
        return file_path
