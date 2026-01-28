from __future__ import annotations

import requests
from typing import Any, Dict, Optional

from .config import settings
from .utils.http import with_retries

class PlacesClient:
    """Client for Google Places API (New) over REST.
    Uses:
    - POST /v1/places:searchText
    - GET  /v1/places/{placeId}
    """

    def __init__(self, api_key: Optional[str] = None, timeout_s: float = 20.0) -> None:
        self.api_key = (api_key or settings.api_key).strip()
        if not self.api_key:
            raise ValueError("Missing GOOGLE_MAPS_API_KEY. Set it in .env or environment variables.")
        self.base_url = settings.places_base_url.rstrip("/")
        self.timeout_s = timeout_s
        self.session = requests.Session()

    def _headers(self, field_mask: str) -> Dict[str, str]:
        # Field mask must be a comma-separated string, no spaces.
        return {
            "X-Goog-Api-Key": self.api_key,
            "X-Goog-FieldMask": field_mask,
            "Content-Type": "application/json; charset=utf-8",
        }

    def search_text(
        self,
        *,
        text_query: str,
        center_lat: float,
        center_lng: float,
        radius_m: int,
        page_token: Optional[str] = None,
        max_result_count: int = 20,
        language_code: str = "fr",
        region_code: str = "CA",
        field_mask: str = "places.id,places.displayName,places.formattedAddress,places.googleMapsUri,places.location,nextPageToken",
    ) -> Dict[str, Any]:
        url = f"{self.base_url}/places:searchText"
        payload: Dict[str, Any] = {
            "textQuery": text_query,
            "maxResultCount": max_result_count,
            "languageCode": language_code,
            "regionCode": region_code,
            "locationRestriction": {
                "circle": {
                    "center": {"latitude": center_lat, "longitude": center_lng},
                    "radius": radius_m,
                }
            },
        }
        if page_token:
            payload["pageToken"] = page_token

        def call() -> Dict[str, Any]:
            r = self.session.post(url, headers=self._headers(field_mask), json=payload, timeout=self.timeout_s)
            if r.status_code >= 400:
                raise RuntimeError(f"Places searchText failed: {r.status_code} {r.text}")
            return r.json()

        return with_retries(call)

    def place_details(
        self,
        *,
        place_id: str,
        language_code: str = "fr",
        region_code: str = "CA",
        field_mask: str = "id,internationalPhoneNumber,websiteUri",
    ) -> Dict[str, Any]:
        # NOTE: For GET details, field mask does NOT need the 'places.' prefix.
        url = f"{self.base_url}/places/{place_id}"
        params = {"languageCode": language_code, "regionCode": region_code}

        def call() -> Dict[str, Any]:
            r = self.session.get(url, headers=self._headers(field_mask), params=params, timeout=self.timeout_s)
            if r.status_code >= 400:
                raise RuntimeError(f"Places details failed for {place_id}: {r.status_code} {r.text}")
            return r.json()

        return with_retries(call)
