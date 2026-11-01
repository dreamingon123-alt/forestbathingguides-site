# Operating manual: forestbathingguides.ch

Everything a future session needs to run this site. Replaces the Mac folder "Forest Bathing Switzerland website" (START-HERE, project docs, deploy state). Last updated 31 Oct 2026.

## 1. Locked rules (do not reopen)

1. One page per language: English at `/`, German at `/waldbaden/`. No new pages, ever. Anything new goes onto these pages or not on the site.
2. No pricing on this domain. Public pricing lives on catherinepeloquin.com/nature-reset-club/.
3. No dates on this domain. Every "join" link goes to the Nature Reset Club page, never an on-page anchor.
4. Corporate language is "outdoor team events". Never pair "forest bathing" or "Waldbaden" with the corporate offer in headings, metas or alt text. Method words stay in the brand, title and individual sections.
5. Forest bathing is never called a walk.
6. Boundary wording, two places only (method section bullet and FAQ): "The experience is for personal use, not professional use. We do not train trainers."
7. Three equal guides (Catherine, Daniela, Lucia). The site is not built around Cat or the Club.
8. For all of Switzerland. No French-language delivery.
9. Every factual claim cites last name and year. Stats as whole numbers. Never use Antonelli 2019 for a cortisol percentage. Qin et al., 2026 (not Pan). Shang et al., 2025 (not Fei).
10. Copy is short and factual. No invented scenes. No em dashes. No "not X, but Y" constructions.
11. English and German kept in step.
12. Nature quotes: one list (`src/quotes.json`), verbatim, used on both pages here and on the Nature Reset Club page. A new quote goes onto all three or none. Towns are real.
13. The email address never appears in the page source (the build enforces this).
14. Coach, not therapist: no treatment, cure or health-promise language.
15. Visible place wording is only "Zug", "Zurich" and "across Switzerland" (Cat, 1 Nov 2026). No lists of town names on the page; the canton of Zug towns live in the schema only.
16. Cat declared the site finished on 1 Nov 2026. Between quarterly reviews, change nothing unless she asks. The quarterly review limits itself to titles, metas, FAQ wording and schema.
17. Testimonial towns are the person's real town.

## 2. How the site works

- Source: this repository, branch `main`. Edit `src/` (text, quotes, CSS, redirects) and `static/` (images).
- `python3 build.py` builds `site/` and refuses to finish on: a second H1, an em dash, a missing image, an absolute upload URL, Antonelli, or a visible email address.
- Push to `main`: GitHub Actions builds into branch `live` (about 1 minute).
- Hostpoint cron job (Control Panel, Advanced, Cronjob Manager, every 10 minutes) downloads `live` into `~/www/fbs-static`. The domain's folder in Hostpoint Websites points to `fbs-static`.
- Live within about 10 minutes of a push. Verify with `curl -s https://forestbathingguides.ch/` and look for the change.

**Rollback:** in Hostpoint, Websites, forestbathingguides.ch, set the folder back to the WordPress folder (`forestbathingguides.ch` under `www`). WordPress was left untouched there on 31 Oct 2026. Planned retirement of that fallback: after 30 Nov 2026.

**Redirects** (in `src/htaccess.txt`): all 14 legacy WordPress pages and archives 301 to `/`; old sitemaps 301 to `/sitemap.xml`; WordPress system paths return 410; unknown URLs return a real 404; `.git` is blocked.

## 3. Measurement

| Source | Where | What |
|---|---|---|
| Google Analytics 4 | property 552925343, `G-YPDB066MPB` (Chrome authuser=1) | Users, channels. Key events to mark: `join_event_click`, `email_click`, `call_booking_click` (fired by the site since 31 Oct 2026). |
| Search Console | `https://forestbathingguides.ch/` (Chrome authuser=2) | Queries, CTR, position, indexing, Generative AI features. Sitemap `/sitemap.xml` submitted 31 Oct 2026. |
| Bing Webmaster | forestbathingguides.ch (authuser=2) | Impressions, AI Performance citations (feeds ChatGPT search). |
| Microsoft Clarity | project `yktsoicgjc` | Scroll depth, dead and rage clicks. |
| GEO log | Google Sheet "Forest Bathing GEO log", id `1iBAnsAoTU9RCmxuHmlKGSiLlS9TMYko24Akngog8pWc` | One row per month or quarter, column order: month, ga_users, ga_sessions, ga_top_channel, gsc_impressions, gsc_clicks, gsc_avg_position, gsc_top_query, bing_impressions, bing_clicks, bing_ai_impressions, changed_this_month, next_action. |

### Baselines

- 1 Oct 2026 (4 to 28 Sep): GSC 26 clicks, 488 impressions, position 8.3. "forest bathing" position 2.9 at 1.4% CTR. 90% scroll: 23% of desktop visitors.
- 30 Oct 2026 (28 days, WordPress, before the switch): GSC 12 clicks, 357 impressions, 3.4% CTR, position 7.0. "forest bathing" 5 clicks, 62 impressions (8% CTR). German team and Zurich queries ("waldbaden teamevent" 26, "waldbaden team" 23, "waldbaden zürich" 22) 71 impressions, 0 clicks. GA4 75 sessions, organic 32, 0 key events.
- 31 Oct 2026: static site live. New DE title "Waldbaden in Zürich & Zug | Outdoor-Teamevents Schweiz" targets the German zero-click queries. Judge it from the January review.

### Keyword strategy (Sept 2026)

Swiss demand: "teamevent" far above "teambuilding", "waldbaden" and "forest bathing" (near zero). Canton Zug is the top region for "teamevent". Head terms are owned by aggregators. Bridge terms, German first: outdoor teamevent zug; teamevent wald zug; firmenanlass wald schweiz; teamanlass natur zug; outdoor teambuilding zentralschweiz; waldbaden schweiz (individual sections only). The faster revenue lever is listings on Eventbutler.ch, Eventinc.ch, zuerich.com business programmes, Zug Tourismus and ausflugsziele.ch.

## 4. Quarterly review and optimisation (automated)

Runs on the 1st of February, May, August and November, 07:41 Zurich (moved from Jan/Apr/Jul/Oct by Cat, 1 Nov 2026; first run 1 Feb 2027). Steps:

1. Read this file and the last rows of the GEO log.
2. Pull the numbers (section 3) for the quarter and compare with the previous quarter and the baselines. If the browser cannot be reached, use public checks only and say so.
3. Technical check: both pages 200, redirects, sitemap, hreflang, tags, images, email hidden.
4. Decide up to three improvements with the highest click or discovery value, tied to the numbers (titles and metas for click-through, FAQ and schema for queries with impressions and no clicks, location wording). Each must follow section 1.
5. Make them in `src/`, run `build.py`, push, confirm live.
6. Append a row to the GEO log and a dated line to the log below.
7. Report to Cat: what moved, what was changed and why, one question. Changes are reversible with `git revert`.

Not automated (needs Cat): new testimonials, new photos, offer or positioning changes, listings that need an account, anything that changes the rules above.

## 5. Open items

- Nature Reset Club page (catherinepeloquin.com) still needs the 31 Oct quote set (see `src/quotes.json`).
- Mark the three GA4 click events as key events once they appear.
- `www.forestbathingguides.ch` does not resolve: add a `www` DNS entry in Hostpoint pointing to the same site.
- After 30 Nov 2026: retire the WordPress fallback; keep the 2 Oct 2026 full backup (Cat's Mac, `03_Live site backup/backups/2026-10-02-1324/`) in Drive Archive.
- Entity fixes queued from the 19 Sep sweep: ANFT bio, ICF Switzerland, Strozzi, Swiss Activities website link, MySwitzerland operator name, LinkedIn pages.

## 6. Log

- 2026-10-31: WordPress retired. Static site live from this repository. Changes: keyword H1 with statistic below, header Contact us and Join an upcoming event, hero Book an event (email), Cham quote first, four quotes removed (Teacher, Retiree love joy peace, Digital Publisher, VP Innovation), towns on all quotes, canton of Zug towns (Zug, Baar, Cham, Steinhausen, Hünenberg, Rotkreuz, Walchwil, Unterägeri, Oberägeri) in the Individuals card, plus Oberwil bei Zug, Menzingen, Zugerberg, Zurich and Lucerne in the schema, "Listed with" header, full footer with Impressum and privacy note, new DE title and meta, real 404, email hidden from source. Verified live; Search Console read `/sitemap.xml` (Success, 2 pages).
- 2026-11-01: Visible town list removed at Cat's request; Individuals card reads "Zug and Zurich". The canton of Zug towns stay in the schema only. Languages line added to the Teams card.
- 2026-11-01: Languages line removed from the Individuals card (kept on Teams). H1 now "Forest bathing in Zug, Zurich and across Switzerland" / "Waldbaden in Zug, Zürich und in der ganzen Schweiz". Nature Reset Club quote update dropped by Cat. Site declared finished by Cat; no further changes outside the quarterly review.
- 2026-11-01: Quarterly review moved to 1 Feb, May, Aug, Nov (first run 1 Feb 2027).
