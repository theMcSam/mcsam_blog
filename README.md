# Mcsam's Blog
Blogging API written with the FastAPI framework in python3.

## Features of API
1. Registering an account.
2. Logging into the account.
3. Deleting an account.
4. Create blog posts.
5. Updating blog posts.
6. View one blog post.
7. Get all blog posts.
8. Deleting blog posts.
9. Commenting on blog posts.
10. Updating  comments.
11. Deleting comments.

## How to run the application
1. Clone the repository.<br>
```git clone https://github.com/theMcSam/mcsam_blog.git```

2. Change your current working directory.<br>
```cd mcsam_blog```

3. Install the necessary requirements.<br>
```pip install -r requirements.txt```

4. Run the application with uvicorn.<br>
```uvicorn app:app --reload```

## API documentation
Visit the url: https://blogging-api-qpax.onrender.com/docs/ or

End point: /api/auth/signup<br>
Request body: 
```json
{
  "username": "string",
  "password": "password",
  "email": "mail@mail.com"
}
```

End point: /api/auth/login<br>
Request body: 
```json
{
  "username": "string",
  "password": "password"
} 
```
NB: After logging in you will be given a jwt in which you can use to authorized other requests by including it in the request headers. <br>

End point: /api/blog/create-post<br>
Request headers: Authorization jwt_token<br>
Request body:
```json 
{
  "title": "string",
  "content": "string"
}
```

## Deployed application
Visit the url: https://blogging-api-qpax.onrender.com/