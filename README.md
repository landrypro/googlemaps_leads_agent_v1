# Google Maps Leads Agent V1 (Python)

Ce projet récupère des entreprises via **Google Places API (New)** et exporte un fichier **Excel (.xlsx)** avec:
- Nom, Adresse, Téléphone, Site web, URL Google Maps, Latitude/Longitude, PlaceId

✅ Inclus:
- **Text Search (New)** avec pagination (20 résultats/page)
- **Déduplication** par PlaceId
- **Enrichissement optionnel** via Place Details (New) pour téléphone/site web
- **Backoff / retries** (simple) sur erreurs/transitoires
- Deux façons d'utiliser:
  1) **CLI** (recommandé pour tester vite)
  2) **API FastAPI** (endpoint qui renvoie le .xlsx)

> Important: vous devez avoir une clé Google Maps Platform avec Places API activée.

---

## 1) Installation

### Prérequis
- Python 3.10+

### Installer les dépendances
```bash
pip install -r requirements.txt
```

### Configurer la clé API
Créez un fichier `.env` à la racine (ou exportez la variable d'environnement):
```bash
cp .env.example .env
```

Dans `.env`, renseignez:
```
GOOGLE_MAPS_API_KEY=VOTRE_CLE_ICI
```

---

## 2) Utilisation en ligne de commande (CLI)

Exemple (centre-ville de Québec, rayon 50 km, plomberie, 500 max):
```bash
python -m app.cli \
  --query "plombier" \
  --center-lat 46.8139 \
  --center-lng -71.2080 \
  --radius-m 50000 \
  --limit 500 \
  --enrich false \
  --out leads_quebec_plomberie.xlsx
```

### Astuce
Essayez aussi:
- `--query "plomberie"`
- `--query "plombier Québec"`

---

## 3) Utilisation via API (FastAPI)

Lancer l'API:
```bash
uvicorn app.api:app --host 0.0.0.0 --port 8000
```

Tester l'endpoint:
- POST `http://localhost:8000/api/leads/export-xlsx`

Body JSON exemple:
```json
{
  "query": "plombier",
  "centerLat": 46.8139,
  "centerLng": -71.2080,
  "radiusMeters": 50000,
  "limit": 500,
  "enrich": false
}
```

La réponse est un fichier `.xlsx`.

---

## 4) Notes sur les quotas / coûts
- Text Search renvoie **jusqu'à 20** résultats par page.
- Pour obtenir téléphone/site web manquants, `enrich=true` déclenche des appels Place Details par placeId (plus d'appels donc plus de coût).

---

## 5) Dépannage
- Si vous avez une erreur 403/permission, vérifiez:
  - Places API activée dans Google Cloud
  - Facturation activée
  - Restrictions de clé (API/HTTP referrers) compatibles avec votre usage

---

## 6) Structure
- `app/places_client.py`: client HTTP Places API (New)
- `app/services/collector.py`: collecte + pagination + dédup
- `app/services/exporter.py`: export Excel
- `app/cli.py`: utilisation CLI
- `app/api.py`: API FastAPI

Bon test !
