# AI Gender-bias paraphrasing
## GPT3 used to remove bias from the job adverts

Please read the Medium article at ... 

This is a demo of the application for removal of the gender-biased term from job adverts.

## Overview

A static website ready to deploy.
This repo includes all the file and it is ready to deploy to Heroku.

- .env
- .gitignore
- app
- Procfile
- README.md
- requirements.txt
- runtime.txt
- static
- templates



## Installation & Usage

```bash

# change the directory
$ cd fastapi-web-starter
# install packages
$ pip install -r requirements.txt
# start the server
$ uvicorn app.main:app --reload --port 8080
```

Visit [http://127.0.0.1:8080/](http://127.0.0.1:8080/).

## Features

- Highlighting of gender-biased term 
- Automatic paraphrasing 

## Test

All tests are under `tests` directory.

```bash
# Change the directory
$ cd fastapi-web-starter
# Run tests
$ pytest -v
```

## Licence
Boilerplate Frontend: Copyright 2013-2020 Start Bootstrap LLC. Code released under the [MIT](https://github.com/StartBootstrap/startbootstrap-resume/blob/gh-pages/LICENSE) license.
Boilerplate Backend : [Copyright 2021 Shinichi Okada](https://levelup.gitconnected.com/building-a-website-starter-with-fastapi-92d077092864)