from fastapi import FastAPI, Request, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException



posts: list[dict] = [
        {
                "id": 1,
                "author": "Alex",
                "title": "FastAPI is Awesome",
                "content": "This framework is really easy to use and super fast.",
                "date_posted": "April 20, 2025",
        },

        {
                "id": 2,
                "author": "Jane Doe",
                "title": "Python is Great for Web Development",
                "content": "Python is a great language for web development, and FastAPI makes it even better",
                "date_posted": "April 21, 2025",
        }
]

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")




@app.get("/")
def home(request: Request):
        return templates.TemplateResponse(request, "home.html", {"posts": posts, "title": "Home"}, )

@app.get("/api/posts")
def get_posts():
        return f"<h1>{posts[0]}</h1><br><h2>{posts[1]}</h2>"

@app.get("/posts/{post_id}", include_in_schema=False)
def post_page(post_id: int, request: Request):
        for post in posts:
                if post.get("id") == post_id:
                        title = post["title"][:50]
                        return templates.TemplateResponse(request, "post.html", {"post":post, "title": title})
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")



@app.get("/api/posts/{post_id}")
def get_post(post_id: int):
        for post in posts:
                if post.get("id") == post_id:
                        return post
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


@app.exception_handler(StarletteHTTPException)
def general_http_exception_handler(request: Request, exception:StarletteHTTPException):
        message = (
                exception.detail
                if exception.detail
                else "An Error has occured. Please check your request and try again later"
        )

        if request.url.path.startswith("/api"):
                return JSONResponse(status_code=exception.status_code, content={"detail": message})
                        
                
        return templates.TemplateResponse(request, "error.html", {"status_code":exception.status_code, "title":exception.status_code, "message": message}, status_code=exception.status_code)


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exception: RequestValidationError):
        if request.url.path.startswith("/api"):
                return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, content={"detail":exception.errors()}, )
        return templates.TemplateResponse(request, "error.html", {"status_code": status.HTTP_422_UNPROCESSABLE_CONTENT, "title": status.HTTP_422_UNPROCESSABLE_CONTENT, "message": "Invalid request, please check your request and try again"}, status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, )
