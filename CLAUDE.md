# CLAUDE.md - AI Assistant Context for SmartNote AI

## Project Overview

SmartNote AI is an iPad note-taking app with real-time handwriting beautification using hybrid on-device/cloud ML processing. Built by a 2-developer team learning as they build.

## Tech Stack

- **Backend**: Python 3.12, FastAPI, PostgreSQL, Redis, Celery
- **iOS**: Swift 5.9, SwiftUI, PencilKit, Core ML
- **Infrastructure**: DigitalOcean ($73/month), Cloudflare R2, Sentry
- **Architecture**: Hybrid - On-device (<50ms) + Cloud (200-500ms async)

## Project Structure

```
backend/     - FastAPI backend
ios/         - SwiftUI iPad app
ml-models/   - Training & Core ML conversion
shared/      - API specs, constants
docs/        - Planning, tasks, PRD
```

## Coding Standards

### Python (Backend)

```python
# Use type hints always
async def create_note(title: str, user_id: int) -> Dict[str, Any]:

# Async/await for all I/O
async with db.session() as session:

# Structured logging
logger.info("Note created", extra={"user_id": user_id})

# Handle errors explicitly
try:
    result = await process()
except SpecificError as e:
    logger.error(f"Processing failed: {e}")
    raise HTTPException(status_code=400, detail=str(e))
```

### Swift (iOS)

```swift
// Use SwiftUI + Combine
@StateObject private var viewModel = NoteViewModel()

// Async/await for networking
func fetchNotes() async throws -> [Note]

// Error handling with Result type
func process() -> Result<Data, ProcessingError>

// PencilKit for drawing
PKCanvasView with PKToolPicker
```

## Key Constraints

1. **Performance**: On-device must be <50ms latency
2. **Cost**: Keep infrastructure under $100/month
3. **Offline-First**: Core features work without internet
4. **Learning Curve**: Team is learning FastAPI/SwiftUI - suggest simple solutions first
5. **Monitoring**: Telemetry and Sentry from day 1

## Current Phase

Week 1 of 12-week MVP. Focus on foundation with monitoring built-in.

## Database Schema (Simplified)

```sql
users (id, email, created_at)
notes (id, user_id, title, stroke_data, created_at, updated_at)
telemetry_events (request_id, timestamp, user_id, response_time_ms)
```

## API Patterns

```
POST   /auth/register
POST   /auth/login
GET    /api/notes
POST   /api/notes
PUT    /api/notes/{id}
DELETE /api/notes/{id}
WS     /ws/sync
```

## Common Issues & Solutions

### WebSocket Sync Conflicts

Use version vectors, not just timestamps. Both devs need to understand conflict resolution.

### Model Size

Core ML models must be <10MB. Use quantization and pruning.

### Storage Costs

Implement tiered storage: Redis (hot) → PostgreSQL (warm) → R2 (cold)

## Response Guidelines

1. **Be Direct**: Skip pleasantries, get to the solution
2. **Show Code**: Provide working examples, not just theory
3. **Consider Both Devs**: Both team members touch all code
4. **Acknowledge Learning**: Explain the "why" briefly
5. **Cost-Conscious**: Always consider the $73/month budget
6. **Error Handling**: Every example should include error handling
7. **Testing**: Include test examples when relevant

## Don't Suggest

- Complex microservices (team too small)
- Kubernetes (overkill for current scale)
- Additional paid services without discussing cost
- React Native (already committed to native iOS)
- NoSQL as primary DB (PostgreSQL chosen for good reasons)

## Files to Reference

- `TASKS.md` - Current sprint tasks
- `PLANNING.md` - Overall timeline and milestones
- `PRD.md` - Feature requirements
- `.env.example` - All configuration options

## Team Context

Two full-stack developers alternating between backend/iOS daily. Both learning the stack. Pair programming on complex features. No dedicated DevOps/designer/PM - wearing all hats.

---

_Last Updated: Week 1 of Development_
