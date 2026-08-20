from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates



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