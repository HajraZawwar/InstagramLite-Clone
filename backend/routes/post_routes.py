from fastapi import APIRouter
from controllers.post_controller import router as post_router

router = APIRouter()

router.include_router(post_router, prefix="/posts", tags=["Posts"])
