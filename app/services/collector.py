from __future__ import annotations

from typing import Dict, List, Optional

from ..models import Lead
from ..places_client import PlacesClient

def _get_display_name(place: dict) -> Optional[str]:
    dn = place.get("displayName")
    if isinstance(dn, dict):
        return dn.get("text")
    return None

def collect_leads(
    client: PlacesClient,
    *,
    query: str,
    center_lat: float,
    center_lng: float,
    radius_m: int,
    limit: int,
    enrich: bool = False,
) -> List[Lead]:
    results_by_id: Dict[str, Lead] = {}
    page_token: Optional[str] = None

    while True:
        data = client.search_text(
            text_query=query,
            center_lat=center_lat,
            center_lng=center_lng,
            radius_m=radius_m,
            page_token=page_token,
            max_result_count=20,
        )

        places = data.get("places", []) or []
        for p in places:
            pid = p.get("id")
            if not pid or pid in results_by_id:
                continue

            loc = p.get("location") or {}
            lead = Lead(
                placeId=pid,
                name=_get_display_name(p),
                address=p.get("formattedAddress"),
                googleMapsUrl=p.get("googleMapsUri"),
                latitude=loc.get("latitude"),
                longitude=loc.get("longitude"),
                phone=None,
                website=None,
            )
            results_by_id[pid] = lead

            if len(results_by_id) >= limit:
                break

        if len(results_by_id) >= limit:
            break

        page_token = data.get("nextPageToken")
        if not page_token:
            break

    leads = list(results_by_id.values())

    if enrich and leads:
        for i, lead in enumerate(leads):
            details = client.place_details(place_id=lead.place_id)
            lead.phone = details.get("internationalPhoneNumber") or lead.phone
            lead.website = details.get("websiteUri") or lead.website
            leads[i] = lead

    return leads
