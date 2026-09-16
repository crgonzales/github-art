# Cute contribution garden

Hearts, cats, stars, bunnies, flowers, mushrooms, and smiley faces drawn on the GitHub contribution calendar.

This is intentional decorative, backdated commit art, not a record of historical software work. Original commits are preserved; the old per-pixel files have been removed from the current tree.

## How it works

`art.py` uses only Python's standard library. Starting Sunday, June 2, 2024, each symbol occupies seven weeks and seven weekday rows, with two blank weeks between symbols. The seven-symbol collection repeats indefinitely. Each lit pixel gets eight commits; blank pixels get none. Only `art-state.json` changes, so there is no pile of generated files.

The daily GitHub Actions workflow runs at 20:43 UTC, draws pixels due through today, and pushes them to `master`. It catches up missed days and safely does nothing when rerun. It never creates future-dated commits. Automation continues while GitHub Actions and repository write access remain enabled. Existing contributions elsewhere and the original art can show through the design.

## Run manually

```sh
python3 art.py --through 2026-06-30 --dry-run
python3 art.py --through 2026-06-30
git push origin master
```

Without `--through`, the script catches up through the current UTC date. You can also run **Daily cute art** from the repository's Actions tab. To pause future art, disable that workflow. Edit `PATTERNS` in `art.py` to change future designs (`#` is lit; `.` is blank).
