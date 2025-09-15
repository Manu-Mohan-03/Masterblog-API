# Masterblog API

To create an API that can be used by  web applications for blog management(CRUD)
Also a sample front end is provided with CSR functionality

## Installation

To install this project, simply clone the repository and install the dependencies in requirements.txt using `pip`

## Usage

To use this project, run the following command - `backend/backend_app.py`. To start the
frontend run frontend/frontend_app.py

## Design

As of now program don't support persistent storage. API provides following methods
1. /api/posts - GET method for all posts
2. /api/posts - POST method for saving new post
3. /api/post/search/?title=test&content=test - to search for a blog title or content
4. /api/post/?sort=['title' or 'content']&direction=['asc' or 'desc'] for sorting
5. /api/posts/<int:id> - DELETE method for deleting post numbered id (id should be integer)
6. /api/posts/<int:id> - PUT method for updating the post numbered id (id should be integer)

## Contributing

We welcome contributions! If you'd like to contribute to this project, please follow these guidelines
1. Create a new git branch
2. Push the branch with changes to github, please donot merge locally
3. Create a pull request if you want to merge it to main branch
4. After a successful review only branches will be merged with main branch

## Future enhancements
1. implement persistent storage
2. Altering the frontend app for editing blog



