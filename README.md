# 🏺 API Comunitaria Dolores Hidalgo

Backend REST para digitalizar y conectar a los artesanos, ciudadanos y dependencias del municipio de **Dolores Hidalgo, Guanajuato**.

> Proyecto del curso **Desarrollo de APIs** — Bloque 1: Fundamentos y Primera API

---

## 📋 Tabla de Contenidos

- [Descripción](#-descripción)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Endpoints](#-endpoints)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Validaciones](#-validaciones)
- [Códigos HTTP](#-códigos-http)
- [Datos de Prueba](#-datos-de-prueba)
- [Dependencias](#-dependencias)
- [Hoja de Ruta](#️-hoja-de-ruta)

---

## 📖 Descripción

Una API (Interfaz de Programación de Aplicaciones) actúa como traductor entre sistemas distintos. En el contexto de Dolores Hidalgo, permite que una app móvil, un sitio web o un kiosco de información se comuniquen con el mismo backend sin importar en qué tecnología estén construidos.

Este proyecto implementa una arquitectura **REST con Flask**, siguiendo el principio de separación de responsabilidades en capas:

```
Petición HTTP → Rutas → Servicios → Repositorio → Datos
```

### ¿Qué problema resuelve?

- Los artesanos locales no tienen visibilidad digital para ofrecer sus productos
- Los ciudadanos no tienen un canal unificado para reportar problemas
- Diferentes sistemas necesitan comunicarse con el mismo backend

---

## 🚀 Instalación

### Requisitos

- Python 3.9+
- pip

### Pasos

```bash
# 1. Clonar o descomprimir el proyecto
cd api-comunitaria-dolores

# 2. Crear entorno virtual
python -m venv venv

# Linux / Mac
source venv/bin/activate

# Windows
venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements/dev.txt

# 4. Configurar variables de entorno
cp .env.example .env

# 5. Ejecutar
python run.py
```

La API queda disponible en `http://localhost:5000`

### Variables de entorno (`.env`)

| Variable | Default | Descripción |
|----------|---------|-------------|
| `FLASK_CONFIG` | `dev` | Ambiente: `dev`, `prod`, `test` |
| `PORT` | `5000` | Puerto del servidor |
| `SECRET_KEY` | `dev-secret-key-...` | Clave secreta para sesiones |
| `LOG_LEVEL` | `INFO` | Nivel de logs: `DEBUG`, `INFO`, `ERROR` |
| `LOG_FILE` | `logs/api.log` | Ruta del archivo de logs |
| `DATABASE_URL` | `postgresql://...` | URL de PostgreSQL (Bloque 2) |

---

## 💻 Uso

### Ejemplos con `curl`

```bash
# Verificar que la API está corriendo
curl http://localhost:5000/api/health/

# Listar todos los artesanos
curl http://localhost:5000/api/artesanos/

# Filtrar por oficio
curl "http://localhost:5000/api/artesanos/?oficio=Alfarería"

# Filtrar por comunidad
curl "http://localhost:5000/api/artesanos/?comunidad=Rancho El Llanito"

# Crear un artesano
curl -X POST http://localhost:5000/api/artesanos/ \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Juan Pérez", "oficio": "Carpintero", "comunidad": "Centro"}'

# Obtener artesano por ID
curl http://localhost:5000/api/artesanos/1

# Actualización parcial (PATCH)
curl -X PATCH http://localhost:5000/api/artesanos/1 \
  -H "Content-Type: application/json" \
  -d '{"años_experiencia": 30}'

# Reemplazo completo (PUT)
curl -X PUT http://localhost:5000/api/artesanos/1 \
  -H "Content-Type: application/json" \
  -d '{"nombre":"María", "oficio":"Alfarería", "comunidad":"El Llanito", "años_experiencia":26, "activo":true}'

# Eliminar artesano
curl -X DELETE http://localhost:5000/api/artesanos/3
```

### Formato de respuesta exitosa

```json
{
  "success": true,
  "message": "Listado completo de artesanos",
  "data": [
    {
      "id": 1,
      "nombre": "María Guadalupe Sánchez",
      "oficio": "Alfarería",
      "comunidad": "Rancho El Llanito",
      "años_experiencia": 25,
      "activo": true
    }
  ],
  "total": 1
}
```

### Formato de respuesta de error

```json
{
  "success": false,
  "error": "ValidationError",
  "message": "Error de validación",
  "status_code": 400,
  "validation_errors": {
    "años_experiencia": ["No puede ser negativo"]
  }
}
```

---

## 📡 Endpoints

### Health / Estado

| Método | URL | Descripción |
|--------|-----|-------------|
| `GET` | `/api/health/` | Estado general de la API |
| `GET` | `/api/health/ping` | Ping simple |
| `GET` | `/api/health/version` | Versión, proyecto y ambiente activo |

### Artesanos

| Método | URL | Descripción | Código |
|--------|-----|-------------|--------|
| `GET` | `/api/artesanos/` | Listar todos los artesanos activos | `200` |
| `POST` | `/api/artesanos/` | Crear un nuevo artesano | `201` |
| `GET` | `/api/artesanos/{id}` | Obtener un artesano por ID | `200` |
| `PUT` | `/api/artesanos/{id}` | Reemplazar todos los campos | `200` |
| `PATCH` | `/api/artesanos/{id}` | Actualizar solo los campos enviados | `200` |
| `DELETE` | `/api/artesanos/{id}` | Eliminar un artesano | `204` |

**Parámetros de consulta disponibles en `GET /api/artesanos/`:**
- `?oficio=Alfarería`
- `?comunidad=Rancho El Llanito`

---

## 📁 Estructura del Proyecto

```
api-comunitaria-dolores/
├── app/
│   ├── __init__.py                      # Fábrica de la aplicación (create_app)
│   ├── config.py                        # Configuración por ambiente
│   ├── extensions.py                    # Extensiones Flask (SQLAlchemy, etc.)
│   ├── routes/                          # Capa de presentación (blueprints)
│   │   ├── health.py                    # Endpoints de salud
│   │   ├── artesanos.py                 # CRUD completo de artesanos
│   │   └── errors.py                    # Manejadores de errores HTTP
│   ├── services/
│   │   └── artesano_service.py          # Lógica de negocio
│   ├── repositories/
│   │   └── artesano_repository_impl.py  # Repositorio en memoria
│   ├── models/
│   │   ├── dummy_data.py                # Datos de prueba
│   │   └── interfaces/
│   │       └── artesano_repository.py   # Contrato abstracto (ABC)
│   ├── schemas/
│   │   └── artesano_schema.py           # Validación y serialización (DTOs)
│   └── exceptions/
│       └── api_exceptions.py            # Excepciones personalizadas
├── requirements/
│   ├── base.txt                         # Flask, python-dotenv
│   ├── dev.txt                          # + black, flake8, pytest
│   └── prod.txt                         # + gunicorn, SQLAlchemy
├── logs/                                # Archivos de log (auto-generado)
├── run.py                               # Punto de entrada
├── .env.example                         # Plantilla de configuración
└── .gitignore
```

### Rol de cada capa

| Capa | Carpeta | Responsabilidad |
|------|---------|-----------------|
| Presentación | `routes/` | Recibe peticiones HTTP, extrae parámetros, delega al servicio |
| Negocio | `services/` | Reglas de negocio, validaciones y orquestación |
| Datos | `repositories/` | Acceso y manipulación de los datos |
| DTOs | `schemas/` | Valida tipos, aplica defaults, serializa a JSON |
| Errores | `exceptions/` | Jerarquía de errores → respuestas JSON con código HTTP correcto |

---

## ✅ Validaciones

### Campos del modelo Artesano

| Campo | Tipo | Requerido | Restricciones |
|-------|------|-----------|---------------|
| `nombre` | `string` | ✅ Sí | No puede estar vacío |
| `oficio` | `string` | ✅ Sí | No puede estar vacío |
| `comunidad` | `string` | No | Default: `"No especificada"` |
| `años_experiencia` | `integer` | No | Entre `0` y `100`. Default: `0` |
| `activo` | `boolean` | No | Default: `true` |

### Reglas de negocio

- No se puede crear un artesano con el mismo nombre en la misma comunidad → `409 Conflict`
- `años_experiencia` no puede ser negativo ni superar 100 → `400 Bad Request`
- Tipo de dato incorrecto en cualquier campo → `400` con detalle del campo que falló
- **PUT** requiere todos los campos (reemplazo completo)
- **PATCH** acepta solo los campos que se quieran modificar

---

## 🔢 Códigos HTTP

| Código | Nombre | Cuándo ocurre |
|--------|--------|---------------|
| `200` | OK | GET, PUT, PATCH exitosos |
| `201` | Created | POST exitoso — artesano creado |
| `204` | No Content | DELETE exitoso (sin cuerpo) |
| `400` | Bad Request | JSON inválido o campos incorrectos |
| `404` | Not Found | Artesano con ese ID no existe |
| `405` | Method Not Allowed | Verbo HTTP no soportado en esa URL |
| `409` | Conflict | Artesano duplicado |
| `422` | Unprocessable Entity | Violación de regla de negocio |
| `500` | Internal Server Error | Error inesperado del servidor |

---

## 🧪 Datos de Prueba

Al iniciar la API se cargan automáticamente en memoria, sin necesitar base de datos:

| ID | Nombre | Oficio | Comunidad | Años | Activo |
|----|--------|--------|-----------|------|--------|
| 1 | María Guadalupe Sánchez | Alfarería | Rancho El Llanito | 25 | ✅ |
| 2 | José Luis Hernández | Trabajo en cuero | Dolores Hidalgo Centro | 15 | ✅ |
| 3 | Petra Cortés | Textiles | Rancho La Erre | 40 | ❌ |

> `GET /api/artesanos/` solo retorna artesanos con `activo: true`, por eso el listado inicial muestra 2.

---

## 📦 Dependencias

### Desarrollo (`requirements/dev.txt`)

| Paquete | Versión | Para qué sirve |
|---------|---------|----------------|
| Flask | 2.3.3 | Framework web principal |
| python-dotenv | 1.0.0 | Carga variables de entorno desde `.env` |
| black | 23.9.1 | Formateador automático de código |
| flake8 | 6.1.0 | Linter — detecta errores y malos estilos |
| pytest | 7.4.0 | Framework de pruebas unitarias |

### Producción (`requirements/prod.txt`)

| Paquete | Versión | Para qué sirve |
|---------|---------|----------------|
| gunicorn | 21.2.0 | Servidor WSGI para producción |
| psycopg2-binary | 2.9.7 | Driver de PostgreSQL |
| SQLAlchemy | 2.0.21 | ORM para base de datos relacional |
| Flask-SQLAlchemy | 3.1.1 | Integración SQLAlchemy + Flask |
| Flask-Migrate | 4.0.5 | Migraciones de base de datos |

---

## 🗺️ Hoja de Ruta

| Bloque | Tema | Estado |
|--------|------|--------|
| 1 | Fundamentos y Primera API | ✅ Completo |
| 2 | PostgreSQL y SQLAlchemy | ⏳ Pendiente |
| 3 | Autenticación con JWT | ⏳ Pendiente |
| 4 | MongoDB (reportes y eventos) | ⏳ Pendiente |
| 5 | Pruebas, Swagger y Docker | ⏳ Pendiente |
| 6 | Despliegue en producción | ⏳ Pendiente |

> La arquitectura actual está preparada para el Bloque 2: solo se reemplaza el repositorio en memoria por uno de SQLAlchemy, sin tocar rutas ni servicios.

---

*"La tecnología no vale nada si no sirve para conectar personas y fortalecer comunidades."*
