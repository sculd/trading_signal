import daily_stat

stat_prameters = daily_stat.get_stat_prameters(
    'AAPL', 'stock', 1626458700,
    200, 149, 148.5)

print(stat_prameters)

import prediction_jump

p = prediction_jump.predict(
    -1.0, 10.1,
    0.44, 1.07, 0.71,
    0.89, 0.83, 0.84,
    0.85
)

print(p)

import record

record.record_prediction('DUMMY', 'stock', 1626458700, 'drop', 'jump', p)
