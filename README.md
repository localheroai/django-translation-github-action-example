# Django translation with a GitHub Action

This repo shows how to translate a Django app's gettext `.po` files automatically on every pull request with a GitHub Action. When a pull request adds or changes a string, the workflow runs `makemessages` and [Localhero.ai](https://localhero.ai) translates the new messages into Swedish, Polish and Arabic. The translated `.po` files are committed back to the same pull request. Code and translations merge together.

## How it works

The app is a single team settings page with English source strings in a template and a view. On each pull request that touches Python, templates or catalogs, [`localhero-translate.yml`](.github/workflows/localhero-translate.yml) runs `makemessages --keep-pot`, which writes new strings to `locale/django.pot` and every target catalog. The [Localhero.ai action](https://github.com/localheroai/localhero-action) then compares the branch with its base and translates only the messages that are new or still empty. Each language gets as many plural forms as its `Plural-Forms` header asks for: two in Swedish, four in Polish (Django's header adds one for fractions) and six in Arabic.

A second workflow, [`ci.yml`](.github/workflows/ci.yml), compiles the catalogs and runs tests that render the page in every language. It also runs `npx @localheroai/cli check`, which fails when a message has no translation or is missing a plural form. That catches what a green test run misses: Django falls back to English without complaining.

## Set it up in your own Django project

1. Run `npx @localheroai/cli init` in the project root. It detects Django from `manage.py`, writes [`localhero.json`](localhero.json) and offers to create the workflow.
2. Add your API key as the repository secret `LOCALHERO_API_KEY` under Settings, Secrets and variables, Actions. You get a key from [your account](https://localhero.ai/api-keys).
3. Commit `localhero.json`, the workflow and `locale/django.pot`. The `.pot` is your source catalog and belongs in git. `init` offers to create it if you don't have one.
4. Install the [Localhero.ai GitHub App](https://localhero.ai/docs/github-app). Without it the translation commit is pushed with `GITHUB_TOKEN` and GitHub won't run your CI on it automatically.

The full guide, with uv and Poetry setups and how plurals work, is at [localhero.ai/docs/django](https://localhero.ai/docs/django).

## What a translation pull request looks like

Say your branch adds `{% translate "Delete team" %}` to the template. You don't need to run `makemessages` yourself. The workflow adds a commit called `Update translations` to your branch, with the number of messages, the languages and a link to review them on Localhero.ai. The diff has the new message in `locale/django.pot` and a translated entry in each catalog:

```diff
+#: teams/templates/teams/team_settings.html:72
+msgid "Delete team"
+msgstr "Ta bort teamet"
```

The action also comments on the pull request with a link to the review page. When a reviewer edits a translation there, **Sync to GitHub** sends it back as a `Sync translations` commit on the same branch.

## Run it locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py compilemessages --ignore .venv
python manage.py runserver
```

Open http://localhost:8000/ for English, or `/sv/`, `/pl/` and `/ar/` for the translations. `compilemessages` needs GNU gettext (`brew install gettext` or `apt-get install gettext`).

Tests and the translation check:

```bash
python manage.py test
npx @localheroai/cli check
```

## License

MIT
