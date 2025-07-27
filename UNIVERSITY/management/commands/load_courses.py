from django.core.management.base import BaseCommand, CommandError
from UNIVERSITY.models import Course # Import your Course model

class Command(BaseCommand):
    help = 'Loads initial course data into the database.'

    def handle(self, *args, **options):
        courses_to_add = [
            # Undergraduate Programs - Social Management Sciences
            {'title': 'Economics', 'code': 'ECO', 'department': 'Social Management Sciences'},
            {'title': 'Accounting', 'code': 'ACC', 'department': 'Social Management Sciences'},
            {'title': 'Actuarial Science', 'code': 'ACTS', 'department': 'Social Management Sciences'},
            {'title': 'Business Administration', 'code': 'BAD', 'department': 'Social Management Sciences'},
            {'title': 'Marketing', 'code': 'MKT', 'department': 'Social Management Sciences'},
            {'title': 'Banking & Finance', 'code': 'B&F', 'department': 'Social Management Sciences'},

            # Undergraduate Programs - Pure and Applied Sciences
            {'title': 'Biochemistry', 'code': 'BCH', 'department': 'Pure and Applied Sciences'},
            {'title': 'Microbiology', 'code': 'MCB', 'department': 'Pure and Applied Sciences'},
            {'title': 'Computer Science', 'code': 'CSC', 'department': 'Pure and Applied Sciences'},
            {'title': 'Industrial Chemistry', 'code': 'ICH', 'department': 'Pure and Applied Sciences'},
            {'title': 'Industrial Mathematics', 'code': 'IMT', 'department': 'Pure and Applied Sciences'},
            {'title': 'Physics with Electronics', 'code': 'PWE', 'department': 'Pure and Applied Sciences'},

            # Other Undergraduate Programs
            {'title': 'Real Estate Management', 'code': 'REM', 'department': 'Other Undergraduate Programs'},
            {'title': 'Customs Administration', 'code': 'CUSAD', 'department': 'Other Undergraduate Programs'},
            {'title': 'International Relations', 'code': 'IRL', 'department': 'Other Undergraduate Programs'},
            {'title': 'Mass Communication', 'code': 'MCM', 'department': 'Other Undergraduate Programs'},

            # Postgraduate Programs
            {'title': 'Master of Business Administration', 'code': 'MBA', 'credits': 0, 'department': 'Postgraduate Programs'},
            {'title': 'Master of Arts in Theological Studies', 'code': 'MATS', 'credits': 0, 'department': 'Postgraduate Programs'},
            {'title': 'Master of Information Technology', 'code': 'MIT', 'credits': 0, 'department': 'Postgraduate Programs'},
            {'title': 'Master of Arts in Nursing', 'code': 'MAN', 'credits': 0, 'department': 'Postgraduate Programs'},
            {'title': 'Master of Science in Social Work', 'code': 'MSSW', 'credits': 0, 'department': 'Postgraduate Programs'},
        ]

        self.stdout.write("Loading courses...")
        for course_data in courses_to_add:
            # Use get_or_create to avoid creating duplicates if the script is run multiple times
            course, created = Course.objects.get_or_create(
                code=course_data['code'], # Use 'code' for unique identification
                defaults={
                    'title': course_data['title'],
                    'department': course_data['department'],
                    'credits': course_data.get('credits', 3), # Default to 3 credits if not specified
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Successfully added course: {course.title} ({course.code})"))
            else:
                self.stdout.write(self.style.WARNING(f"Course already exists: {course.title} ({course.code}) - Skipping."))

        self.stdout.write(self.style.SUCCESS('Finished loading courses.'))