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

from boto3.dynamodb.conditions import Key, Attr
import time_util

_RESOURCE_DYNAMODB = 'dynamodb'
_TABLE_NAME = 'market_daily_stat'

_dynamodb = boto3.resource(_RESOURCE_DYNAMODB, config=my_config)
_table = _dynamodb.Table(_TABLE_NAME)

_DATABASE_KEY_SYMBOL = 'symbol'
_DATABASE_KEY_DATE_STR = 'date_str'
_DATABASE_KEY_MARKET = 'market'


def _get_daily_stat_from_db(symbol, market, epoch_seconds):
    date_str = time_util.epoch_seconds_to_et_datetime(epoch_seconds).strftime('%Y-%m-%d')

    response = _table.query(
        KeyConditionExpression=Key(_DATABASE_KEY_DATE_STR).eq(date_str) & Key(_DATABASE_KEY_SYMBOL).eq(symbol),
        FilterExpression=Attr(_DATABASE_KEY_MARKET).eq(market)
    )

    items = response['Items']
    items = [i for i in items if i[_DATABASE_KEY_MARKET] == market]
    return items[0] if items else None


def _get_prev_daily_stat_from_db(symbol, market, epoch_seconds):
    time_util.epoch_seconds_to_et_datetime(epoch_seconds).strftime('%Y-%m-%d')
    prev_epoch_seconds = epoch_seconds
    while True:
        prev_epoch_seconds -= 3600 * 24
        daily_stat = _get_daily_stat_from_db(symbol, market, prev_epoch_seconds)
        if daily_stat:
            print("{t}'s prev day: {pt}".format(t=time_util.epoch_seconds_to_et_datetime(epoch_seconds).strftime('%Y-%m-%d'), pt=time_util.epoch_seconds_to_et_datetime(prev_epoch_seconds).strftime('%Y-%m-%d')))
            break
    return daily_stat


class DailyStatParams:
    def __init__(self, min_sofar_today, max_sofar_today, avg_sofar_today,
                 prev_daily_min, prev_daily_max, prev_daily_avg, prev_day_close):
        self.min_sofar_today = min_sofar_today
        self.max_sofar_today = max_sofar_today
        self.avg_sofar_today = avg_sofar_today
        self.prev_daily_min = prev_daily_min
        self.prev_daily_max = prev_daily_max
        self.prev_daily_avg = prev_daily_avg
        self.prev_day_close = prev_day_close

    def __str__(self):
        return 'min_sofar_today: {min_sofar_today}, max_sofar_today: {max_sofar_today}, avg_sofar_today: {avg_sofar_today}, prev_daily_min: {prev_daily_min}, prev_daily_max: {prev_daily_max}, prev_daily_avg: {prev_daily_avg}, prev_day_close: {prev_day_close}'.format(
            min_sofar_today=self.min_sofar_today, max_sofar_today=self.max_sofar_today, avg_sofar_today=self.avg_sofar_today,
            prev_daily_min=self.prev_daily_min, prev_daily_max=self.prev_daily_max, prev_daily_avg=self.prev_daily_avg, prev_day_close=self.prev_day_close)


def get_stat_prameters(symbol, market, epoch_seconds, windowed_min, windowed_max, windowed_avg):
    '''
    return the daily stats of the given day and the prev day needed to make a prediction.

    :param symbol:
    :param market:
    :param epoch_seconds:
    :param windowed_max:
    :param windowed_min:
    :param windowed_avg:
    :return:
    '''
    today_daily_stat = _get_daily_stat_from_db(symbol, market, epoch_seconds)
    min_sofar_today = min(windowed_min, float(today_daily_stat['daily_min'])) if windowed_min else float(today_daily_stat['daily_min'])
    max_sofar_today = max(windowed_max, float(today_daily_stat['daily_max'])) if windowed_max else float(today_daily_stat['daily_max'])
    avg_sofar_today = (windowed_avg + float(today_daily_stat['daily_avg'])) / 2.0 if windowed_avg else float(today_daily_stat['daily_avg'])

    prev_daily_stat = _get_prev_daily_stat_from_db(symbol, market, epoch_seconds)

    print('today_daily_stat:', today_daily_stat)
    print('prev_daily_stat:', prev_daily_stat)
    return DailyStatParams(
        min_sofar_today, max_sofar_today, avg_sofar_today,
        float(prev_daily_stat['daily_min']), float(prev_daily_stat['daily_max']), float(prev_daily_stat['daily_avg']),
        float(prev_daily_stat['daily_close'])
    )
