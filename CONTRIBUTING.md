# Developing guide

# Run locally

Place `.env` with environment variables to project root, then run:

```
$ pip install -r requirements.txt
$ python run.py
```

# Environment Variables

- `HOLODULE_PAGE`: **Required.** Holodule page URL to get. Must be a `シンプル版`.
- `HOLODULE_YOUTUBE_KEY`: **Required.** API key of YouTube Data API.
- `HOLODULE_DIR`: Directory to place result `.ics` files. Default to `public`.
- `HOLODULE_LOGLEVEL`: Loglevel of `logging` module. Default to `INFO`.
