from fastapi import APIRouter, Depends


router = APIRouter()

@router.post("/send-notification/email")
async def send_data_to_queue():
    pass