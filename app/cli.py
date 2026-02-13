from __future__ import annotations

import argparse
import os
from datetime import datetime

from .places_client import PlacesClient
from .services.collector import collect_leads
from .services.exporter import export_to_xlsx

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Google Places (New) leads exporter to Excel.")
    p.add_argument("--query", required=True, help="Text query, e.g. 'plombier' or 'plomberie'")
    p.add_argument("--center-lat", type=float, required=True)
    p.add_argument("--center-lng", type=float, required=True)
    p.add_argument("--radius-m", type=int, default=50000)
    p.add_argument("--limit", type=int, default=500)
    p.add_argument("--enrich", type=str, default="false", choices=["true", "false"])
    p.add_argument("--out", default=None, help="Output .xlsx file path")
    return p.parse_args()

def main() -> None:
    args = parse_args()
    enrich = args.enrich.lower() == "true"

    out_path = args.out
    if not out_path:
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_q = "".join(ch for ch in args.query if ch.isalnum() or ch in ("-", "_")).strip() or "query"
        out_path = f"leads_{safe_q}_{stamp}.xlsx"

    client = PlacesClient()
    leads = collect_leads(
        client,
        query=args.query,
        center_lat=args.center_lat,
        center_lng=args.center_lng,
        radius_m=args.radius_m,
        limit=args.limit,
        enrich=enrich,
    )
    # print(leads, 'before exporting')
    export_to_xlsx(leads, out_path)
    print(f"OK: {len(leads)} leads exported -> {os.path.abspath(out_path)}")

if __name__ == "__main__":
    main()
