# Testing Guide - Todo Phase 2 Project

## Overview

This guide provides step-by-step instructions for testing the full-stack Todo application using both manual and automated testing approaches.

## Testing Checklist

### ✅ Pre-Test Setup

Before testing, ensure you have:

- [ ] Docker Desktop installed and running
- [ ] Neon database URL configured in `.env`
- [ ] BETTER_AUTH_SECRET generated and set in `.env`
- [ ] All environment files created (`.env`, `backend/.env`, `frontend/.env.local`)
- [ ] Docker images built successfully (`docker compose build`)

---

## 🧪 Test Suite 1: Backend API Tests

### Test 1.1: Backend Health Check
**Command**:
```bash
curl http://localhost:8000/health
```

**Expected Result**:
```json
{"status": "healthy"}
```

**Status**: ⏭️ Not Run

---

### Test 1.2: Create Task (Authenticated)

**Setup**: Get a JWT token from Better Auth after signing up

**Command**:
```bash
curl -X POST http://localhost:8000/api/test-user-123/tasks \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Task", "description": "Test description"}'
```

**Expected Result**:
- Status: 201 Created
- Response contains task with ID, UUID, title, description, completed=false, user_id

**Status**: ⏭️ Not Run

---

### Test 1.3: List Tasks (Authenticated)

**Command**:
```bash
curl -X GET http://localhost:8000/api/test-user-123/tasks \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Expected Result**:
- Status: 200 OK
- Response: `{"tasks": [...], "total": n}`

**Status**: ⏭️ Not Run

---

### Test 1.4: Get Single Task

**Command**:
```bash
curl -X GET http://localhost:8000/api/test-user-123/tasks/1 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Expected Result**:
- Status: 200 OK
- Response contains task details

**Status**: ⏭️ Not Run

---

### Test 1.5: Update Task

**Command**:
```bash
curl -X PUT http://localhost:8000/api/test-user-123/tasks/1 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Task", "completed": true}'
```

**Expected Result**:
- Status: 200 OK
- Response contains updated task

**Status**: ⏭️ Not Run

---

### Test 1.6: Toggle Task Completion

**Command**:
```bash
curl -X PATCH http://localhost:8000/api/test-user-123/tasks/1/complete \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Expected Result**:
- Status: 200 OK
- Response: `{"id": 1, "uuid": "...", "completed": true}`

**Status**: ⏭️ Not Run

---

### Test 1.7: Delete Task

**Command**:
```bash
curl -X DELETE http://localhost:8000/api/test-user-123/tasks/1 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Expected Result**:
- Status: 204 No Content

**Status**: ⏭️ Not Run

---

### Test 1.8: Authentication Required (No Token)

**Command**:
```bash
curl -X GET http://localhost:8000/api/test-user-123/tasks
```

**Expected Result**:
- Status: 403 Forbidden or 401 Unauthorized

**Status**: ⏭️ Not Run

---

### Test 1.9: User Isolation

**Steps**:
1. Create task as User A
2. Try to access User A's task with User B's JWT token
3. Try to modify User A's task with User B's JWT token

**Expected Results**:
- All attempts should return 403 or 404
- User B cannot access/modify User A's tasks

**Status**: ⏭️ Not Run

---

## 🧪 Test Suite 2: Frontend Tests

### Test 2.1: Frontend Loads

**URL**: http://localhost:3000

**Expected Results**:
- [ ] Page loads successfully
- [ ] Shows marketing/landing page
- [ ] "Get Started" and "Sign In" buttons visible

**Status**: ⏭️ Not Run

---

### Test 2.2: Sign Up Flow

**Steps**:
1. Navigate to http://localhost:3000/signup
2. Enter email: `test@example.com`
3. Enter password: `TestPass123!`
4. Confirm password
5. Click "Sign Up"

**Expected Results**:
- [ ] Form validation works
- [ ] Account created successfully
- [ ] Redirected to /dashboard
- [ ] JWT token stored (check Application > Cookies)

**Status**: ⏭️ Not Run

---

### Test 2.3: Sign In Flow

**Steps**:
1. Navigate to http://localhost:3000/signin
2. Enter credentials
3. Click "Sign In"

**Expected Results**:
- [ ] Authentication successful
- [ ] Redirected to /dashboard
- [ ] Session persisted on refresh

**Status**: ⏭️ Not Run

---

### Test 2.4: Dashboard Displays Tasks

**Prerequisites**: User signed in, at least one task exists

**URL**: http://localhost:3000/dashboard

**Expected Results**:
- [ ] Dashboard loads
- [ ] Task list displayed
- [ ] "Add New Task" form visible
- [ ] No errors in console

**Status**: ⏭️ Not Run

---

### Test 2.5: Create Task via Frontend

**Steps**:
1. On dashboard, enter title: "Frontend Test Task"
2. Enter description: "Created from frontend"
3. Click "Add Task"

**Expected Results**:
- [ ] Task appears in list immediately
- [ ] Task persisted in database (check Neon console)
- [ ] Success indicator shown

**Status**: ⏭️ Not Run

---

### Test 2.6: Edit Task

**Steps**:
1. Click edit icon (pencil) on existing task
2. Modify title and/or description
3. Click "Save"

**Expected Results**:
- [ ] Changes saved immediately
- [ ] Updates persist after refresh
- [ ] Edit mode closes

**Status**: ⏭️ Not Run

---

### Test 2.7: Toggle Completion

**Steps**:
1. Click checkbox next to task
2. Verify task is marked complete (strikethrough)
3. Click checkbox again

**Expected Results**:
- [ ] Visual state changes immediately
- [ ] Completion status toggles correctly
- [ ] Persistence verified on refresh

**Status**: ⏭️ Not Run

---

### Test 2.8: Delete Task

**Steps**:
1. Click trash icon on existing task
2. Confirm deletion in popup

**Expected Results**:
- [ ] Task removed from list immediately
- [ ] Confirmation dialog shown
- [ ] Task deleted from database

**Status**: ⏭️ Not Run

---

### Test 2.9: Sign Out

**Steps**:
1. Click "Sign Out" button on dashboard
2. Verify redirect to home page
3. Try accessing /dashboard directly

**Expected Results**:
- [ ] Session cleared
- [ ] Redirected to home page
- [ ] /dashboard inaccessible (redirects to signin)

**Status**: ⏭️ Not Run

---

### Test 2.10: Responsive Design

**Test on Multiple Viewports**:
- Desktop (1920x1080)
- Tablet (768x1024)
- Mobile (375x667)

**Expected Results**:
- [ ] Layout adapts correctly
- [ ] Text readable on all sizes
- [ ] Touch targets appropriate (mobile)
- [ ] No horizontal scrolling

**Status**: ⏭️ Not Run

---

## 🧪 Test Suite 3: End-to-End Integration Tests

### Test 3.1: Full CRUD Flow

**Steps**:
1. Sign up as new user
2. Create 3 tasks
3. Verify all 3 appear in list
4. Edit one task
5. Toggle completion on one task
6. Delete one task
7. Sign out
8. Sign back in
9. Verify remaining tasks persist

**Expected Results**:
- [ ] All operations successful
- [ ] Data persists across sessions
- [ ] No data loss

**Status**: ⏭️ Not Run

---

### Test 3.2: User Isolation

**Steps**:
1. Sign up as User A (user-a@example.com)
2. Create 2 tasks
3. Sign out
4. Sign up as User B (user-b@example.com)
5. Create 1 task
6. Verify User B can only see their own task
7. Try to guess User A's task ID and access via URL

**Expected Results**:
- [ ] User A sees 2 tasks
- [ ] User B sees 1 task
- [ ] User B cannot access User A's tasks
- [ ] Returns 403/404 for unauthorized access

**Status**: ⏭️ Not Run

---

### Test 3.3: Data Persistence

**Steps**:
1. Create multiple tasks
2. Restart docker containers: `docker compose restart`
3. Refresh dashboard
4. Verify all tasks still present

**Expected Results**:
- [ ] All tasks persist after restart
- [ ] No data loss

**Status**: ⏭️ Not Run

---

### Test 3.4: JWT Token Expiration

**Steps**:
1. Sign in and capture JWT token
2. Wait for token expiration (if testing short expiry)
3. Try to access protected resource

**Expected Results**:
- [ ] Expired token rejected (401)
- [ ] User redirected to signin

**Status**: ⏭️ Not Run

---

## 🧪 Test Suite 4: Performance Tests

### Test 4.1: API Response Times

**Expected Results**:
- GET /tasks: < 200ms
- POST /tasks: < 300ms
- PUT /tasks/{id}: < 300ms
- DELETE /tasks/{id}: < 200ms

**Status**: ⏭️ Not Run

---

### Test 4.2: Frontend Load Time

**Expected Results**:
- Initial page load: < 2s
- Dashboard load: < 1s
- Task operations: < 500ms feedback

**Status**: ⏭️ Not Run

---

## 🧪 Test Suite 5: Automated API Tests

### Running Automated Tests

**Backend Tests**:
```bash
cd backend
uv run pytest tests/ -v
```

**Expected Results**:
- [ ] All tests pass
- [ ] Coverage > 80%

**Status**: ⏭️ Not Run

---

## 📊 Test Results Summary

| Test Suite | Total Tests | Passed | Failed | Skipped | Pass Rate |
|------------|-------------|--------|--------|---------|-----------|
| Backend API | 9 | 0 | 0 | 9 | 0% |
| Frontend | 10 | 0 | 0 | 10 | 0% |
| E2E Integration | 4 | 0 | 0 | 4 | 0% |
| Performance | 2 | 0 | 0 | 2 | 0% |
| Automated | 1 | 0 | 0 | 1 | 0% |
| **TOTAL** | **26** | **0** | **0** | **26** | **0%** |

---

## 🔧 Running All Tests

### Full Test Script

**Using Docker**:
```bash
# Start services
docker compose up -d

# Wait for services to be ready
sleep 30

# Run tests
./run-tests.sh

# View results
cat test-results.txt
```

**Manual Testing**:
```bash
# Frontend
cd frontend && npm run dev
# Test at http://localhost:3000

# Backend
cd backend && uv run uvicorn src.main:app --reload
# Test at http://localhost:8000/docs
```

---

## 📋 Pre-Submission Checklist

Before submitting, ensure all tests pass:

- [ ] All 6 API endpoints functional
- [ ] JWT authentication working
- [ ] User isolation enforced
- [ ] Frontend loads and displays properly
- [ ] Sign up/sign in flows work
- [ ] All 5 Basic Level features functional:
  - [ ] Add Task
  - [ ] View Task List
  - [ ] Update Task
  - [ ] Delete Task
  - [ ] Mark as Complete
- [ ] Data persists in Neon database
- [ ] Responsive design works on mobile/tablet
- [ ] Demo video recorded (< 90 seconds)
- [ ] Application deployed (Vercel)
- [ ] GitHub repository is public

---

## 🚀 Deployment Testing

### Vercel Deployment

**Test Steps**:
1. Deploy frontend to Vercel
2. Configure environment variables:
   - `NEXT_PUBLIC_API_URL` = backend URL
   - `BETTER_AUTH_SECRET` = same secret
3. Update backend CORS to allow Vercel domain
4. Test live deployment

**Expected Results**:
- [ ] Frontend accessible via Vercel URL
- [ ] Connects to backend successfully
- [ ] All features functional

**Status**: ⏭️ Not Run

---

## 🎬 Demo Video Checklist

**Video Requirements** (< 90 seconds):

- [ ] Show landing page
- [ ] Demonstrate sign up
- [ ] Show dashboard with tasks
- [ ] Create new task
- [ ] Toggle completion
- [ ] Edit task
- [ ] Delete task
- [ ] Show data persistence (optional)

**Video Status**: ⏭️ Not Recorded

---

## 📤 Submission Checklist

**Google Form Submission**:
- [ ] GitHub repository URL (public)
- [ ] Vercel deployment URL
- [ ] Demo video URL (YouTube/Vimeo/Loom)
- [ ] WhatsApp contact number
- [ ] Brief project description
- [ ] Features implemented (Basic + any bonuses)

**GitHub Repository**:
- [ ] README.md with setup instructions
- [ ] All code committed
- [ ] CONSTITUTION.md present
- [ ] /specs directory with all specifications
- [ ] .gitignore configured (excluding .env)
- [ ] License file (MIT recommended)

**Status**: ⏭️ Not Submitted

---

## 🐛 Known Issues & Limitations

**Document any issues found during testing:**

| Issue ID | Description | Severity | Workaround | Status |
|----------|-------------|----------|------------|--------|
| N/A | No testing performed yet | N/A | N/A | OPEN |

---

## 📞 Support

If tests fail:
1. Check container logs: `docker compose logs`
2. Verify .env configuration
3. Check database connection
4. Review API responses in browser DevTools
5. Contact support with error messages

---

**Last Updated**: 2025-01-16
**Tested By**: Not Yet Tested
**Docker Version**: Not Available
**Status**: Ready for Testing
