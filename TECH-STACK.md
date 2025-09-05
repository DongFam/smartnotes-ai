# Tech Stack

Created by: Julian Hein
Created time: September 3, 2025 7:03 PM
Last edited by: Julian Hein
Last updated time: September 3, 2025 7:11 PM

# SmartNote AI - Complete Tech Stack Documentation

## Version 1.0 - Hybrid Architecture

---

## 📋 Executive Summary

### Architecture Type: **Hybrid (On-Device + Cloud)**

### Team Size: **2 Full-Stack Developers**

### Target Platform: **iPad (iOS) with Cloud Backend**

### Monthly Infrastructure Cost: **~$73/month**

### Time to MVP: **12 weeks**

---

## 🏗️ Architecture Overview

### Hybrid Processing Model

### On-Device (iOS) Processing

- **Response Time:** < 50ms
- **Features:** Stroke smoothing, jitter removal, basic line straightening, simple shape detection, pressure curves
- **Technology:** Core ML, Swift
- **Benefits:** Instant feedback, works offline, battery efficient

### Cloud Processing (Backend)

- **Response Time:** 200-500ms (async)
- **Features:** Advanced beautification, handwriting recognition, layout analysis, complex shape recognition, formula detection
- **Technology:** FastAPI, Python ML models
- **Benefits:** Powerful AI, easy updates, A/B testing capability

---

## 🔧 Backend Stack

### Core Framework

- **Framework:** FastAPI
- **Language:** Python 3.12.7
- **ASGI Server:** Uvicorn
- **Process Manager:** Gunicorn

### Why FastAPI?

- Automatic API documentation (OpenAPI/Swagger)
- Native async support for WebSockets
- Built-in data validation with Pydantic
- High performance (on par with Node.js/Go)
- Excellent ML library ecosystem

### Database

- **Primary Database:** PostgreSQL 17
- **Hosting:** DigitalOcean Managed Database
- **Cost:** $15/month
- **Configuration:** 1GB RAM, 10GB storage, 1 vCPU

### Why PostgreSQL 17?

- JSONB support for flexible stroke data
- ACID compliance for data integrity
- Excellent performance with proper indexing
- Native full-text search capabilities
- Robust backup and recovery options

### Caching Layer

- **Cache:** Redis 7
- **Provider:** RedisLabs Free Tier
- **Usage:** Session storage, API response caching, WebSocket presence, Celery broker
- **Cost:** $0 (free tier: 30MB storage)

### Task Queue

- **Queue System:** Celery 5.3
- **Broker:** Redis
- **Use Cases:** PDF generation, model inference, email sending, batch processing
- **Worker Configuration:** 2 workers, 4 threads each

### Real-time Communication

- **Protocol:** WebSockets
- **Implementation:** FastAPI native WebSocket support
- **Use Cases:** Real-time sync, collaborative editing, live notifications
- **Scaling:** Redis Pub/Sub for multi-instance

---

## 📱 iOS Frontend Stack

### Core Technologies

- **Language:** Swift 5.9
- **UI Framework:** SwiftUI
- **Minimum iOS Version:** iOS 17
- **Target Device:** iPad (iPad Pro, iPad Air, iPad mini)

### Key Frameworks

- **PencilKit:** Apple Pencil input and stroke handling
- **Core ML:** On-device machine learning
- **Combine:** Reactive programming for data flow
- **Core Data:** Local storage and offline support

### Networking

- **HTTP Client:** URLSession (native)
- **WebSocket Client:** URLSessionWebSocketTask
- **API Format:** REST + WebSocket
- **Authentication:** OAuth 2.0 / OIDC

---

## 🚀 Infrastructure & Deployment

### Hosting Platform

- **Provider:** DigitalOcean App Platform
- **Type:** Platform as a Service (PaaS)
- **Cost:** $24/month
- **Configuration:** 1 vCPU, 512MB RAM (auto-scales)

### Why DigitalOcean App Platform?

- Zero-config deployment from GitHub
- Automatic SSL certificates
- Built-in monitoring and logging
- Auto-scaling capabilities
- Predictable pricing

### Storage Solution

- **Provider:** Cloudflare R2
- **Type:** S3-compatible object storage
- **Cost:** $0.015/GB stored, $0 egress fees
- **Usage:** Note backups, exports, ML models, user uploads

### Why Cloudflare R2?

- Zero egress fees (huge cost savings)
- S3 API compatibility
- Global CDN included
- Excellent performance

### Content Delivery

- **CDN:** Cloudflare CDN
- **Usage:** ML model distribution, static assets
- **Cost:** Included with R2
- **Benefits:** Global edge locations, DDoS protection

---

## 🔐 Authentication & Security

### Identity Provider

- **Service:** Keycloak
- **Deployment:** Self-hosted on DigitalOcean Droplet
- **Cost:** $20/month (4GB RAM droplet)
- **Protocol:** OAuth 2.0 / OpenID Connect

### Why Keycloak?

- Open source (no vendor lock-in)
- Enterprise features (MFA, SSO, federation)
- Customizable login flows
- No user limits
- GDPR compliant

### Security Implementation

- **Token Type:** JWT (JSON Web Tokens)
- **Token Storage (iOS):** iOS Keychain Services
- **Token Refresh:** Automatic with refresh tokens
- **MFA:** Optional TOTP support
- **Session Management:** Redis-backed sessions

---

## 💳 Payment Processing

### Payment Provider

- **Service:** Stripe
- **SDK:** stripe-python (backend), StripePaymentSheet (iOS)
- **Cost:** 2.9% + $0.30 per successful transaction

### Subscription Tiers

- **Free Tier:** 50 notes, basic features
- **Pro Tier:** $9.99/month, unlimited notes, advanced AI
- **Team Tier:** $19.99/month per user (future)

### Implementation

- **Billing:** Subscription-based with Stripe Billing
- **Webhooks:** Payment events to FastAPI
- **Invoice:** Automatic via Stripe
- **Tax:** Stripe Tax (automatic calculation)

---

## 📧 Communication Services

### Email Service

- **Provider:** Resend
- **Cost:** Free tier (3,000 emails/month)
- **Upgrade:** $20/month for 50,000 emails

### Email Types

- **Transactional:** Welcome, password reset, payment receipts
- **Notifications:** Export ready, collaboration invites
- **Marketing:** Feature announcements (future)

### Implementation

- **Templates:** React Email components
- **Sending:** Async via Celery tasks
- **Tracking:** Open rates and clicks

---

## 🌐 Marketing Website

### Landing Page Stack

- **Framework:** Next.js 14 (App Router)
- **Styling:** Tailwind CSS
- **Animations:** Framer Motion
- **Hosting:** Vercel (free tier)
- **Domain:** Cloudflare DNS

### Features

- **Performance:** Server-side rendering, edge optimization
- **SEO:** Meta tags, OpenGraph, sitemap
- **Analytics:** Vercel Analytics + Google Analytics
- **Forms:** Waitlist capture to PostgreSQL
- **CMS:** MDX for blog/documentation (future)

---

## 🤖 Machine Learning Pipeline

### Training Stack

- **Frameworks:** TensorFlow 2.x / PyTorch 2.x
- **Experiment Tracking:** Weights & Biases (free tier)
- **Data Storage:** Cloudflare R2
- **Training Compute:** Local GPU or Colab Pro ($10/month)

### Model Deployment

- **On-Device Format:** Core ML (.mlmodel)
- **Cloud Format:** ONNX or native PyTorch
- **Conversion:** coremltools
- **Versioning:** Semantic versioning (1.0.0)

### Model Distribution

- **Storage:** Cloudflare R2
- **Delivery:** CDN with geographic distribution
- **Updates:** Delta updates when possible
- **Fallback:** Previous version kept on device

### Models in Production

### On-Device Models

- **Stroke Beautifier:** ~5MB, runs on every stroke
- **Shape Detector:** ~3MB, triggered by gestures
- **Line Straightener:** ~1MB, real-time processing

### Cloud Models

- **Handwriting Recognition:** ~100MB, GPU inference
- **Layout Analyzer:** ~50MB, async processing
- **Formula Detector:** ~75MB, on-demand
- **Advanced Beautifier:** ~200MB, quality mode

---

## 📊 Monitoring & Analytics

### Error Tracking

- **Service:** Sentry
- **Tier:** Free (5,000 errors/month)
- **Integration:** Both iOS and Backend
- **Features:** Crash reporting, performance monitoring, release tracking

### Custom Telemetry

- **Storage:** PostgreSQL time-series tables
- **Collection:** Async from iOS, direct from backend
- **Metrics:** User behavior, feature usage, performance data
- **Privacy:** Anonymized, GDPR compliant

### Infrastructure Monitoring

- **Logs:** DigitalOcean built-in logging
- **Metrics:** DigitalOcean monitoring
- **Alerts:** Email and Slack notifications
- **Uptime:** Better Stack (free tier)

---

## 🛠️ Development Tools

### Version Control

- **Platform:** GitHub
- **Structure:** Monorepo
- **Branching:** Git Flow (main/develop/feature)
- **Code Review:** Pull request required

### CI/CD Pipeline

- **CI Service:** GitHub Actions
- **Backend Tests:** pytest, coverage reporting
- **iOS Tests:** XCTest, UI testing
- **Deployment:** Automatic to staging, manual to production

### Local Development

- **Backend:** Docker Compose (PostgreSQL + Redis)
- **iOS:** Xcode 15+, Swift Playgrounds
- **API Testing:** Bruno (open-source)
- **Database GUI:** DBeaver

### Documentation

- **API Docs:** OpenAPI/Swagger (auto-generated)
- **Code Docs:** Docstrings + Sphinx
- **User Docs:** Notion or GitBook
- **Architecture:** Mermaid diagrams

---

## 💰 Cost Analysis

### Monthly Infrastructure Costs

### Fixed Costs

- DigitalOcean App Platform: **$24**
- PostgreSQL Database: **$15**
- Keycloak Droplet: **$20**
- Apple Developer Program: **$8** (yearly amortized)
- Domain Name: **$1** (yearly amortized)
- **Subtotal:** **$68/month**

### Variable Costs (scales with usage)

- Cloudflare R2: **~$5** (10GB storage)
- Redis: **$0** (free tier)
- Sentry: **$0** (free tier)
- Resend: **$0** (free tier)
- Vercel: **$0** (free tier)
- Stripe: **2.9% + $0.30** per transaction

### Total Estimated: **$73/month** (before Stripe fees)

### Cost Scaling Projections

### 100 Users

- Infrastructure: $73/month
- Per user: $0.73

### 1,000 Users

- Infrastructure: ~$150/month (scaled resources)
- Per user: $0.15

### 10,000 Users

- Infrastructure: ~$800/month (multiple instances, larger database)
- Per user: $0.08

---

## 🚀 Deployment Configuration

### Environment Variables

### Backend (.env)

```
# Database
DATABASE_URL=postgresql://user:pass@host:5432/smartnote
REDIS_URL=redis://default:pass@redis-host:6379

# Authentication
KEYCLOAK_URL=[https://auth.smartnote.ai](https://auth.smartnote.ai)
KEYCLOAK_REALM=smartnote
KEYCLOAK_CLIENT_ID=backend
KEYCLOAK_CLIENT_SECRET=xxx

# Storage
R2_ACCESS_KEY_ID=xxx
R2_SECRET_ACCESS_KEY=xxx
R2_ENDPOINT_URL=[https://xxx.r2.cloudflarestorage.com](https://xxx.r2.cloudflarestorage.com)
R2_BUCKET_NAME=smartnote-storage

# Services
STRIPE_SECRET_KEY=sk_live_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx
RESEND_API_KEY=re_xxx
SENTRY_DSN=[https://xxx@sentry.io/xxx](https://xxx@sentry.io/xxx)

# App
ENVIRONMENT=production
DEBUG=false
SECRET_KEY=xxx
ALLOWED_ORIGINS=[https://smartnote.ai,https://app.smartnote.ai](https://smartnote.ai,https://app.smartnote.ai)
```

### Docker Configuration

### Production Dockerfile

```docker
FROM python:3.12.7-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Run with gunicorn
CMD ["gunicorn", "app.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
```

### iOS Build Configuration

### Info.plist Requirements

```xml
<key>NSCameraUsageDescription</key>
<string>Used for document scanning</string>
<key>NSPhotoLibraryUsageDescription</key>
<string>Save and import notes</string>
<key>UISupportsDocumentBrowser</key>
<true/>
<key>UIRequiresPersistentWiFi</key>
<false/>
```

---

## 📈 Scaling Strategy

### Phase 1: MVP (0-100 users)

- Single backend instance
- Basic PostgreSQL
- Manual monitoring
- Focus on stability

### Phase 2: Growth (100-1,000 users)

- 2 backend instances with load balancer
- PostgreSQL read replica
- Redis Sentinel for HA
- Automated monitoring

### Phase 3: Scale (1,000-10,000 users)

- Kubernetes orchestration
- PostgreSQL cluster
- Multi-region deployment
- Dedicated ML inference servers
- 24/7 on-call support

### Phase 4: Enterprise (10,000+ users)

- Multi-cloud strategy
- Global edge deployment
- Custom ML hardware
- Dedicated infrastructure team
- SOC 2 compliance

---

## 🔄 Version Management

### Semantic Versioning

- **Format:** MAJOR.MINOR.PATCH (e.g., 1.2.3)
- **Major:** Breaking changes
- **Minor:** New features, backward compatible
- **Patch:** Bug fixes

### Release Cycle

- **Backend:** Continuous deployment to staging, weekly to production
- **iOS:** Bi-weekly TestFlight, monthly App Store
- **ML Models:** Monthly updates, quarterly major versions
- **Database:** Migrations tested in staging first

---

## 🎯 Technology Decisions Rationale

### Why Hybrid Architecture?

- **Best UX:** Instant feedback for writing, powerful AI when needed
- **Cost Effective:** ~$73/month vs $4,000/month for full cloud
- **Offline Support:** Works without internet for basic features
- **Privacy:** Sensitive processing stays on device
- **Scalable:** Can shift processing based on metrics

### Why Python/FastAPI Backend?

- **ML Ecosystem:** Best libraries for AI/ML
- **Fast Development:** High productivity framework
- **Team Expertise:** Both developers learn one backend language
- **Performance:** Async support for WebSockets
- **Documentation:** Auto-generated API docs

### Why Native iOS?

- **PencilKit:** Only available native
- **Performance:** <50ms latency requirement
- **Core ML:** Best on-device ML performance
- **User Experience:** Platform-specific optimizations
- **App Store:** Better featuring opportunities

### Why PostgreSQL?

- **ACID Compliance:** Data integrity critical
- **JSONB:** Flexible stroke data storage
- **Maturity:** Battle-tested, great tooling
- **Performance:** Excellent with proper indexing
- **Cost:** Predictable, reasonable pricing

### Why Keycloak?

- **No Vendor Lock-in:** Open source
- **No User Limits:** Unlimited users
- **Enterprise Features:** MFA, SSO included
- **Customizable:** Full control over auth flows
- **Cost Effective:** $20/month vs $100s for Auth0

---

## 🚧 Future Considerations

### Potential Additions (Phase 2)

- **GraphQL:** For complex queries
- **Redis Streams:** For event sourcing
- **Temporal:** For workflow orchestration
- **Elasticsearch:** For advanced search
- **Prometheus + Grafana:** For detailed metrics

### Potential Migrations

- **Kubernetes:** When exceeding 5,000 users
- **Multi-region:** When latency becomes issue
- **Dedicated ML servers:** When inference costs spike
- **Data warehouse:** When analytics needs grow

---

## 📚 Documentation Links

### Official Documentation

- FastAPI: [https://fastapi.tiangolo.com](https://fastapi.tiangolo.com)
- SwiftUI: [https://developer.apple.com/swiftui](https://developer.apple.com/swiftui)
- PostgreSQL: [https://www.postgresql.org/docs/17](https://www.postgresql.org/docs/17)
- Keycloak: [https://www.keycloak.org/documentation](https://www.keycloak.org/documentation)
- Stripe: [https://stripe.com/docs](https://stripe.com/docs)
- Resend: [https://resend.com/docs](https://resend.com/docs)
- Next.js: [https://nextjs.org/docs](https://nextjs.org/docs)

### Internal Documentation

- API Specification: `/shared/api-spec/openapi.yaml`
- Database Schema: `/docs/[database-schema.md](http://database-schema.md)`
- Deployment Guide: `/docs/[deployment.md](http://deployment.md)`
- Troubleshooting: `/docs/[troubleshooting.md](http://troubleshooting.md)`

---

## ✅ Stack Validation Checklist

### Production Readiness

- ✅ All components production-tested
- ✅ Scaling strategy defined
- ✅ Monitoring in place
- ✅ Backup strategy defined
- ✅ Security measures implemented

### Cost Effectiveness

- ✅ Under $100/month for MVP
- ✅ Linear scaling costs
- ✅ No vendor lock-in
- ✅ Free tiers utilized
- ✅ Egress fees minimized

### Developer Experience

- ✅ Fast local development
- ✅ Good documentation
- ✅ Active communities
- ✅ Easy debugging
- ✅ CI/CD automated

### User Experience

- ✅ <50ms on-device latency
- ✅ Offline support
- ✅ Real-time sync
- ✅ Professional UI
- ✅ Data privacy

---

*Last Updated: December 2024*

*Version: 1.0*

*Status: Approved for Development*