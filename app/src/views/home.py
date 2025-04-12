from renders.home import HomeRender
from services.cookie import CookieService
from services.resource import ResourceService

# Load styles and templates
ResourceService.load_styles("home.css")
templates = {
    "subscription": ResourceService.load_template("home/subscription_required.html"),
    "header": ResourceService.load_template("home/generation_header.html"),
    "result": ResourceService.load_template("home/result_container.html"),
}

render = HomeRender(templates)
query_balance = CookieService.controller.get("query_balance")

# Check subscription
if query_balance is None or query_balance == 0:
    render.render_subscription_required()
else:
    render.render_generation_form()
    render.render_result()
