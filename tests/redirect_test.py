import responses
from resteasy import RESTEasy


@responses.activate
def test_redirect():
    responses.add(
        responses.POST,
        "http://foo.com/post",
        headers={"Location": "http://foo.com/get"},
    )
    responses.add(responses.GET, "http://foo.com/get", json={"foo": "bar"})

    api = RESTEasy("http://foo.com")

    res = api.route("post").post()

    assert res == {"foo": "bar"}
    assert len(responses.calls) == 2
    assert responses.calls[0].request.method == "POST"
    assert responses.calls[0].request.url == "http://foo.com/post"
    assert responses.calls[1].request.method == "GET"
    assert responses.calls[1].request.url == "http://foo.com/get"
