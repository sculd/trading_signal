import os
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(os.getcwd(), 'credential.json')

from google.cloud import aiplatform
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value

_PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT')
_ENDPOINT_ID = os.getenv('MODEL_ENDPOINT_ID')
_LOCATION = 'us-central1'
_API_ENDPOINT = "us-central1-aiplatform.googleapis.com"
_CLIENT_OPTIONS = {"api_endpoint": _API_ENDPOINT}
_client = aiplatform.gapic.PredictionServiceClient(client_options=_CLIENT_OPTIONS)


def predict(
        min_drop_backward_percent,
        max_jump_backward_percent,
        min_sofar_today,
        max_sofar_today,
        avg_sofar_today,
        prev_daily_min,
        prev_daily_max,
        prev_daily_avg,
        prev_day_close):
    instance_dict = {
        "min_drop_backward_percent": min_drop_backward_percent,
        "max_jump_backward_percent": max_jump_backward_percent,
        "min_sofar_today": min_sofar_today,
        "max_sofar_today": max_sofar_today,
        "avg_sofar_today": avg_sofar_today,
        "prev_daily_min": prev_daily_min,
        "prev_daily_max": prev_daily_max,
        "prev_daily_avg": prev_daily_avg,
        "prev_day_close": prev_day_close
        }
    instance = json_format.ParseDict(instance_dict, Value())
    instances = [instance]
    parameters_dict = {}
    parameters = json_format.ParseDict(parameters_dict, Value())
    endpoint = _client.endpoint_path(
        project=_PROJECT_ID, location=_LOCATION, endpoint=_ENDPOINT_ID
    )
    response = _client.predict(
        endpoint=endpoint, instances=instances, parameters=parameters
    )
    predictions = response.predictions
    for prediction in predictions:
        prediction = dict(prediction)
        ret = {}
        for i, c in enumerate(prediction['classes']):
            ret[c] = prediction['scores'][i]
        return ret
    return {}

