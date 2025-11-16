# 🚀 Quick Start Guide

## Podsumowanie projektu

AI Research Agent to kompletny system badawczy oparty na AI, który:
1. **Wyszukuje** informacje w internecie (Tavily API)
2. **Analizuje** je za pomocą GPT-4 (OpenAI API)
3. **Przechowuje** wyniki w bazie wektorowej (ChromaDB)
4. **Generuje** profesjonalne raporty PDF (ReportLab)

---

## ⚡ Szybki Start (3 kroki)

### 1. Sprawdź instalację
```powershell
python check_setup.py
```

### 2. Dodaj klucze API do `.env`
```env
OPENAI_API_KEY=sk-your-key-here
TAVILY_API_KEY=tvly-your-key-here
```

### 3. Uruchom serwer
```powershell
python start.py
```

**Gotowe!** API dostępne pod: http://localhost:8000

---

## 📚 Struktura Plików

```
Ai-Resercher-Agent-python/
│
├── backend/
│   ├── main.py                    # 🎯 Główna aplikacja FastAPI
│   └── src/
│       ├── services/
│       │   ├── agent.py          # 🤖 OpenAI GPT-4 Agent
│       │   ├── search.py         # 🔍 Tavily Web Search
│       │   ├── vector_store.py   # 💾 ChromaDB (RAG)
│       │   └── pdf_generator.py  # 📄 ReportLab PDF
│       └── models/
│           └── schemas.py        # 📋 Modele danych
│
├── config/
│   └── settings.py               # ⚙️ Konfiguracja
│
├── .env                          # 🔐 Klucze API (NIE COMMITUJ!)
├── requirements.txt              # 📦 Zależności Python
└── README.md                     # 📖 Pełna dokumentacja
```

---

## 🎓 Kluczowe Endpointy

| Endpoint | Co robi |
|----------|---------|
| `POST /research` | Przeprowadź badanie na dowolny temat |
| `POST /report` | Wygeneruj PDF z badania |
| `GET /history` | Zobacz historię badań |
| `GET /docs` | Interaktywna dokumentacja API |

---

## 💡 Przykład Użycia

### Python
```python
import requests

# 1. Przeprowadź badanie
response = requests.post("http://localhost:8000/research", json={
    "topic": "Artificial Intelligence in Healthcare",
    "depth": 3,
    "max_results": 10
})
research = response.json()
print(f"✅ Research ID: {research['research_id']}")

# 2. Wygeneruj raport PDF
report = requests.post("http://localhost:8000/report", json={
    "research_id": research['research_id']
})
print(f"📄 Report: {report.json()['download_url']}")
```

### cURL
```bash
# Badanie
curl -X POST "http://localhost:8000/research" \
  -H "Content-Type: application/json" \
  -d '{"topic": "AI in Healthcare", "depth": 3}'

# Raport
curl -X POST "http://localhost:8000/report" \
  -H "Content-Type: application/json" \
  -d '{"research_id": "res_abc123"}'
```

---

## 🔧 Przydatne Skrypty

| Skrypt | Opis |
|--------|------|
| `check_setup.py` | Sprawdź instalację wszystkich zależności |
| `start.py` | Uruchom serwer FastAPI |
| `test_api_example.py` | Przykładowe testy API |

---

## 📊 Technologie

- **FastAPI** - Nowoczesny, szybki framework web
- **OpenAI GPT-4** - Najpotężniejszy model językowy
- **Tavily** - Specjalizowany web search dla AI
- **ChromaDB** - Vector database z embeddings
- **ReportLab** - Generowanie PDF programatically

---

## 🎯 Use Cases

1. **Academic Research** - Szybkie przeglądy literatury
2. **Market Analysis** - Analiza trendów rynkowych
3. **Competitive Intelligence** - Monitoring konkurencji
4. **Content Research** - Przygotowanie artykułów
5. **Due Diligence** - Badanie firm/technologii

---

## 🐛 Troubleshooting

### Problem: ModuleNotFoundError
```powershell
# Reinstaluj zależności
pip install -r requirements.txt
```

### Problem: API Error
```
Sprawdź klucze w .env:
- OPENAI_API_KEY=sk-...
- TAVILY_API_KEY=tvly-...
```

### Problem: Port zajęty
```powershell
# Zmień port w .env
PORT=8080
```

---

## 📞 Wsparcie

- 📖 Pełna dokumentacja: `README.md`
- 🔧 API Examples: `API_EXAMPLES.md`
- 📡 Interactive Docs: http://localhost:8000/docs
- 🧪 Testy: `pytest tests/`

---

## ✅ Checklist przed uruchomieniem

- [ ] Python 3.11+ zainstalowany
- [ ] Zależności zainstalowane (`pip install -r requirements.txt`)
- [ ] Plik `.env` utworzony
- [ ] Klucze API dodane do `.env`
- [ ] Check setup przeszedł (`python check_setup.py`)

**Jeśli wszystko ✅ - uruchom `python start.py`!**

---

Made with ❤️ for recruitment purposes
