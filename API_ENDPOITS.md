# Educational Center API Endpoints

#шпаргалка або текстовий путівник по вашому API, швидка текстова копія Swaggera

## Authentication
- POST /api/auth/login/ — Login with phone & password
- POST /api/auth/refresh/ — Refresh access token
- POST /api/auth/logout/ — Logout

## Branches
- GET /api/branches/ — List branches (admin only)
- POST /api/branches/ — Create branch
- GET /api/branches/{id}/ — Branch detail
- PUT /api/branches/{id}/ — Update branch
- POST /api/branches/{id}/archive/ — Archive branch

## Subjects
- GET /api/branches/{branch_id}/subjects/ — List subjects
- POST /api/branches/{branch_id}/subjects/ — Create subject
- PUT /api/subjects/{id}/ — Update subject
- POST /api/subjects/{id}/archive/ — Archive subject

## Students
- GET /api/students/ — List students (filters: branch, status, group)
- POST /api/students/ — Register student
- GET /api/students/{id}/ — Student detail
- PUT /api/students/{id}/ — Update student
- POST /api/students/{id}/archive/ — Archive student

## Groups
- GET /api/groups/ — List groups
- POST /api/groups/ — Create group
- POST /api/groups/{id}/add-student/ — Add student
- POST /api/groups/{id}/remove-student/ — Remove student

## Subscription Plans
- GET /api/subscription-plans/ — List plans
- POST /api/subscription-plans/ — Create plan
- POST /api/students/{id}/subscriptions/ — Assign plan

## Lessons
- GET /api/lessons/ — List lessons (filters: teacher, date, status)
- POST /api/lessons/ — Create lesson
- PUT /api/lessons/{id}/ — Update lesson
- POST /api/lessons/{id}/cancel/ — Cancel lesson

## Lesson Templates
- GET /api/lesson-templates/ — List templates
- POST /api/lesson-templates/ — Create template

## Attendance
- GET /api/lessons/{id}/attendance/ — Get attendance
- POST /api/lessons/{id}/attendance/ — Mark attendance

## Reports
- GET /api/reports/teacher-schedule/ — Teacher schedule
- GET /api/reports/student-attendance/ — Student attendance history