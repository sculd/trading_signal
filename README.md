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
