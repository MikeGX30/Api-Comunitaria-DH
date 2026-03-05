# API Comunitaria Dolores Hidalgo

Backend REST para apoyar digitalmente a la comunidad de Dolores Hidalgo, Guanajuato.

## 🚀 Inicio Rápido

### Requisitos
- Python 3.9+
- pip

### Instalación

```bash
# 1. Crear entorno virtual
python -m venv venv
source venv/bin/activate   # Linux/Mac
# venv\Scripts\activate    # Windows

# 2. Instalar dependencias de desarrollo
pip install -r requirements/dev.txt

# 3. Configurar variables de entorno
cp .env.example .env

# 4. Ejecutar
python run.py
```

La API quedará disponible en `http://localhost:5000`

## 📡 Endpoints

| Método | URL | Descripción |
|--------|-----|-------------|
| GET | /api/health/ | Estado de la API |
| GET | /api/health/ping | Ping |
| GET | /api/health/version | Versión y ambiente |
| GET | /api/artesanos/ | Listar artesanos |
| POST | /api/artesanos/ | Crear artesano |
| GET | /api/artesanos/{id} | Obtener artesano |
| PUT | /api/artesanos/{id} | Reemplazar artesano |
| PATCH | /api/artesanos/{id} | Actualizar parcialmente |
| DELETE | /api/artesanos/{id} | Eliminar artesano |

### Filtros disponibles (GET /api/artesanos/)
- `?oficio=Alfarería`
- `?comunidad=Rancho El Llanito`

## 🧪 Pruebas rápidas con curl

```bash
# Listar artesanos
curl http://localhost:5000/api/artesanos/

# Crear artesano
curl -X POST http://localhost:5000/api/artesanos/ \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Juan Pérez", "oficio": "Carpintero"}'

# Actualizar parcialmente
curl -X PATCH http://localhost:5000/api/artesanos/1 \
  -H "Content-Type: application/json" \
  -d '{"años_experiencia": 30}'

# Eliminar
curl -X DELETE http://localhost:5000/api/artesanos/3
```

## 📁 Estructura

```
app/
├── __init__.py          # Fábrica de la aplicación
├── config.py            # Configuración por ambiente
├── extensions.py        # Extensiones Flask (SQLAlchemy, etc.)
├── routes/              # Blueprints (endpoints HTTP)
├── services/            # Lógica de negocio
├── repositories/        # Acceso a datos
├── models/              # Modelos e interfaces
├── schemas/             # Validación y serialización
└── exceptions/          # Excepciones personalizadas
```

## 🗺️ Hoja de ruta

- **Bloque 1** ✅ — Fundamentos, arquitectura y primera API (este proyecto)
- **Bloque 2** — PostgreSQL y SQLAlchemy (datos persistentes)
- **Bloque 3** — Autenticación JWT y usuarios
- **Bloque 4** — MongoDB (reportes ciudadanos y eventos)
- **Bloque 5** — Pruebas, Swagger y Docker
- **Bloque 6** — Despliegue en producción
