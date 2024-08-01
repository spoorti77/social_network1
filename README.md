# Social Networking API

## Description

A Django REST Framework application for a social networking platform with features including user authentication, friend requests, and user search.

## Features

- User signup and login
- Search users by email or name
- Send, accept, and reject friend requests
- List pending and accepted friend requests

## Installation

### Prerequisites

- Python 3.8 or higher
- pip
- Docker (optional, for containerization)

### Setting Up the Project

1. **Clone the Repository**

   ```bash
   git clone https://github.com/spoorti77/social_network1.git
   cd social_network1
   ```

2. **Create a Virtual Environment**

   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment**

   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

5. **Apply Migrations**

   ```bash
   python manage.py migrate
   ```

6. **Create a Superuser (Optional, for admin access)**

   ```bash
   python manage.py createsuperuser
   ```

7. **Run the Development Server**

   ```bash
   python manage.py runserver
   ```

   The server will be accessible at `http://127.0.0.1:8000/`.

### Docker Setup (Optional)

1. **Build the Docker Image**

   ```bash
   docker-compose build
   ```

2. **Run the Docker Container**

   ```bash
   docker-compose up
   ```

   The application will be accessible at `http://localhost:8000/`.

## Usage

- **Signup**: POST to `/api/signup/` with `email` and `password`.
- **Login**: POST to `/api/login/` with `email` and `password` to get a JWT token.
- **Search Users**: GET `/api/search/` with query parameters `email` or `name`.
- **Send Friend Request**: POST to `/api/friend-request/send/` with `email`.
- **Respond to Friend Request**: POST to `/api/friend-request/respond/{request_id}/` with `action` (`accept` or `reject`).
- **List Friends**: GET `/api/friends/`.
- **List Pending Friend Requests**: GET `/api/friend-request/pending/`.

## Postman Collection

You can import the Postman collection to easily test the API endpoints. Download the collection from [Postman Collection](URL_TO_YOUR_POSTMAN_COLLECTION) and import it into Postman.

## Contributing

Feel free to submit issues or pull requests to improve the project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```

### Instructions for Postman

1. **Export Postman Collection:**
   - Open Postman.
   - Go to the "Collections" tab.
   - Click on the collection you want to export.
   - Click on the three dots (more options) next to the collection name.
   - Choose "Export" and select the format (e.g., JSON).

2. **Upload to GitHub or Share:**
   - If you want to share the collection link, upload the exported JSON file to your repository or any file-sharing service and update the `URL_TO_YOUR_POSTMAN_COLLECTION` in the README.

3. **Update README:**
   - Replace `URL_TO_YOUR_POSTMAN_COLLECTION` with the actual URL or path where the Postman collection file is located.

By following these steps, you can ensure that your README file is comprehensive and useful for others who want to use or contribute to your project.
