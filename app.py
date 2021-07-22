import os, time, datetime, logging
logging.basicConfig(level=logging.DEBUG)
import daily_stat, prediction_jump, prediction_drop, record
from flask import Flask, request

# make sure these libraries don't log debug statement which can contain
# sensitive information
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

app = Flask(__name__)


@app.route('/record_prediction', methods=['GET'])
def handle_record_prediction():
    move_type = request.args.get('move_type')
    symbol = request.args.get('symbol')
    market = request.args.get('market')
    price = float(request.args.get('price'))
    epoch_seconds = int(request.args.get('epoch_seconds'))
    max_jump_backward_percent = float(request.args.get('max_jump_backward_percent'))
    min_drop_backward_percent = float(request.args.get('min_drop_backward_percent'))

    windowed_max = float(request.args.get('windowed_max'))
    windowed_min = float(request.args.get('windowed_min'))
    windowed_avg = float(request.args.get('windowed_avg'))

    daily_stat_parameters = daily_stat.get_stat_prameters(symbol, market, epoch_seconds, windowed_min, windowed_max, windowed_avg)
    p = prediction_jump.predict(
        min_drop_backward_percent, max_jump_backward_percent,
        daily_stat_parameters.min_sofar_today / price,
        daily_stat_parameters.max_sofar_today / price,
        daily_stat_parameters.avg_sofar_today / price,
        daily_stat_parameters.prev_daily_min / price,
        daily_stat_parameters.prev_daily_max / price,
        daily_stat_parameters.prev_daily_avg / price,
        daily_stat_parameters.prev_day_close / price
    )

    record.record_prediction(symbol, market, epoch_seconds, move_type, 'jump', p)

    return p

@app.route('/record_drop_prediction', methods=['GET'])
def handle_record_drop_prediction():
    move_type = request.args.get('move_type')
    symbol = request.args.get('symbol')
    market = request.args.get('market')
    price = float(request.args.get('price'))
    epoch_seconds = int(request.args.get('epoch_seconds'))
    max_jump_backward_percent = float(request.args.get('max_jump_backward_percent'))
    min_drop_backward_percent = float(request.args.get('min_drop_backward_percent'))

    windowed_max = float(request.args.get('windowed_max'))
    windowed_min = float(request.args.get('windowed_min'))
    windowed_avg = float(request.args.get('windowed_avg'))

    daily_stat_parameters = daily_stat.get_stat_prameters(symbol, market, epoch_seconds, windowed_min, windowed_max, windowed_avg)
    p = prediction_drop.predict(
        min_drop_backward_percent, max_jump_backward_percent,
        daily_stat_parameters.min_sofar_today / price,
        daily_stat_parameters.max_sofar_today / price,
        daily_stat_parameters.avg_sofar_today / price,
        daily_stat_parameters.prev_daily_min / price,
        daily_stat_parameters.prev_daily_max / price,
        daily_stat_parameters.prev_daily_avg / price,
        daily_stat_parameters.prev_day_close / price
    )

    record.record_prediction(symbol, market, epoch_seconds, move_type, 'drop', p)

    return p

@app.route('/hello', methods=['GET'])
def hello():
    return 'hello world'

if __name__ == '__main__':
    # Used when running locally only. When deploying to Cloud Run,
    # a webserver process such as Gunicorn will serve the app.
    app.run(host='localhost', port=8081, debug=True)
