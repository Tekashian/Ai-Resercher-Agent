# 🧠 AI Research Agent

## Project Description

An intelligent research assistant powered by OpenAI GPT-4, combining web search capabilities, vector storage, and automated PDF report generation. This production-ready API enables autonomous research on any topic with comprehensive analysis and professional documentation.

## 🎯 Key Features

- **Automated Web Research** - Leverages Tavily API to gather up-to-date information from across the internet
- **AI-Powered Analysis** - Uses OpenAI GPT-4 to analyze, synthesize, and extract key insights from raw data
- **RAG System** - Implements Retrieval-Augmented Generation using ChromaDB for intelligent information storage and retrieval
- **PDF Report Generation** - Automatically creates professional, well-structured PDF reports with ReportLab
- **Research History** - Maintains complete history of all research with searchable vector database
- **RESTful API** - Clean, well-documented API with automatic interactive documentation (Swagger UI)

## 🛠 Technology Stack

| Technology | Purpose |
|-----------|---------|
| **Python 3.11+** | Core programming language |
| **FastAPI** | Modern, high-performance web framework |
| **OpenAI API (GPT-4)** | Natural language processing and analysis |
| **Tavily API** | Specialized web search engine for AI applications |
| **ChromaDB** | Vector database for embeddings and semantic search |
| **ReportLab** | Professional PDF document generation |
| **Pydantic** | Data validation and settings management |
| **Docker** | Containerization and deployment |

## 📋 Architecture

The project follows clean architecture principles with clear separation of concerns:

```
backend/
├── main.py                    # FastAPI application & routing
└── src/
    ├── services/
    │   ├── agent.py          # OpenAI GPT-4 integration
    │   ├── search.py         # Tavily web search
    │   ├── vector_store.py   # ChromaDB RAG implementation
    │   └── pdf_generator.py  # ReportLab PDF creation
    └── models/
        └── schemas.py        # Pydantic models & validation
```

## 🚀 How It Works

1. **User submits a research topic** via API endpoint
2. **System performs web search** using Tavily to gather relevant information
3. **AI analyzes the data** using GPT-4 to create structured insights
4. **Results are stored** in ChromaDB vector database for future retrieval
5. **PDF report is generated** with professional formatting and citations
6. **User receives** comprehensive research with downloadable PDF

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/research` | Conduct research on any topic |
| `POST` | `/report` | Generate PDF report from research |
| `GET` | `/history` | Retrieve research history |
| `GET` | `/research/{id}` | Get specific research details |
| `GET` | `/download/{file}` | Download PDF report |
| `GET` | `/search` | Search similar research |
| `GET` | `/docs` | Interactive API documentation |

## 💡 Use Cases

- **Academic Research** - Quick literature reviews and topic summaries
- **Market Analysis** - Competitive intelligence and market trends
- **Content Creation** - Research for articles, blogs, and presentations
- **Business Intelligence** - Company research and due diligence
- **Technology Assessment** - Evaluation of emerging technologies

## 🎓 Technical Highlights

- **Async/Await** - Efficient asynchronous operations throughout
- **Type Safety** - Full Pydantic model validation
- **Error Handling** - Comprehensive exception management
- **Docker Ready** - Containerized with docker-compose
- **Testing** - Unit tests with pytest
- **Documentation** - Complete API docs with Swagger UI
- **Clean Code** - Follows PEP 8 and best practices

## 📦 Quick Start

```bash
# Clone repository
git clone <repository-url>
cd Ai-Resercher-Agent-python

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Add your API keys to .env

# Run server
python start.py

# Visit API docs
open http://localhost:8000/docs
```

## 🔑 Required API Keys

- **OpenAI API Key** - Get from [platform.openai.com](https://platform.openai.com/api-keys)
- **Tavily API Key** - Get from [tavily.com](https://tavily.com) (1000 free queries/month)

## 🐳 Docker Deployment

```bash
docker-compose up --build
```

## 📊 Example Request

```python
import requests

response = requests.post("http://localhost:8000/research", json={
    "topic": "Latest developments in quantum computing",
    "depth": 3,
    "max_results": 10
})

research = response.json()
print(f"Research ID: {research['research_id']}")
print(f"Summary: {research['summary']}")
```

## 🎯 Project Goals

Built as a demonstration of:
- Modern Python web development with FastAPI
- Integration with cutting-edge AI APIs (OpenAI, Tavily)
- Vector database implementation (RAG pattern)
- Clean architecture and SOLID principles
- Production-ready code with proper error handling
- Comprehensive documentation and testing

## 📈 Future Enhancements

- Multi-language support
- WebSocket for real-time progress updates
- Advanced RAG with re-ranking
- Export to multiple formats (DOCX, Markdown)
- User authentication and API rate limiting
- Frontend interface (React/Vue)

## 📄 License

MIT License

## 👨‍💻 Author

Created as a portfolio project demonstrating full-stack development skills with modern AI technologies.

---

**Technologies**: Python • FastAPI • OpenAI GPT-4 • Tavily • ChromaDB • Vector Databases • RAG • PDF Generation • Docker • REST API

**Skills Demonstrated**: API Development • AI Integration • Vector Databases • Document Generation • Clean Architecture • Async Programming • Testing • Documentation
