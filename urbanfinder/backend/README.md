# 🏙️ UrbanFinder — Rental Platform Backend

A **scalable, production-ready REST API** for a rental property platform built with Django and Django REST Framework. Designed to power both mobile (Android) and web clients with a clean, modular architecture.

---

## 📋 Table of Contents

- [About the Project](#-about-the-project)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [App Modules](#-app-modules)
- [Getting Started](#-getting-started)
- [Environment Variables](#-environment-variables)
- [API Endpoints](#-api-endpoints)
- [Authentication](#-authentication)
- [Role-Based Access Control](#-role-based-access-control)
- [Connecting a Frontend](#-connecting-a-frontend)
- [Database Schema Overview](#-database-schema-overview)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🔍 About the Project

**UrbanFinder** is a full-stack rental listing platform where:

- **Tenants (USER role)** can browse properties, bookmark favorites, write reviews, and chat with property owners.
- **Property Owners (OWNER role)** can list rental properties, upload images, manage their listings, and submit verification documents.
- **Admins (ADMIN role)** can review and approve property verification documents, manage users, and oversee the platform.

The backend is an **API-first** system — it has no frontend templates. All data is served via JSON REST endpoints, making it easy to connect any frontend framework (React, Angular, Flutter, Android, etc.).

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **Python 3.12+** | Programming language |
| **Django 5.1** | Web framework |
| **Django REST Framework 3.15** | RESTful API toolkit |
| **PostgreSQL** | Production database |
| **Simple JWT** | JSON Web Token authentication |
| **django-filter** | Advanced queryset filtering |
| **django-cors-headers** | Cross-Origin Resource Sharing |
| **Pillow** | Image upload handling |
| **python-decouple** | Environment variable management |
| **Gunicorn** | Production WSGI server |

---

## 📁 Project Structure

```
urbanfinder/backend/
│
├── config/                     # ⚙️  Project Configuration
│   ├── __init__.py
│   ├── settings.py             # Django settings (DB, JWT, DRF, CORS, etc.)
│   ├── urls.py                 # Root URL router — includes all app URLs
│   ├── wsgi.py                 # WSGI entry point (production)
│   └── asgi.py                 # ASGI entry point (async support)
│
├── common/                     # 🔧 Shared Utilities
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py               # BaseModel (UUID PK + timestamps)
│   ├── permissions.py          # Role-based permissions (IsOwnerRole, IsAdminRole, etc.)
│   ├── pagination.py           # StandardPagination (20/page, configurable)
│   └── responses.py            # success_response() / error_response() helpers
│
├── users/                      # 👤 Users & Authentication
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py               # Custom User model (email-based auth, roles)
│   ├── managers.py             # Custom user manager
│   ├── serializers.py          # Register, Login, Profile, ChangePassword
│   ├── views.py                # Auth views (register, JWT login, profile)
│   ├── urls.py                 # /api/v1/auth/...
│   └── admin.py                # User admin configuration
│
├── properties/                 # 🏠 Property Listings
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py               # Property, PropertyImage, PropertyAmenity
│   ├── serializers.py          # List, Detail, Create/Update serializers
│   ├── filters.py              # Advanced filter (price range, specs, location)
│   ├── views.py                # CRUD + image upload + public search
│   ├── urls.py                 # /api/v1/properties/...
│   └── admin.py                # Property admin with inline images/amenities
│
├── bookmarks/                  # 🔖 Wishlist / Bookmarks
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py               # Bookmark (unique per user-property pair)
│   ├── serializers.py          # Bookmark with nested property details
│   ├── views.py                # List, toggle, check
│   ├── urls.py                 # /api/v1/bookmarks/...
│   └── admin.py
│
├── reviews/                    # ⭐ Reviews & Ratings
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py               # Review (1-5 rating, unique per user-property)
│   ├── serializers.py          # Review + stats serializers
│   ├── views.py                # CRUD + aggregate stats endpoint
│   ├── urls.py                 # /api/v1/reviews/...
│   └── admin.py
│
├── notifications/              # 🔔 In-App Notifications
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py               # Notification (types, read/unread, action URL)
│   ├── serializers.py
│   ├── views.py                # List, mark read, mark all read, unread count
│   ├── urls.py                 # /api/v1/notifications/...
│   └── admin.py
│
├── verification/               # ✅ Property Document Verification
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py               # VerificationDocument (status workflow)
│   ├── serializers.py          # Upload + admin review serializers
│   ├── views.py                # Upload, my docs, pending queue, admin review
│   ├── urls.py                 # /api/v1/verification/...
│   └── admin.py
│
├── chat/                       # 💬 Messaging System
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py               # Conversation + Message
│   ├── serializers.py          # Conversation list, message CRUD
│   ├── views.py                # Conversations, send/receive, auto-read
│   ├── urls.py                 # /api/v1/chat/...
│   └── admin.py
│
├── manage.py                   # Django management script
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variable template
├── .gitignore                  # Git ignore rules
└── README.md                   # ← You are here
```

---

## 📦 App Modules

### 1. `users` — Authentication & User Management
- Custom user model with **email-based login** (no username)
- Three roles: `USER`, `OWNER`, `ADMIN`
- JWT authentication with custom claims (role, email, full name embedded in token)
- Profile management and password change

### 2. `properties` — Rental Listings
- Full property details: type, furnishing, pricing, bedrooms, bathrooms, area, floor
- Location fields with latitude/longitude support
- Status lifecycle: `DRAFT` → `ACTIVE` → `RENTED` / `INACTIVE`
- Multi-image upload with cover image support
- Amenity tagging system
- Advanced search and filtering (price range, specs, location, type)
- Atomic view-count tracking

### 3. `bookmarks` — Wishlist
- Users can save/unsave properties with a single toggle endpoint
- Quick check endpoint to see if a property is bookmarked
- Returns full property details in list view

### 4. `reviews` — Ratings & Reviews
- 1–5 star rating system
- One review per user per property (enforced at DB and API level)
- Prevents owners from reviewing their own properties
- Aggregate stats endpoint with rating distribution `{1: 3, 2: 0, 3: 5, 4: 12, 5: 8}`

### 5. `notifications` — In-App Notifications
- Notification types: `REVIEW`, `BOOKMARK`, `VERIFICATION`, `PROPERTY`, `SYSTEM`, `MESSAGE`
- Read/unread state management
- Bulk mark-all-read action
- Unread count endpoint (for badge counters)

### 6. `verification` — Document Verification
- Owners upload documents (ownership proof, utility bills, identity, tax receipts)
- Documents enter a `PENDING` → `APPROVED` / `REJECTED` workflow
- Admin review queue with notes
- **Auto-verification**: When all documents for a property are approved, the property is automatically marked as verified

### 7. `chat` — Messaging
- Direct messaging between users (typically tenants ↔ owners)
- Conversations optionally linked to specific properties
- Auto-marks messages as read when the recipient views them
- Participant validation (only conversation members can read/send)

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.12+**
- **PostgreSQL 14+**
- **pip** (Python package manager)

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/urbanfinder.git
cd urbanfinder/backend
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate        # macOS/Linux
# venv\Scripts\activate         # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

```bash
cp .env.example .env
```

Edit `.env` with your values (see [Environment Variables](#-environment-variables) below).

### 5. Create the PostgreSQL Database

```bash
createdb urbanfinder_db
```

Or via `psql`:

```sql
CREATE DATABASE urbanfinder_db;
```

### 6. Run Migrations

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

### 7. Create a Superuser (Admin)

```bash
python3 manage.py createsuperuser
```

### 8. Start the Development Server

```bash
python3 manage.py runserver
```

The API is now live at: **`http://localhost:8000`**

- Admin panel: `http://localhost:8000/admin/`
- API root: `http://localhost:8000/api/v1/`

---

## 🔐 Environment Variables

Create a `.env` file in the project root (copy from `.env.example`):

```env
# Django
SECRET_KEY=your-super-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (PostgreSQL)
DB_NAME=urbanfinder_db
DB_USER=postgres
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432

# JWT Token Lifetimes
JWT_ACCESS_TOKEN_LIFETIME_MINUTES=60
JWT_REFRESH_TOKEN_LIFETIME_DAYS=7

# CORS — Add your frontend URL(s)
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:4200
```

---

## 📡 API Endpoints

All endpoints are prefixed with `/api/v1/`.

### Authentication (`/api/v1/auth/`)

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `/auth/register/` | ❌ | Register a new user |
| `POST` | `/auth/login/` | ❌ | Login → returns JWT tokens |
| `POST` | `/auth/token/refresh/` | ❌ | Refresh access token |
| `GET` | `/auth/profile/` | ✅ | Get current user's profile |
| `PATCH` | `/auth/profile/` | ✅ | Update profile |
| `POST` | `/auth/change-password/` | ✅ | Change password |

### Properties (`/api/v1/properties/`)

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `GET` | `/properties/` | ❌ | List all active properties (with filters) |
| `GET` | `/properties/<uuid>/` | ❌ | Get property details |
| `POST` | `/properties/create/` | 🏠 OWNER | Create new listing |
| `PATCH` | `/properties/<uuid>/update/` | 🏠 Owner of listing | Update listing |
| `DELETE` | `/properties/<uuid>/delete/` | 🏠 Owner of listing | Delete listing |
| `GET` | `/properties/my/` | 🏠 OWNER | Get my listings |
| `POST` | `/properties/<uuid>/images/` | 🏠 OWNER | Upload images |
| `DELETE` | `/properties/images/<uuid>/` | 🏠 OWNER | Delete an image |

**Available Filters** (as query params on `GET /properties/`):

```
?min_price=5000&max_price=20000
?city=kathmandu
?property_type=APARTMENT
?furnishing=FURNISHED
?min_bedrooms=2&max_bedrooms=4
?is_verified=true
?negotiable=true
?search=modern+apartment
?ordering=-price
```

### Bookmarks (`/api/v1/bookmarks/`)

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `GET` | `/bookmarks/` | ✅ | List my bookmarked properties |
| `POST` | `/bookmarks/toggle/` | ✅ | Toggle bookmark (add/remove) |
| `GET` | `/bookmarks/check/<uuid>/` | ✅ | Check if property is bookmarked |

### Reviews (`/api/v1/reviews/`)

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `GET` | `/reviews/?property=<uuid>` | ❌ | List reviews for a property |
| `POST` | `/reviews/` | ✅ | Submit a review |
| `PATCH` | `/reviews/<uuid>/` | ✅ Author | Update your review |
| `DELETE` | `/reviews/<uuid>/delete/` | ✅ Author | Delete your review |
| `GET` | `/reviews/stats/<uuid>/` | ❌ | Rating stats & distribution |

### Notifications (`/api/v1/notifications/`)

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `GET` | `/notifications/` | ✅ | List notifications (`?is_read=false`) |
| `PATCH` | `/notifications/<uuid>/read/` | ✅ | Mark as read |
| `POST` | `/notifications/read-all/` | ✅ | Mark all as read |
| `GET` | `/notifications/unread-count/` | ✅ | Get unread count |

### Verification (`/api/v1/verification/`)

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `/verification/upload/` | 🏠 OWNER | Upload verification document |
| `GET` | `/verification/my/` | 🏠 OWNER | My uploaded documents |
| `GET` | `/verification/pending/` | 🛡️ ADMIN | Pending review queue |
| `POST` | `/verification/<uuid>/review/` | 🛡️ ADMIN | Approve/reject document |

### Chat (`/api/v1/chat/`)

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `GET` | `/chat/` | ✅ | List my conversations |
| `POST` | `/chat/start/` | ✅ | Start a new conversation |
| `GET` | `/chat/<uuid>/messages/` | ✅ | List messages in conversation |
| `POST` | `/chat/<uuid>/send/` | ✅ | Send a message |

> **Legend**: ❌ = Public, ✅ = Any authenticated user, 🏠 = OWNER role, 🛡️ = ADMIN role

---

## 🔑 Authentication

This project uses **JWT (JSON Web Tokens)** via `djangorestframework-simplejwt`.

### How It Works

1. **Register** → `POST /api/v1/auth/register/`
2. **Login** → `POST /api/v1/auth/login/` → returns `access` and `refresh` tokens
3. **Use the access token** in subsequent requests:
   ```
   Authorization: Bearer <access_token>
   ```
4. **Refresh** when the access token expires → `POST /api/v1/auth/token/refresh/`

### Token Payload (Custom Claims)

```json
{
  "user_id": "uuid-here",
  "email": "user@example.com",
  "role": "USER",
  "full_name": "John Doe",
  "exp": 1700000000
}
```

The role is embedded in the token — frontends can decode it (it's a standard JWT) to conditionally show/hide UI based on the user's role without making an extra API call.

---

## 🛡️ Role-Based Access Control

| Role | Capabilities |
|------|-------------|
| **USER** | Browse properties, bookmark, review, chat, manage own profile |
| **OWNER** | Everything USER can do + create/manage property listings, upload images, submit verification docs |
| **ADMIN** | Everything OWNER can do + approve/reject verification documents, access admin panel |

Roles are assigned at registration via the `role` field and enforced server-side through custom DRF permission classes.

---

## 🔗 Connecting a Frontend

This backend is designed to work with **any frontend** — React, Angular, Vue, Flutter, Android (Kotlin/Java), etc.

### Step 1: Configure CORS

In your `.env` file, add your frontend's URL:

```env
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

### Step 2: API Base URL

Point your frontend's HTTP client to:

```
http://localhost:8000/api/v1/
```

### Step 3: Authentication Flow

```
Frontend                          Backend
   │                                 │
   │  POST /auth/register/           │
   │  {email, password, ...}    ───► │  → Creates user
   │                            ◄─── │  → Returns user data
   │                                 │
   │  POST /auth/login/              │
   │  {email, password}         ───► │  → Validates credentials
   │                            ◄─── │  → Returns {access, refresh}
   │                                 │
   │  GET /properties/               │
   │  Header: Bearer <token>    ───► │  → Returns paginated listings
   │                            ◄─── │
```

### Step 4: Example Frontend Integration (JavaScript/Fetch)

```javascript
// Login
const response = await fetch('http://localhost:8000/api/v1/auth/login/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email: 'user@example.com', password: 'password123' }),
});
const { access, refresh } = await response.json();

// Store tokens
localStorage.setItem('access_token', access);
localStorage.setItem('refresh_token', refresh);

// Authenticated request
const properties = await fetch('http://localhost:8000/api/v1/properties/', {
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
  },
});
const data = await properties.json();
```

### Step 5: Example Frontend Integration (Android / Kotlin with Retrofit)

```kotlin
// ApiService.kt
interface ApiService {
    @POST("auth/login/")
    suspend fun login(@Body credentials: LoginRequest): Response<TokenResponse>

    @GET("properties/")
    suspend fun getProperties(
        @Header("Authorization") token: String,
        @Query("city") city: String? = null,
        @Query("min_price") minPrice: Int? = null,
    ): Response<PaginatedResponse<Property>>
}

// Usage
val token = "Bearer ${savedAccessToken}"
val response = apiService.getProperties(token, city = "Kathmandu")
```

### API Response Format

All endpoints return a consistent JSON envelope:

```json
// Success
{
  "status": "success",
  "message": "Description of what happened",
  "data": { ... }
}

// Error
{
  "status": "error",
  "message": "What went wrong",
  "errors": { "field": ["Error detail"] }
}

// Paginated list
{
  "count": 42,
  "next": "http://localhost:8000/api/v1/properties/?page=2",
  "previous": null,
  "results": [ ... ]
}
```

---

## 🗄️ Database Schema Overview

```
┌──────────────────┐       ┌──────────────────┐
│      User        │       │    Property       │
│──────────────────│       │──────────────────│
│ id (UUID PK)     │       │ id (UUID PK)     │
│ email (unique)   │◄──┐   │ owner (FK→User)  │──┐
│ full_name        │   │   │ title            │  │
│ role (enum)      │   │   │ description      │  │
│ phone_number     │   │   │ property_type    │  │
│ avatar           │   │   │ price            │  │
│ is_verified      │   │   │ city / address   │  │
│ created_at       │   │   │ lat / lng        │  │
└──────────────────┘   │   │ status           │  │
                       │   │ is_verified      │  │
                       │   └──────────────────┘  │
                       │            │             │
          ┌────────────┼────────────┼─────────────┤
          │            │            │             │
          ▼            ▼            ▼             ▼
  ┌──────────────┐ ┌─────────┐ ┌──────────┐ ┌──────────────────┐
  │  Bookmark    │ │ Review  │ │ Property │ │ Verification     │
  │──────────────│ │─────────│ │ Image    │ │ Document         │
  │ user (FK)    │ │ user    │ │──────────│ │──────────────────│
  │ property(FK) │ │ property│ │ image    │ │ property (FK)    │
  │              │ │ rating  │ │ caption  │ │ document (file)  │
  │ unique_pair  │ │ comment │ │ is_cover │ │ document_type    │
  └──────────────┘ └─────────┘ └──────────┘ │ status           │
                                             │ reviewed_by (FK) │
  ┌───────────────────┐                      └──────────────────┘
  │   Conversation    │
  │───────────────────│     ┌──────────────┐
  │ initiator (FK)    │     │   Message     │
  │ receiver (FK)     │◄────│──────────────│
  │ related_property  │     │ sender (FK)  │
  └───────────────────┘     │ content      │
                            │ is_read      │
  ┌───────────────────┐     └──────────────┘
  │  Notification     │
  │───────────────────│
  │ recipient (FK)    │
  │ notification_type │
  │ title / message   │
  │ is_read           │
  └───────────────────┘
```

All models inherit from `BaseModel` which provides:
- **UUID primary key** (no sequential IDs)
- **`created_at`** (auto-set on creation, indexed)
- **`updated_at`** (auto-set on every save)

---

## 🧑‍💻 Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m "Add my feature"`
4. Push to the branch: `git push origin feature/my-feature`
5. Open a Pull Request

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

---

<p align="center">
  Built with ❤️ using Django & Django REST Framework
</p>
