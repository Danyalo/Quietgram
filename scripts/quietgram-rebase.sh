#!/usr/bin/env bash
# Replay the personal patch stack on a new pinned upstream commit.
set -euo pipefail

if [[ $# -ne 3 ]]; then
    echo "Usage: bash scripts/quietgram-rebase.sh OLD_BASE NEW_BASE NEW_CANDIDATE_BRANCH" >&2
    echo "Fetch upstream first and pass verified release tags or full commit SHAs." >&2
    exit 2
fi
old_base=$(git rev-parse --verify "${1}^{commit}")
new_base=$(git rev-parse --verify "${2}^{commit}")
candidate=$3
git check-ref-format --branch "$candidate" >/dev/null
if [[ -n "$(git status --porcelain)" ]]; then
    echo 'The working tree must be clean before rebasing.' >&2
    exit 1
fi
if git show-ref --verify --quiet "refs/heads/$candidate"; then
    echo 'Choose a new candidate branch; existing branches are never overwritten.' >&2
    exit 1
fi
git merge-base --is-ancestor "$old_base" HEAD
old_tip=$(git rev-parse HEAD)
git branch "$candidate" "$old_tip"
git rebase --onto "$new_base" "$old_base" "$candidate"
git range-diff "$old_base..$old_tip" "$new_base..$candidate"
echo 'Candidate prepared. Review new UI entry points and publishing guards, update provenance/version code, and run APK/phone checks.'
echo 'The previous branch and all published tags are unchanged. Nothing was pushed.'
