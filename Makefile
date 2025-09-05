dev-backend:
	cd backend && docker compose up

build-backend:
	cd backend && docker compose up --build

dev-ios:
	cd ios && open smartnotes.xcodeproj

setup-ios:
	cd ios && pod install

setup-backend:
	cd backend && uv sync
