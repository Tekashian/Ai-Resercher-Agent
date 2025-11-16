# API Testing Commands (curl)

## 1. Health Check
```bash
curl http://localhost:8000/health
```

## 2. Root Endpoint
```bash
curl http://localhost:8000/
```

## 3. Conduct Research
```bash
curl -X POST "http://localhost:8000/research" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Latest developments in quantum computing",
    "depth": 3,
    "max_results": 10
  }'
```

## 4. Generate Report
```bash
curl -X POST "http://localhost:8000/report" \
  -H "Content-Type: application/json" \
  -d '{
    "research_id": "res_abc123xyz",
    "format": "pdf",
    "include_sources": true
  }'
```

## 5. Get Research History
```bash
curl "http://localhost:8000/history?limit=5"
```

## 6. Get Specific Research
```bash
curl "http://localhost:8000/research/res_abc123xyz"
```

## 7. Search Similar Research
```bash
curl "http://localhost:8000/search?query=quantum+computing&limit=5"
```

## 8. Download PDF Report
```bash
curl -O "http://localhost:8000/download/report_rpt_def456uvw_20251116_120500.pdf"
```

---

## PowerShell Equivalents

### Health Check
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get
```

### Conduct Research
```powershell
$body = @{
    topic = "Latest developments in quantum computing"
    depth = 3
    max_results = 10
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/research" -Method Post -Body $body -ContentType "application/json"
```

### Generate Report
```powershell
$body = @{
    research_id = "res_abc123xyz"
    format = "pdf"
    include_sources = $true
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/report" -Method Post -Body $body -ContentType "application/json"
```

### Get History
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/history?limit=5" -Method Get
```

---

## Python Example

```python
import requests

# Conduct research
response = requests.post(
    "http://localhost:8000/research",
    json={
        "topic": "Latest developments in quantum computing",
        "depth": 3,
        "max_results": 10
    }
)
research_data = response.json()
print(f"Research ID: {research_data['research_id']}")

# Generate report
report_response = requests.post(
    "http://localhost:8000/report",
    json={
        "research_id": research_data['research_id'],
        "format": "pdf",
        "include_sources": True
    }
)
report_data = report_response.json()
print(f"Report URL: http://localhost:8000{report_data['download_url']}")
```
