"""
Django management command to test TaskIQ tasks.
Usage: python manage.py test_tasks
"""
import asyncio
from django.core.management.base import BaseCommand
from taskiq_config import broker
from tasks import send_email_task, process_data_task, generate_report_task, cleanup_old_files_task


class Command(BaseCommand):
    help = 'Test TaskIQ tasks'

    def add_arguments(self, parser):
        parser.add_argument(
            '--task',
            type=str,
            help='Specific task to test (email, data, report, cleanup)',
        )

    def handle(self, *args, **options):
        """Handle the management command."""
        asyncio.run(self.run_tests(options.get('task')))

    async def run_tests(self, specific_task=None):
        """Run the task tests."""
        await broker.startup()
        
        try:
            if specific_task == 'email' or specific_task is None:
                await self.test_email_task()
            
            if specific_task == 'data' or specific_task is None:
                await self.test_data_task()
                
            if specific_task == 'report' or specific_task is None:
                await self.test_report_task()
                
            if specific_task == 'cleanup' or specific_task is None:
                await self.test_cleanup_task()
                
        finally:
            await broker.shutdown()

    async def test_email_task(self):
        """Test the email task."""
        self.stdout.write("Testing email task...")
        task = await send_email_task.kiq(
            "test@example.com",
            "Test Subject",
            "This is a test message"
        )
        result = await task.wait_result()
        self.stdout.write(self.style.SUCCESS(f"Email task result: {result}"))

    async def test_data_task(self):
        """Test the data processing task."""
        self.stdout.write("Testing data processing task...")
        test_data = {"name": "test", "value": 123}
        task = await process_data_task.kiq(test_data)
        result = await task.wait_result()
        self.stdout.write(self.style.SUCCESS(f"Data task result: {result}"))

    async def test_report_task(self):
        """Test the report generation task."""
        self.stdout.write("Testing report generation task...")
        task = await generate_report_task.kiq("monthly", 1)
        result = await task.wait_result()
        self.stdout.write(self.style.SUCCESS(f"Report task result: {result}"))

    async def test_cleanup_task(self):
        """Test the cleanup task."""
        self.stdout.write("Testing cleanup task...")
        task = await cleanup_old_files_task.kiq(30)
        result = await task.wait_result()
        self.stdout.write(self.style.SUCCESS(f"Cleanup task result: {result}")) 