# About
This projects returns the prediction, collecting features from database to make a request.

# Build & Deploy

### Build
```
python run build
```

### Deploy
```
python run deploy
```

### Test
```
http://localhost:8081/record_prediction?symbol=AAPL&market=stock&move_type=drop&epoch_seconds=1626458700&max_jump_backward_percent=5.0&min_drop_backward_percent=-1.0&windowed_max=147&windowed_min=140&windowed_avg=144
```

## Architecture

```
stream aggregation
    |
    |
    \/
cloud run
    |
    | <--(read daily stats)--> dynamoDB (daily stat)
    |
    ^ --(record prediction)--> dynamoDB (prediction)
    |
    \/
vertex ai endpoint
```
