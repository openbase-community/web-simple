"""
Django views that demonstrate TaskIQ integration.
"""
import asyncio
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from taskiq_config import broker
from tasks import send_email_task, process_data_task, generate_report_task


@csrf_exempt
@require_http_methods(["POST"])
def send_email_async(request):
    """
    API endpoint to send email asynchronously using TaskIQ.
    
    POST /api/send-email/
    Body: {
        "to_email": "user@example.com",
        "subject": "Test Subject",
        "message": "Test message"
    }
    """
    try:
        data = json.loads(request.body)
        to_email = data.get('to_email')
        subject = data.get('subject')
        message = data.get('message')
        
        if not all([to_email, subject, message]):
            return JsonResponse({
                'error': 'Missing required fields: to_email, subject, message'
            }, status=400)
        
        # Queue the email task
        async def queue_task():
            await broker.startup()
            try:
                task = await send_email_task.kiq(to_email, subject, message)
                return task.task_id
            finally:
                await broker.shutdown()
        
        task_id = asyncio.run(queue_task())
        
        return JsonResponse({
            'status': 'queued',
            'task_id': task_id,
            'message': 'Email task has been queued for processing'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def process_data_async(request):
    """
    API endpoint to process data asynchronously using TaskIQ.
    
    POST /api/process-data/
    Body: {
        "data": {"key": "value", "number": 123}
    }
    """
    try:
        request_data = json.loads(request.body)
        data_to_process = request_data.get('data')
        
        if not data_to_process:
            return JsonResponse({
                'error': 'Missing required field: data'
            }, status=400)
        
        # Queue the data processing task
        async def queue_task():
            await broker.startup()
            try:
                task = await process_data_task.kiq(data_to_process)
                return task.task_id
            finally:
                await broker.shutdown()
        
        task_id = asyncio.run(queue_task())
        
        return JsonResponse({
            'status': 'queued',
            'task_id': task_id,
            'message': 'Data processing task has been queued'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def generate_report_async(request):
    """
    API endpoint to generate report asynchronously using TaskIQ.
    
    POST /api/generate-report/
    Body: {
        "report_type": "monthly",
        "user_id": 1
    }
    """
    try:
        data = json.loads(request.body)
        report_type = data.get('report_type')
        user_id = data.get('user_id')
        
        if not all([report_type, user_id]):
            return JsonResponse({
                'error': 'Missing required fields: report_type, user_id'
            }, status=400)
        
        # Queue the report generation task
        async def queue_task():
            await broker.startup()
            try:
                task = await generate_report_task.kiq(report_type, user_id)
                return task.task_id
            finally:
                await broker.shutdown()
        
        task_id = asyncio.run(queue_task())
        
        return JsonResponse({
            'status': 'queued',
            'task_id': task_id,
            'message': 'Report generation task has been queued'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def task_status(request, task_id):
    """
    API endpoint to check task status.
    
    GET /api/task-status/<task_id>/
    """
    # Note: In a real implementation, you would query the result backend
    # to get the actual task status. This is a simplified example.
    return JsonResponse({
        'task_id': task_id,
        'status': 'This endpoint would check task status in the result backend',
        'note': 'Implement actual status checking using the result backend'
    }) 