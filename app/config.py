from __future__ import annotations

import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    api_key: str = os.getenv("GOOGLE_MAPS_API_KEY", "").strip()
    places_base_url: str = "https://places.googleapis.com/v1"

settings = Settings()
