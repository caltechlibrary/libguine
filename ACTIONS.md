# GitHub Actions

## Workflows

- [Compile Artifacts](#compile-artifacts)
- [Deploy Components](#deploy-components)
- [Build & Deploy Notices](#build--deploy-notices)
- [Manually Publish Fragments](#manually-publish-fragments)

## Compile Artifacts

The [Compile Artifacts workflow](https://github.com/caltechlibrary/libguine/blob/main/.github/workflows/compile.yml) is set up as a resuable workflow that is triggered with the [Deploy Components workflow](https://github.com/caltechlibrary/libguine/blob/main/.github/workflows/deploy.yml).

See [`.github/workflows/compile.py`](https://github.com/caltechlibrary/libguine/blob/main/.github/workflows/compile.py) for the logic that determines which files to compile and how to compile them.

## Deploy Components

The [Deploy Components workflow](https://github.com/caltechlibrary/libguine/blob/main/.github/workflows/deploy.yml) downloads the artifacts created in the [Compile Artifacts workflow](https://github.com/caltechlibrary/libguine/blob/main/.github/workflows/compile.yml) and deploys them to LibGuides.

See [`.github/workflows/deploy.py`](https://github.com/caltechlibrary/libguine/blob/main/.github/workflows/deploy.py) for the logic that determines which files to deploy and how to deploy them.

## Build & Deploy Notices

A scheduled GitHub Actions job in [`.github/workflows/notices.yml`](https://github.com/caltechlibrary/libguine/blob/main/.github/workflows/notices.yml) runs periodically that executes [`.github/workflows/notices.py`](https://github.com/caltechlibrary/libguine/blob/main/.github/workflows/notices.py) which does the transformation from RSS to HTML fragments. These fragments are then committed and pushed to this repository under [`fragments/notices`](https://github.com/caltechlibrary/libguine/tree/main/fragments/notices).

The final steps in the job conditionally publish any updated HTML fragments with GitHub Pages. The [HTML fragments are now publicly available](https://caltechlibrary.github.io/libguine/notices/) for our JavaScript widget without CORS restrictions.

## Manually Publish Fragments

TK
