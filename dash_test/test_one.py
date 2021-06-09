from dash.testing.application_runners import import_app



def test_one(dash_duo):
    app = import_app("dash_test.app")
    dash_duo.start_server(app)

    dash_duo.wait_for_text_to_equal("h1", "A interactive dashboard to gain an overview of geological features relevant to the carbon sequestration process.", timeout=20)



