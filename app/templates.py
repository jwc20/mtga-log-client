from fastapi.templating import Jinja2Templates

from app.config import template_path

templates = Jinja2Templates(directory=template_path)