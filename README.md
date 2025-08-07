# assets-ngeea-ilamb3
ilamb3 assets for NGEE-A benchmarking work on CADES

To run a study:

```bash
uv run python run.py
```

## Running Notes

### 7 Aug 2025

- Cartopy assets are not automatically downloading because of a certificate error. I had to manually place them in the right location.
- The 4 sites being run are close together and so for this first proof of concept results do not make a ton of sense.
- This run requires the local ilamb3 that is in this directory (in the ngeea branch). As we play around I will eventually merge back in what we develop once we find tests.
