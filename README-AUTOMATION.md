# Legal Khata website source
- `src/build.py` (+ `src/content_india.py`, `src/content_world.py`) generates the whole static site into `./worker/public/`.
- To publish a change: edit the content in `src/content_india.py` / `src/content_world.py` (or add a new page in `build.py`), then run `./publish.sh "message"` from the repo root. It rebuilds, pushes the source to branch `source`, and pushes the built site to branch `main` (Cloudflare auto-deploys `main` to legalkhata.com).
- Images used on pages live in `assets/img/`.
- Country/service pages are data-driven from `content_india.py` and `content_world.py` — add a country or service there rather than hand-writing HTML.
