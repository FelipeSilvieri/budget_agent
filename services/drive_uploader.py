from __future__ import annotations

import os
from typing import Optional

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build  # type: ignore
from googleapiclient.http import MediaFileUpload  # type: ignore


def upload_file(filepath: str, folder_id: str) -> Optional[str]:
    """Upload a file to a Google Drive folder and return the file ID.

    Parameters
    ----------
    filepath:
        Absolute path to the file to upload.
    folder_id:
        Google Drive folder identifier.
    Returns
    -------
    Optional[str]
        File ID if upload succeeds, otherwise ``None``.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(filepath)

    creds = Credentials.from_authorized_user_file(
        "token.json", ["https://www.googleapis.com/auth/drive.file"]
    )
    service = build("drive", "v3", credentials=creds)

    file_metadata = {"name": os.path.basename(filepath), "parents": [folder_id]}
    media = MediaFileUpload(filepath)
    uploaded = (
        service.files()
        .create(body=file_metadata, media_body=media, fields="id")
        .execute()
    )
    return uploaded.get("id")
