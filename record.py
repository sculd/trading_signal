import boto3
from botocore.config import Config

my_config = Config(
    region_name = 'us-east-2',
    signature_version = 'v4',
    retries = {
        'max_attempts': 1,
        'mode': 'standard'
    }
)

import time_util
import logging_util

_RESOURCE_DYNAMODB = 'dynamodb'
_TABLE_NAME = 'market_daily_stat'

_dynamodb = boto3.resource(_RESOURCE_DYNAMODB, config=my_config)
_table = _dynamodb.Table(_TABLE_NAME)

def record_prediction(symbol, market, epoch_seconds, input_move_type, prediction_move_type, prediction):
    item = {
        'date_et': time_util.epoch_seconds_to_et_str(epoch_seconds)
        'timestamp': epoch_seconds,
        'datetime_et': time_util.epoch_seconds_to_et_str(epoch_seconds),
        'symbol': symbol,
        'market': market,
        'move_type': input_move_type,
        'prediction_move_type': prediction_move_type,
        '0': prediction['0'],
        '1': prediction['1']
        }

    message_str = '[dynamodb.record] {t} {s}'.format(
        t=time_util.epoch_seconds_to_et_str(epoch_seconds), s=symbol)
    logging_util.info(item)
    logging_util.info(message_str)
    print(item)
    print(message_str)
    try:
        _table.put_item(
            Item=item
        )
    except Exception as ex:
        logging_util.warning('an exception occurred while writing to dynamodb: {e}'.format(e=str(ex)))
        print(ex)
