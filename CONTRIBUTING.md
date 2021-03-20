# Developing guide

# Clone repository

To avoid cloning numerous deploy histories in `public` and `gh-pages` branch,
make sure to clone with `--single-branch` option:

```
$ git clone -b master --single-branch https://github.com/sarisia/holodule-ics.git
```

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
