from locust import HttpUser, task, between
from AsyncApp import delivery_generate


class QuickstartUser(HttpUser):
    """Locust class for user behaviour."""

    wait_time = between(5, 9)

    @task
    def get_list(self) -> None:
        """Getting main page scenario."""
        self.client.get("/")

    @task(1)
    def post_order(self) -> None:
        """Posting json  scenario."""
        data = delivery_generate()
        self.client.post("/", json=data)

    def on_start(self) -> None:
        """Simple start function."""
        pass
