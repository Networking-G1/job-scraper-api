# 🎓 Job Scraper API - Prácticas Profesionales

API REST desarrollada con FastAPI para recolectar, almacenar y consultar ofertas de trabajo orientadas a prácticas profesionales y pre-prácticas para estudiantes universitarios.

## 📋 Tabla de Contenidos

- [Características](#características)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Uso](#uso)
- [Endpoints de la API](#endpoints-de-la-api)
- [Modelo de Datos](#modelo-de-datos)
- [Web Scraping](#web-scraping)
- [Desarrollo](#desarrollo)
- [Roadmap](#roadmap)

## ✨ Características

- ✅ API REST completa con FastAPI
- ✅ Base de datos SQLite con SQLAlchemy ORM
- ✅ Web scraping modular y extensible
- ✅ Filtros avanzados de búsqueda
- ✅ Documentación automática (Swagger/ReDoc)
- ✅ Procesamiento en background
- ✅ Estadísticas de ofertas
- ✅ CORS habilitado para frontends

## 📁 Estructura del Proyecto

```
job-scraper-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # Aplicación principal FastAPI
│   ├── database.py          # Configuración de base de datos
│   ├── models.py            # Modelos SQLAlchemy
│   ├── schemas.py           # Esquemas Pydantic
│   ├── crud.py              # Operaciones CRUD
│   ├── scraper/
│   │   ├── __init__.py
│   │   ├── base_scraper.py      # Clase base abstracta
│   │   └── linkedin_scraper.py  # Scraper específico
│   └── routers/
│       ├── __init__.py
│       └── jobs.py          # Endpoints de trabajos
├── requirements.txt         # Dependencias Python
├── .env.example            # Variables de entorno ejemplo
├── .gitignore
└── README.md
```

## 🚀 Instalación

### Prerrequisitos

- Python 3.8 o superior
- pip (gestor de paquetes Python)

### Pasos de Instalación

1. **Clonar o crear el proyecto**

```bash
mkdir job-scraper-api
cd job-scraper-api
```

2. **Crear entorno virtual**

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Instalar dependencias**

```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**

```bash
cp .env.example .env
# Editar .env según necesites
```

## ⚙️ Configuración

### Variables de Entorno

Crear archivo `.env` en la raíz del proyecto:

```env
DATABASE_URL=sqlite:///./jobs.db
API_HOST=0.0.0.0
API_PORT=8000
```

## 🎯 Uso

### Iniciar el servidor

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

La API estará disponible en: `http://localhost:8000`
La API estará disponible en: `http://localhost:8001`

### Documentación Interactiva

- **Swagger UI**: http://localhost:8000/docs
- **Swagger UI**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8000/redoc

## 📡 Endpoints de la API

### Health Check

```http
GET /health
```

Verifica el estado de la API.

**Respuesta:**
```json
{
  "status": "healthy"
}
```

---

### Obtener Ofertas de Trabajo

```http
GET /jobs/
```

**Parámetros de consulta:**

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| skip | int | Número de registros a saltar (default: 0) |
| limit | int | Límite de registros (default: 100) |
| location | string | Filtrar por ubicación |
| company_name | string | Filtrar por nombre de empresa |
| remote_allowed | boolean | Filtrar trabajos remotos |
| experience_level | string | Filtrar por nivel de experiencia |
| search | string | Búsqueda en título, descripción y habilidades |

**Ejemplo:**

```bash
curl "http://localhost:8000/jobs/?location=Lima&remote_allowed=true&limit=10"
```

**Respuesta:**
```json
[
  {
    "id": 1,
    "company_name": "Tech Innovators Inc",
    "title": "Practicante de Desarrollo Web",
    "description": "Buscamos estudiante universitario...",
    "location": "Lima, Perú",
    "remote_allowed": true,
    "min_salary": 800.0,
    "max_salary": 1500.0,
    "currency": "PEN",
    "job_posting_url": "https://...",
    ...
  }
]
```

---

### Obtener Oferta Específica

```http
GET /jobs/{job_id}
```

**Ejemplo:**

```bash
curl http://localhost:8000/jobs/1
```

---

### Crear Oferta de Trabajo

```http
POST /jobs/
```

**Body (JSON):**

```json
{
  "company_name": "Tech Company",
  "title": "Practicante de Desarrollo",
  "description": "Descripción de la práctica...",
  "location": "Lima, Perú",
  "job_posting_url": "https://example.com/job/123",
  "remote_allowed": true,
  "min_salary": 800,
  "max_salary": 1200,
  "currency": "PEN",
  "formatted_experience_level": "Internship"
}
```

**Ejemplo con curl:**

```bash
curl -X POST "http://localhost:8000/jobs/" \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "Tech Company",
    "title": "Practicante Backend",
    "description": "Práctica en desarrollo backend",
    "location": "Remoto",
    "job_posting_url": "https://example.com/job/456",
    "remote_allowed": true
  }'
```

---

### Actualizar Oferta

```http
PUT /jobs/{job_id}
```

---

### Eliminar Oferta

```http
DELETE /jobs/{job_id}
```

---

### Obtener Estadísticas

```http
GET /jobs/statistics
```

**Respuesta:**
```json
{
  "total_jobs": 150,
  "remote_jobs": 85,
  "average_salary": 1150.50
}
```

---

### Iniciar Scraping

```http
POST /jobs/scrape
```

**Parámetros de consulta:**

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| keywords | string | Palabras clave separadas por comas |
| location | string | Ubicación para buscar |

**Ejemplo:**

```bash
curl -X POST "http://localhost:8000/jobs/scrape?keywords=practicas,desarrollo,python&location=Lima"
```

**Respuesta:**
```json
{
  "message": "Scraping initiated in background",
  "keywords": "practicas,desarrollo,python",
  "location": "Lima"
}
```

## 💾 Modelo de Datos

### Tabla: job_postings

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | Integer | ID único (Primary Key) |
| company_name | String | Nombre de la empresa |
| title | String | Título de la oferta |
| description | String | Descripción completa |
| max_salary | Float | Salario máximo |
| min_salary | Float | Salario mínimo |
| med_salary | Float | Salario medio |
| pay_period | String | Período de pago (Monthly, Hourly, etc.) |
| location | String | Ubicación |
| company_id | String | ID de la empresa en la fuente |
| views | Integer | Número de visualizaciones |
| formatted_work_type | String | Tipo de trabajo formateado |
| applies | Integer | Número de aplicaciones |
| original_listed_time | DateTime | Fecha original de publicación |
| remote_allowed | Boolean | Si permite trabajo remoto |
| job_posting_url | String | URL de la oferta (unique) |
| application_url | String | URL de aplicación |
| application_type | String | Tipo de aplicación |
| expiry | DateTime | Fecha de expiración |
| closed_time | DateTime | Fecha de cierre |
| formatted_experience_level | String | Nivel de experiencia |
| skills_desc | String | Descripción de habilidades |
| listed_time | DateTime | Fecha de listado |
| posting_domain | String | Dominio de publicación |
| sponsored | Boolean | Si es patrocinada |
| work_type | String | Tipo de trabajo |
| currency | String | Moneda del salario |
| compensation_type | String | Tipo de compensación |
| normalized_salary | Float | Salario normalizado |
| zip_code | String | Código postal |
| fips | String | Código FIPS |
| created_at | DateTime | Fecha de creación en DB |
| updated_at | DateTime | Fecha de última actualización |

## 🕷️ Web Scraping

### Arquitectura del Scraper

El proyecto utiliza un patrón de diseño con clase base abstracta que permite implementar múltiples scrapers para diferentes fuentes.

#### Clase Base: `BaseScraper`

```python
from app.scraper.base_scraper import BaseScraper

class MiScraper(BaseScraper):
    def scrape_jobs(self, keywords, location):
        # Implementación específica
        pass
```

### Agregar Nuevo Scraper

1. **Crear nuevo archivo** en `app/scraper/`

```python
# app/scraper/indeed_scraper.py
from .base_scraper import BaseScraper
from typing import List, Dict

class IndeedScraper(BaseScraper):
    def __init__(self):
        super().__init__("https://www.indeed.com")
    
    def scrape_jobs(self, keywords: List[str], location: str = "") -> List[Dict]:
        # Tu lógica de scraping aquí
        jobs = []
        
        # Ejemplo de estructura de retorno
        for job in scraped_data:
            jobs.append({
                "company_name": "...",
                "title": "...",
                "description": "...",
                "location": location,
                "job_posting_url": "...",
                # ... otros campos
            })
        
        return jobs
```

2. **Usar el nuevo scraper** en `app/routers/jobs.py`

```python
from ..scraper.indeed_scraper import IndeedScraper

# En el endpoint /scrape
scraper = IndeedScraper()
jobs = scraper.scrape_jobs(keywords.split(","), location)
```

### Consideraciones de Scraping

⚠️ **Importante:**

1. **Legalidad**: Verifica los términos de servicio del sitio
2. **Rate Limiting**: Implementa delays entre requests
3. **User-Agent**: Usa user agents realistas
4. **Robots.txt**: Respeta las reglas de robots.txt
5. **APIs Oficiales**: Prioriza APIs oficiales cuando estén disponibles

### Alternativas Recomendadas

Para producción, considera:

- **LinkedIn Jobs API** (requiere aprobación)
- **Indeed API** (Partner Program)
- **ScraperAPI** (servicio de proxy)
- **Selenium** con modo headless para sitios dinámicos
- **Puppeteer/Playwright** para JavaScript rendering

## 🛠️ Desarrollo

### Ejecutar Tests

```bash
# Instalar pytest
pip install pytest pytest-asyncio httpx

# Ejecutar tests
pytest
```

### Ejemplo de Test

```python
# test_jobs.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_jobs():
    response = client.get("/jobs/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_statistics():
    response = client.get("/jobs/statistics")
    assert response.status_code == 200
    assert "total_jobs" in response.json()
```

### Estructura de Desarrollo

```bash
# Crear nueva rama
git checkout -b feature/nueva-funcionalidad

# Hacer cambios
git add .
git commit -m "Descripción del cambio"

# Push
git push origin feature/nueva-funcionalidad
```

## 📚 Ejemplos de Uso con Python

### Cliente Python Básico

```python
import requests

BASE_URL = "http://localhost:8000"

# Obtener todas las ofertas
response = requests.get(f"{BASE_URL}/jobs/")
jobs = response.json()
print(f"Total de ofertas: {len(jobs)}")

# Buscar ofertas remotas en Lima
params = {
    "location": "Lima",
    "remote_allowed": True,
    "limit": 10
}
response = requests.get(f"{BASE_URL}/jobs/", params=params)
remote_jobs = response.json()

# Crear nueva oferta
new_job = {
    "company_name": "Mi Empresa",
    "title": "Practicante Python",
    "description": "Descripción...",
    "location": "Lima",
    "job_posting_url": "https://example.com/job/789",
    "remote_allowed": True
}
response = requests.post(f"{BASE_URL}/jobs/", json=new_job)
created_job = response.json()
print(f"Oferta creada con ID: {created_job['id']}")

# Iniciar scraping
response = requests.post(
    f"{BASE_URL}/jobs/scrape",
    params={"keywords": "python,practicas", "location": "Lima"}
)
print(response.json())
```

## 🗺️ Roadmap

### Versión 1.1
- [ ] Autenticación JWT
- [ ] Rate limiting por IP
- [ ] Paginación mejorada
- [ ] Cache con Redis
- [ ] Scraper para Indeed

### Versión 1.2
- [ ] WebSocket para actualizaciones en tiempo real
- [ ] Sistema de notificaciones
- [ ] Exportar a CSV/Excel
- [ ] Dashboard con métricas

### Versión 2.0
- [ ] Machine Learning para categorización automática
- [ ] Recomendaciones personalizadas
- [ ] Frontend con React/Vue
- [ ] Dockerización completa
- [ ] Deploy en cloud (AWS/GCP/Azure)

## 🤝 Contribuir

1. Fork el proyecto
2. Crea tu rama de feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto es de código abierto y está disponible bajo la [MIT License](LICENSE).

## 📧 Contacto

Para preguntas o sugerencias, abre un issue en el repositorio.

---

**¡Happy Coding! 🚀**