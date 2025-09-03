dev-backend:
	cd backend && docker compose up

dev-ios:
	cd ios && open smartnotes.xcodeproj

setup-ios:
	cd ios && pod install

setup-backend:
	cd backend && pip install -r requirements.txt