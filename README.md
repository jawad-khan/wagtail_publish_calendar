# Wagtail Publish Calendar

A Wagtail plugin that provides a calendar view of scheduled publishing and expiry events for any Wagtail content type that supports go-live and expiry dates. This tool helps editors and site managers visualize and manage when content (pages, snippets, or custom models) will go live or expire, directly from the Wagtail admin interface.

[![License: BSD-3-Clause](https://img.shields.io/badge/License-BSD--3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![PyPI version](https://badge.fury.io/py/wagtail-publish-calendar.svg)](https://badge.fury.io/py/wagtail-publish-calendar)
[![publish-calendar CI](https://github.com/wagtail/wagtail-publish-calendar/actions/workflows/test.yml/badge.svg)](https://github.com/wagtail/wagtail-publish-calendar/actions/workflows/test.yml)

---

## Features
- Calendar view of scheduled publishing and expiry for any Wagtail content type (pages, snippets, custom models)
- Interactive event editing (change go-live and expiry dates)
- Color-coded events for clarity
- Integration with Wagtail admin menu
- Extensible for custom content types

## Supported Versions
- **Python**: 3.8+
- **Django**: 3.2, 4.2, 5.0
- **Wagtail**: 4.0, 5.0, 5.1

## Installation

Install from PyPI:
```sh
python -m pip install wagtail-publish-calendar
```

Or for development:
```sh
git clone https://github.com/wagtail/wagtail-publish-calendar.git
cd wagtail-publish-calendar
python -m pip install -e '.[testing]' -U
```

Add to your `INSTALLED_APPS`:
```python
INSTALLED_APPS = [
    # ...
    'wagtail_publish_calendar',
]
```

## Usage

After installation, log in to the Wagtail admin. You will see a "Content Scheduler" menu item. Click to view the calendar of scheduled publishing and expiry events for all supported content types. You can interactively update dates via the calendar interface.

## Configuration

No configuration is required for basic usage. For advanced customization (e.g., custom models, event colors), extend the views or templates in your own app.

## API Reference

- **calendar_view**: Renders the calendar and form.
- **get_page_schedule_dates**: Returns JSON of scheduled events for all supported content types.
- **update_page_schedule_date**: Updates go-live/expiry dates via AJAX for any supported object.

See `wagtail_publish_calendar/views.py` for details.

## Development

Clone the repo and install dependencies:
```sh
git clone https://github.com/wagtail/wagtail-publish-calendar.git
cd wagtail-publish-calendar
python -m pip install -e '.[testing]' -U
```

### Running Tests

Run all tests:
```sh
tox
```
Or run a specific environment:
```sh
tox -e python3.11-django4.2-wagtail5.1
```

### Linting & Pre-commit

This project uses [pre-commit](https://github.com/pre-commit/pre-commit):
```sh
pre-commit install
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines. Issues and pull requests are welcome!

## License

BSD-3-Clause. See [LICENSE](LICENSE).

## Links & Resources
- [Documentation](https://github.com/wagtail/wagtail-publish-calendar/blob/main/README.md)
- [Changelog](https://github.com/wagtail/wagtail-publish-calendar/blob/main/CHANGELOG.md)
- [Contributing](https://github.com/wagtail/wagtail-publish-calendar/blob/main/CONTRIBUTING.md)
- [Discussions](https://github.com/wagtail/wagtail-publish-calendar/discussions)
- [Security](https://github.com/wagtail/wagtail-publish-calendar/security)

---

For questions or support, open an issue or join the discussions on GitHub.
