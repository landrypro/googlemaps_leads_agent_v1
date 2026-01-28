from __future__ import annotations

import io
from datetime import datetime

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse

from .models import ExportRequest
from .places_client import PlacesClient
from .services.collector import collect_leads
from .services.exporter import export_to_xlsx

app = FastAPI(title="Google Maps Leads Agent V1", version="1.0")

@app.get("/health")
def health() -> dict:
    return {"status": "ok"}

@app.post("/api/leads/export-xlsx")
def export_xlsx(req: ExportRequest):
    try:
        client = PlacesClient()
        leads = collect_leads(
            client,
            query=req.query,
            center_lat=req.centerLat,
            center_lng=req.centerLng,
            radius_m=req.radiusMeters,
            limit=req.limit,
            enrich=req.enrich,
        )
    except Exception as e:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(e))

    # write to in-memory buffer using a temp workbook saved to bytes
    import tempfile, os
    with tempfile.TemporaryDirectory() as d:
        tmp_path = os.path.join(d, "leads.xlsx")
        export_to_xlsx(leads, tmp_path)
        data = open(tmp_path, "rb").read()

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"leads_{stamp}.xlsx"
    return StreamingResponse(
        io.BytesIO(data),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
