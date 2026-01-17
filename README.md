# ⚖️ Judicial Monitor API

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

**Technologies:** Python | FastAPI | PostgreSQL | SQLAlchemy | Docker | Pytest

A comprehensive monitoring system for tracking publications in Official Court Gazettes (Diários Oficiais de Tribunais). This API provides automated monitoring, filtering, and notification capabilities for legal publications across multiple Brazilian court systems.

## ✅ Features

- Real-time monitoring of official court publications
- Advanced filtering and search capabilities
- Publication history and tracking
- RESTful API with automatic documentation
- Containerized deployment with Docker
- Database migrations with Alembic
- Comprehensive test coverage
- Health check endpoints

## 🧱 Project Structure

```
judicial-monitor/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── endpoints/
│   │   │   │   └── publications.py     # Publication endpoints
│   │   │   └── router.py               # API router
│   │   └── deps.py                     # Dependencies
│   ├── core/
│   │   ├── config.py                   # Configuration settings
│   │   └── database.py                 # Database connection
│   ├── models/
│   │   └── publication.py              # Publication model
│   ├── schemas/
│   │   └── publication.py              # Pydantic schemas
│   └── main.py                         # Application entry point
├── alembic/
│   ├── versions/                       # Database migrations
│   └── env.py                          # Alembic configuration
├── tests/
│   ├── test_publications.py            # Publication tests
│   └── conftest.py                     # Test configuration
├── docker-compose.yml                  # Docker services
├── Dockerfile                          # Application container
├── requirements.txt                    # Python dependencies
├── setup_project.py                    # Project setup script
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.11+ (for local development)
- Git

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/your-username/judicial-monitor.git
cd judicial-monitor
```

2. **Create project structure:**
```bash
python setup_project.py
```

3. **Start Docker containers:**
```bash
docker-compose up -d
```

4. **Run database migrations:**
```bash
docker-compose exec app alembic upgrade head
```

5. **Access the API:**
- API Documentation (Swagger): http://localhost:8000/docs
- Alternative Documentation (ReDoc): http://localhost:8000/redoc
- Health Check: http://localhost:8000/health

## 📚 API Endpoints

### Documentation
- `GET /docs` - Interactive Swagger documentation
- `GET /redoc` - Alternative ReDoc documentation

### Health & Status
- `GET /health` - API health check

### Publications
- `GET /api/v1/publications/` - List all publications
  - Query parameters: `skip`, `limit`, `court`, `date_from`, `date_to`
- `GET /api/v1/publications/{id}` - Get publication details
- `POST /api/v1/publications/` - Create new publication (admin)
- `PUT /api/v1/publications/{id}` - Update publication (admin)
- `DELETE /api/v1/publications/{id}` - Delete publication (admin)

### Example Request
```bash
# List publications with filters
curl -X GET "http://localhost:8000/api/v1/publications/?court=STF&limit=10" \
  -H "accept: application/json"

# Get specific publication
curl -X GET "http://localhost:8000/api/v1/publications/1" \
  -H "accept: application/json"
```

## 🛠️ Useful Commands

### Docker Management
```bash
# View logs (all services)
docker-compose logs -f

# View logs (specific service)
docker-compose logs -f app

# Stop containers
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Rebuild containers
docker-compose up -d --build

# Check container status
docker-compose ps
```

### Development
```bash
# Access application shell
docker-compose exec app bash

# Run tests
docker-compose exec app pytest

# Run tests with coverage
docker-compose exec app pytest --cov=app tests/

# Create new migration
docker-compose exec app alembic revision --autogenerate -m "description"

# Apply migrations
docker-compose exec app alembic upgrade head

# Rollback migration
docker-compose exec app alembic downgrade -1
```

### Database
```bash
# Access PostgreSQL
docker-compose exec db psql -U postgres -d judicial_monitor

# Backup database
docker-compose exec db pg_dump -U postgres judicial_monitor > backup.sql

# Restore database
docker-compose exec -T db psql -U postgres judicial_monitor < backup.sql
```

## 🧪 Testing

Run the complete test suite:
```bash
docker-compose exec app pytest -v
```

Run with coverage report:
```bash
docker-compose exec app pytest --cov=app --cov-report=html tests/
```

Test specific file:
```bash
docker-compose exec app pytest tests/test_publications.py -v
```

## 🔧 Configuration

Environment variables can be configured in `docker-compose.yml` or `.env` file:

```env
# Database
DATABASE_URL=postgresql://user:password@db:5432/judicial_monitor

# API
API_V1_PREFIX=/api/v1
PROJECT_NAME=Judicial Monitor API

# Security (for production)
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 📊 Monitored Courts

The system can monitor publications from:
- STF (Supremo Tribunal Federal)
- STJ (Superior Tribunal de Justiça)
- TST (Tribunal Superior do Trabalho)
- TRF (Tribunais Regionais Federais)
- TRT (Tribunais Regionais do Trabalho)
- TJ (Tribunais de Justiça Estaduais)

## 🏗️ Architecture

### Technology Stack
- **Framework:** FastAPI - Modern, fast web framework for building APIs
- **Database:** PostgreSQL - Robust relational database
- **ORM:** SQLAlchemy - Python SQL toolkit and ORM
- **Migrations:** Alembic - Database migration tool
- **Validation:** Pydantic - Data validation using Python type annotations
- **Testing:** Pytest - Testing framework
- **Containerization:** Docker & Docker Compose

### Design Patterns
- Repository Pattern for data access
- Dependency Injection for service management
- Schema validation with Pydantic models
- Layered architecture (API, Business Logic, Data Access)

## 🚀 Deployment

### Production Checklist
- [ ] Set strong `SECRET_KEY` in environment variables
- [ ] Enable HTTPS/SSL
- [ ] Configure CORS for specific origins
- [ ] Set up database backups
- [ ] Configure logging and monitoring
- [ ] Set up rate limiting
- [ ] Enable authentication/authorization
- [ ] Configure firewall rules
- [ ] Set up CI/CD pipeline

### Docker Production Build
```bash
docker-compose -f docker-compose.prod.yml up -d
```

## 📝 Development Guidelines

### Code Style
- Follow PEP 8 style guide
- Use type hints
- Write docstrings for functions and classes
- Keep functions small and focused

### Git Workflow
```bash
# Create feature branch
git checkout -b feature/new-feature

# Commit changes
git add .
git commit -m "feat: add new feature"

# Push and create PR
git push origin feature/new-feature
```

## 🐛 Troubleshooting

### Common Issues

**Port already in use:**
```bash
# Check what's using port 8000
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill the process or change port in docker-compose.yml
```

**Database connection errors:**
```bash
# Check if database container is running
docker-compose ps

# Restart database
docker-compose restart db

# Check database logs
docker-compose logs db
```

**Migration issues:**
```bash
# Reset database (WARNING: destroys data)
docker-compose down -v
docker-compose up -d
docker-compose exec app alembic upgrade head
```

## 📄 License

This project is licensed under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📧 Contact

For questions or support, please open an issue in the GitHub repository.

---

**Note:** This project was developed to provide an efficient solution for monitoring legal publications across Brazilian court systems, helping legal professionals stay updated with relevant information.
