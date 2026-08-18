from fastapi import FastAPI
from fastapi.responses import HTMLResponse



posts: list[dict] = [
        {
                "id": 1,
                "author": "Corey Schafer",
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

@app.get("/", response_class=HTMLResponse)
def home():
        return "<h1>heloooooo!</h1>"

@app.get("/api/posts", response_class=HTMLResponse)
def get_posts():
        return f"<h1>{posts[0]}</h1><br><h2>{posts[1]}</h2>"