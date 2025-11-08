from digits_recognition.server.server import predict_digit
from digits_recognition.types.server_types import Item

def test_predict():
    img = [0,0] * 784
    item = Item(image_data=img)
    response = predict_digit(item)
    assert "predictions" in response
    assert isinstance(response['predictions'], int)