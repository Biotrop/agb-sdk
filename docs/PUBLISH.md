# Publish the package

## Prerequisites

- [poetry](https://python-poetry.org/docs/#installation)
- [twine](https://twine.readthedocs.io/en/stable/installation/)

## Steps

1. Build the package

```bash
poetry build --format wheel
```

2. Upload the package to the repository

```bash
poetry publish
```
