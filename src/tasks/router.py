from fastapi import APIRouter, BackgroundTasks, Depends
from tasks.tasks import send_email_report_dashboard
from auth.base_config import current_user

router = APIRouter(prefix='/report', tags=['Celery'])

@router.get('/dashboard')
def get_dashboard_report(backgroud_tasks: BackgroundTasks, user=Depends(current_user)):
    backgroud_tasks.add_tasks(send_email_report_dashboard, user.username)
    return {
        'status': 200,
        'data': 'Письмо отправлено',
        'details': None
    }