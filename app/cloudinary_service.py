"""
Cloudinary configuration module.

This module loads environment variables from a .env file and configures
Cloudinary for image upload and management services.

Environment Variables Required:
    CLOUDINARY_NAME (str): Cloudinary cloud name.
    CLOUDINARY_API_KEY (str): API key for Cloudinary.
    CLOUDINARY_API_SECRET (str): API secret for Cloudinary.

Notes:
    - Uses python-dotenv to load environment variables.
    - Secure mode is enabled for HTTPS requests.
"""

import cloudinary
from os import getenv
from dotenv import load_dotenv

load_dotenv()

cloudinary.config(
    cloud_name=getenv("CLOUDINARY_NAME"),
    api_key=getenv("CLOUDINARY_API_KEY"),
    api_secret=getenv("CLOUDINARY_API_SECRET"),
    secure=True
)