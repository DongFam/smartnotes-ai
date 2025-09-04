# SmartNote AI 📝✨

> Transform your handwritten notes into beautifully formatted digital documents with the power of AI

[![iOS](https://img.shields.io/badge/iOS-17.0%2B-blue)](https://developer.apple.com/ios/)
[![Python](https://img.shields.io/badge/Python-3.12%2B-green)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-teal)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

SmartNote AI is an intelligent iPad note-taking application that uses hybrid on-device and cloud processing to beautify handwriting in real-time. Experience the natural feel of writing with Apple Pencil while getting perfectly formatted, searchable digital notes.

## 🌟 Features

### Core Capabilities

- **Real-Time Beautification** - Transform messy handwriting into clean, consistent strokes as you write (<50ms latency)
- **Smart Document Structure** - Automatically organize notes with proper spacing, alignment, and hierarchy
- **Shape Recognition** - Convert rough sketches into perfect circles, rectangles, and diagrams
- **Hybrid Processing** - Instant on-device processing for immediate feedback, cloud AI for advanced features
- **Offline First** - Full functionality without internet, seamless sync when connected

### Coming Soon

- Handwriting to text conversion (OCR)
- Mathematical formula recognition
- Multi-device real-time collaboration
- Custom templates and themes

## 🏗️ Architecture

```mermaid
graph TB
    A[iPad App] -->|Real-time <50ms| B[On-Device ML]
    A -->|Async 200-500ms| C[Cloud Processing]
    B --> D[Core ML Models]
    C --> E[FastAPI Backend]
    E --> F[PostgreSQL]
    E --> G[Redis Cache]
    E --> H[ML Models]
    A --> I[Cloudflare CDN]
    I --> J[Model Distribution]
```

### Hybrid Processing Model

- **On-Device**: Stroke smoothing, jitter removal, basic shapes, pressure curves
- **Cloud**: Advanced beautification, layout analysis, OCR, formula detection

## 🚀 Quick Start

### Prerequisites

- **iOS Development**: Xcode 15+, iOS 17+, iPad with Apple Pencil support
- **Backend Development**: Python 3.12+, Docker, PostgreSQL, Redis

### Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/smartnote-ai.git
cd smartnote-ai
```

#### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment variables
cp .env.example .env
# Edit .env with your actual values

# Start Docker services (PostgreSQL + Redis)
docker-compose up -d

# Run database migrations
alembic upgrade head

# Start the backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 3. iOS Setup

```bash
# Navigate to iOS directory
cd ../ios

# Install CocoaPods dependencies (if using)
pod install

# Open in Xcode
open SmartNoteAI.xcodeproj

# Configure signing & capabilities
# Select your development team
# Run on iPad simulator or device
```

## 📁 Project Structure

```
smartnote-ai/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── core/           # Core functionality
│   │   ├── models/         # Database models
│   │   ├── services/       # Business logic
│   │   └── ml/             # ML inference
│   ├── tests/              # Backend tests
│   ├── alembic/            # Database migrations
│   └── requirements.txt    # Python dependencies
│
├── ios/                    # iOS app
│   ├── SmartNoteAI/
│   │   ├── App/           # App lifecycle
│   │   ├── Views/         # SwiftUI views
│   │   ├── Models/        # Data models
│   │   ├── Services/      # Networking, storage
│   │   └── ML/            # Core ML integration
│   └── SmartNoteAITests/  # iOS tests
│
├── ml-models/              # Machine learning
│   ├── training/          # Training scripts
│   ├── models/            # Saved models
│   └── coreml/            # Core ML conversions
│
├── shared/                 # Shared resources
│   ├── api-spec/          # OpenAPI specs
│   └── constants/         # Shared constants
│
└── docs/                   # Documentation
    ├── PLANNING.md        # Development plan
    ├── TASKS.md           # Task breakdown
    ├── PRD.md             # Product requirements
    └── TECH-STACK.md      # Technical decisions
```

## 💻 Development

### Tech Stack

#### Backend

- **Framework**: FastAPI (Python 3.12)
- **Database**: PostgreSQL 17
- **Cache**: Redis 7
- **Task Queue**: Celery
- **Real-time**: WebSockets

#### iOS

- **Language**: Swift 5.9
- **UI**: SwiftUI
- **Drawing**: PencilKit
- **ML**: Core ML
- **Storage**: Core Data

#### Infrastructure

- **Hosting**: DigitalOcean App Platform
- **Storage**: Cloudflare R2
- **CDN**: Cloudflare
- **Monitoring**: Sentry
- **Analytics**: Custom telemetry

### Running Tests

```bash
# Backend tests
cd backend
pytest tests/ -v --cov=app

# iOS tests
# Run from Xcode: Cmd+U
```

### API Documentation

Once the backend is running, visit:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🔧 Configuration

### Environment Variables

Key environment variables (see `.env.example` for full list):

```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/smartnote

# Redis
REDIS_URL=redis://localhost:6379/0

# Authentication
JWT_SECRET_KEY=your-secret-key

# Storage
R2_ACCESS_KEY_ID=your-access-key
R2_BUCKET_NAME=smartnote-storage

# Monitoring
SENTRY_DSN=your-sentry-dsn
```

## 📊 Monitoring & Analytics

The application includes comprehensive monitoring from day one:

- **Error Tracking**: Sentry integration for both iOS and backend
- **Performance Monitoring**: Custom telemetry tracking
- **Cost Monitoring**: Per-user resource usage tracking
- **Analytics**: User behavior and feature adoption metrics

Access metrics at: `http://localhost:8000/health/metrics`

## 🚢 Deployment

### Backend Deployment (DigitalOcean)

```bash
# Build Docker image
docker build -t smartnote-backend .

# Push to registry
docker push registry.digitalocean.com/smartnote/backend:latest

# Deploy via DigitalOcean App Platform
doctl apps create --spec .do/app.yaml
```

### iOS Deployment (App Store)

1. Archive in Xcode: Product → Archive
2. Upload to App Store Connect
3. Submit for TestFlight beta testing
4. Submit for App Store review

## 🗺️ Roadmap

### Phase 1: MVP (Current)

- [x] Basic note creation and storage
- [x] Real-time beautification
- [x] PencilKit integration
- [ ] Shape recognition

### Phase 2: Enhanced Features

- [ ] Handwriting OCR
- [ ] Cloud sync
- [ ] Export to PDF/Markdown
- [ ] Search functionality

### Phase 3: Collaboration

- [ ] Real-time collaboration
- [ ] Sharing and permissions
- [ ] Comments and annotations
- [ ] Version history

## 💰 Pricing

- **Free Tier**: 50 notes, basic features
- **Pro**: $9.99/month - Unlimited notes, advanced AI, cloud sync
- **Team**: $19.99/user/month - Everything in Pro + collaboration

## 🤝 Contributing

We're a small team of 2 developers learning as we build! Contributions are welcome:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please read our [Contributing Guidelines](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Apple for PencilKit and Core ML frameworks
- FastAPI community for the excellent framework
- Our beta testers for valuable feedback

## 📧 Contact

- **Email**: support@smartnoteai.com
- **Twitter**: [@SmartNoteAI](https://twitter.com/smartnoteai)
- **Discord**: [Join our community](https://discord.gg/smartnoteai)

## 🔒 Security

For security vulnerabilities, please email security@smartnoteai.com directly rather than opening an issue.

## 📈 Status

- **Backend API**: ![API Status](https://img.shields.io/endpoint?url=https://api.smartnoteai.com/health)
- **Current Version**: 1.0.0
- **iOS Minimum**: 17.0
- **Infrastructure Cost**: ~$73/month

---

Built with ❤️ by a team of 2 developers learning as we go!
