# Library-Management-System
Build a library management system to manage libraries, books, authors, and categories. Implement user registration, login, and password recovery. Allow users to borrow and return multiple books in one transaction, with notifications and real-time updates for book availability.

## Endpoints

### Library
- List libraries
- Filter libraries by book categories, authors
- Calculate distances between users and nearby libraries

### Authors
- List authors with book counts
- Filter by library and book category

### Books
- List books
- Filter by category, library, and author
- Return author and category names

### Loaded Authors Endpoint
- List authors with all their books objects
- Each book should include its category object
- Filter by category and library


### Notifications

#### Email Notifications
- Send confirmation emails upon borrowing. Test locally with Mailhog, no actual email service required (AWS SES, Sendmail etc.)
- Send daily reminders in the last 3 days of the borrowing period

#### Borrowing Rules
- Allow up to 3 books; return one to borrow a 4th
- Users must specify a return date (max 1 month); late returns incur a daily penalty

#### Penalty Calculation
- Calculate penalties based on overdue days


## Development Setup

### Prerequisites
- Python 3.12+
- Postgresql 16+
- Docker and Docker Compose (optional, but recommended)
- Git

### First Time Setup

1. **Create and activate virtual environment**
```bash
python -m venv env
source env/bin/activate  # On Windows: .\env\Scripts\activate
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
cp .docker.env.example .docker.env  # Copy example env file
cp .env.example .env  # Copy example env file
# Edit .docker.env with your settings
```

4. **Start Docker services**
```bash
make up  # or: docker compose -f local.yml up -d
```

5. **Run migrations and create superuser**
```bash
make migrations
make migrate
make superuser  # Creates superuser with admin@example.com/admin
```

### Development Commands

**Docker Commands:**
```bash
make up           # Start all services
make down         # Stop all services
make logs         # View logs
```

**Django Commands:**
```bash
make migrations   # Create new migrations
make migrate      # Apply migrations
make superuser    # Create superuser
make shell       # Django shell
make test        # Run tests
```

### Available Services

- Django web: http://localhost:8000
- Redis Commander: http://localhost:8081
- MailHog (email testing): http://localhost:8025
- PostgreSQL: localhost:5433
- Celery Worker: None
- Celery Beat: None


### Code Quality Tools
This project uses:
- Black for code formatting

### Contributing
1. Create a new branch
2. Make your changes
3. Run tests and linting
4. Submit a pull request

### Troubleshooting

1. **Database Issues**
   ```bash
   make docker-clean  # Reset all containers and volumes
   make up           # Start fresh
   ```

### Additional Documentation
- [Django Documentation](https://docs.djangoproject.com/)
- [DRF Documentation](https://www.django-rest-framework.org/)
- [Docker Documentation](https://docs.docker.com/)