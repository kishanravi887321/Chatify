import sys
import os
from pathlib import Path

# Add current directory and parent directory to Python path
current_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(current_dir))
if current_dir.name == 'src':
    # If we're in src directory, add parent to path
    sys.path.insert(0, str(current_dir.parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Try different import paths based on where we're running from
try:
    from src.api.chats import chat
except ImportError:
    try:
        from api.chats import chat
    except ImportError:
        # If we're in the src directory already
        sys.path.insert(0, str(current_dir))
        from api.chats import chat

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(chat.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
