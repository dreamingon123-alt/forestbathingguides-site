# forestbathingguides.ch

The static website for Forest Bathing Switzerland. One page per language: English at `/`, German at `/waldbaden/`.

## Where things are

| Path | What |
|---|---|
| `src/en.html`, `src/de.html` | Page text and layout. Edit these. |
| `src/quotes.json` | The one list of nature quotes. Same list runs on the Nature Reset Club page. |
| `src/site.css` | Styles. |
| `src/htaccess.txt` | Redirects (every old WordPress URL goes to `/`), 404, caching. |
| `static/` | Images, kept at their old WordPress paths so image links keep working. |
| `build.py` | Builds `site/`: head tags, schema from the visible FAQ, analytics, sitemap, robots, 404. |

## How a change goes live

1. Edit `src/` or `static/`.
2. Push to `main`.
3. GitHub builds the site and copies it to Hostpoint (`.github/workflows/deploy.yml`).

The build stops on a second H1, an em dash, a missing image or an absolute upload URL.

## Rules (from the project folder, START-HERE)

One page per language. No prices, no dates. Every "join" link goes to the Nature Reset Club page. Corporate offer is "outdoor team events", never paired with forest bathing in a heading. Every factual claim cites last name and year. Nothing goes live without Cat's yes.
