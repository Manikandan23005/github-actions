import app


def test_index():
    client = app.app.test_client()
    rv = client.get("/")
    assert rv.status_code == 200
    assert rv.get_data(as_text=True) == "Hello from Flask!"
