# Task Management with JWT, RBAC and Google Auth

## API Documentation

### 1. User Registration
- **Endpoint**: `POST /api/register/`
- **Allowed Roles**: All Users (Public)
- **Request Payload for admin**:
```json
{
  "email": "admin@example.com",
  "password": "securepassword123",
  "role": "admin" // Optional, defaults to 'user'
}
```
- **Request Payload for User**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123",
}
```
- **Payload Validation**:
  - `email`: Must be unique, valid email format
  - `password`: Minimum 8 characters
  - `role`: Either 'user' or 'admin'
- **Responses**:
  - `201 Created`: User successfully registered
  - `400 Bad Request`: Email already exists or invalid payload

### 2. User Login
- **Endpoint**: `POST /api/login/`
- **Allowed Roles**: All Users (Public)
- **Request Payload**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```
- **Payload Validation**:
  - `email`: Registered email address
  - `password`: Matching password
- **Responses**:
  - `200 OK`: Login successful, returns JWT token
  - `401 Unauthorized`: Invalid credentials

### 3. Google OAuth Authentication
- **Endpoint**: `POST /api/google/`
- **Allowed Roles**: All Users (Public)
- **Request Payload**:
```json
{
  "id_token": "google_oauth_token_here"
}
```
- **Payload Validation**:
  - `id_token`: Valid Google OAuth token
- **Responses**:
  - `200 OK`: Authentication successful
  - `400 Bad Request`: Invalid token

### 4. Create Task
- **Endpoint**: `POST /api/tasks/`
- **Allowed Roles**: ADMIN ONLY
- **Authentication Required**: Yes (JWT Token)
- **Request Payload**:
```json
{
  "title": "Project Meeting",
  "description": "Discuss project progress and next steps",
  "assigned_to": 2 // User ID to assign the task
}
```
- **Payload Validation**:
  - `title`: Required, max 255 characters
  - `description`: Optional, text field
  - `assigned_to`: Must be a valid user ID
- **Responses**:
  - `201 Created`: Task created successfully
  - `403 Forbidden`: Non-admin attempting to create task

### 5. List Tasks
- **Endpoint**: `GET /api/tasks/`
- **Allowed Roles**: 
  - Admin: See all tasks
  - User: See only assigned tasks
- **Authentication Required**: Yes (JWT Token)
- **Query Parameters**:
  - `status`: Filter by task status (optional)
  - `assigned_to`: Filter by assigned user (admin only)
- **Responses**:
  - `200 OK`: List of tasks based on user role
  ```json
  [
    {
      "id": 1,
      "title": "Project Meeting",
      "description": "Discuss project progress",
      "status": "Pending",
      "assigned_to": 2,
      "assigned_to_email": "user@example.com",
      "timestamp": "2024-03-27T10:30:00Z"
    }
  ]
  ```

### 6. Update Task Status
- **Endpoint**: `PUT /api/tasks/<task_id>/`
- **Allowed Roles**: 
  - Admin: Update any task
  - User: Update only assigned tasks
- **Authentication Required**: Yes (JWT Token)
- **Request Payload**:
```json
{
  "status": "Completed" // Can only be 'Pending' or 'Completed'
}
```
- **Payload Validation**:
  - `status`: Must be one of predefined choices
- **Responses**:
  - `200 OK`: Task status updated
  - `403 Forbidden`: Unauthorized task modification
  - `404 Not Found`: Task doesn't exist

### 7. Delete Task
- **Endpoint**: `DELETE /api/tasks/<task_id>/`
- **Allowed Roles**: ADMIN ONLY
- **Authentication Required**: Yes (JWT Token)
- **Responses**:
  - `204 No Content`: Task successfully deleted
  - `403 Forbidden`: Non-admin attempting deletion
  - `404 Not Found`: Task doesn't exist

## Role-Based Access Control (RBAC) Matrix

| Endpoint           | Anonymous | User | Admin |
|--------------------|-----------|------|-------|
| User Registration  | ✓         | ✓    | ✓     |
| User Login         | ✓         | ✓    | ✓     |
| Google OAuth       | ✓         | ✓    | ✓     |
| Create Task        | ✗         | ✗    | ✓     |
| List Tasks         | ✗         | Limited | Full |
| Update Task Status | ✗         | Own Tasks | All Tasks |
| Delete Task        | ✗         | ✗    | ✓     |

## Authentication Headers
Include JWT token in all authenticated requests:
```
Authorization: Bearer <your_jwt_token>
```

## Error Handling
- `400 Bad Request`: Invalid input
- `401 Unauthorized`: Authentication failure
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found

## Security Notes
- Passwords are hashed before storage
- JWT tokens expire after a set duration
- Google OAuth token verification
- Role-based access controls implemented