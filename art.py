#!/usr/bin/env python3
"""Draw intentional contribution art, with no third-party dependencies."""
import argparse
import datetime as dt
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent
START = dt.date(2024, 6, 2)  # Sunday: GitHub's first calendar row.
STROKES = 8
PATTERNS = {
    'heart': ['.##.##.', '#######', '#######', '.#####.', '..###..', '...#...', '.......'],
    'cat': ['#.....#', '##...##', '#.###.#', '#.#.#.#', '#..#..#', '.#...#.', '..###..'],
    'star': ['...#...', '..###..', '#######', '.#####.', '..###..', '.#...#.', '#.....#'],
    'bunny': ['.#...#.', '.#...#.', '.#####.', '#.....#', '#.#.#.#', '#..#..#', '.#####.'],
    'flower': ['..###..', '.#.#.#.', '###.###', '.#.#.#.', '..###..', '...#.#.', '...##..'],
    'mushroom': ['..###..', '.#####.', '##.#.##', '#######', '..###..', '..#.#..', '..###..'],
    'smiley': ['..###..', '.#...#.', '#.#.#.#', '#.....#', '#.#.#.#', '.#.#.#.', '..###..'],
}

def pixel(day):
    offset = (day - START).days
    if offset < 0:
        return None
    week, row = divmod(offset, 7)
    symbol, column = divmod(week, 9)  # Seven columns plus two blank weeks.
    name = list(PATTERNS)[symbol % len(PATTERNS)]
    return name if column < 7 and PATTERNS[name][row][column] == '#' else None

def git(*args, env=None):
    return subprocess.check_output(['git', *args], cwd=ROOT, env=env, text=True).strip()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--through', type=dt.date.fromisoformat,
                        default=dt.datetime.now(dt.timezone.utc).date())
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    if args.through > dt.datetime.now(dt.timezone.utc).date():
        parser.error('Future days are drawn by the daily workflow when they arrive.')
    if git('status', '--porcelain'):
        parser.error('Commit or stash working-tree changes first.')
    state_path = ROOT / 'art-state.json'
    state = json.loads(state_path.read_text()) if state_path.exists() else {}
    last = dt.date.fromisoformat(state['date']) if state else START
    count = 0
    day = last
    while day <= args.through:
        name = pixel(day)
        done = state.get('stroke', 0) if state.get('date') == str(day) else 0
        if name:
            for stroke in range(done + 1, STROKES + 1):
                count += 1
                if args.dry_run:
                    continue
                state = {'date': str(day), 'symbol': name, 'stroke': stroke,
                         'purpose': 'Intentional decorative contribution art'}
                state_path.write_text(json.dumps(state, indent=2) + '\n')
                git('add', '--', 'art-state.json')
                stamp = f'{day}T12:{stroke:02d}:00+00:00'
                env = dict(os.environ, GIT_AUTHOR_NAME='git-art', GIT_COMMITTER_NAME='git-art',
                           GIT_AUTHOR_EMAIL='carlos.roberto.gonzales@gmail.com',
                           GIT_COMMITTER_EMAIL='carlos.roberto.gonzales@gmail.com',
                           GIT_AUTHOR_DATE=stamp, GIT_COMMITTER_DATE=stamp)
                git('-c', 'commit.gpgsign=false', 'commit', '-m',
                    f'art: {name} {day} stroke {stroke}/{STROKES}', env=env)
        day += dt.timedelta(days=1)
    print(f'{"Would create" if args.dry_run else "Created"} {count} art commits through {args.through}.')

if __name__ == '__main__':
    main()
