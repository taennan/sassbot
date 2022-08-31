
# SassBot

A simple demo of various Web and ML principles

## What this is:

- An SPA built with [`Svelte`][svelte] and served by...
- A `Python` and [`Flask`][flask] backend, which returns...
- Responses determined by a [`Tensorflow2`][tensorflow] text classifier...
- All so I could complete a few tasks on the ScoobyApps [milestone list][scooby-milestones]

## What this isn't:

- Smooth round the edges

## Getting Started

To play around with the app, you'll need a few prerequisites:

- Python == v3.9 (**no later!**)
- Yarn
- Node >= v16

Then simply:

- Clone the [repo][repo] and `cd` into it

```bash
git clone https://github.com/taennan/sass-bot.git <dir-name>
cd <dir-name>
```

- Download the ML [training dataset][twitter-dataset] (you'll need a
[Kaggle][kaggle] account for this one) and save it at
`./back/src/data/unprocessed/main-data-unprocessed.csv`. See *Extra Configuration*
below if you don't want to use this dataset

- Run `source` on the file `./shellentry.sh` to use the `sassbot` command line interface

```bash
source ./shellentry.sh
```

- Build the web app and train the ML algorithm with:

```bash
sassbot build
```

- Wait a **long** time for the text classifier to finish training.

- Start the server with:

```bash
sassbot run
```

- And visit the site at `localhost:5000`

The web app itself is pretty simple, you can't get lost there

## Extra configuration

To choose the port the website is served at, do the above with one difference, _i.e_, at the build step, run:

```bash
sassbot build -p <port>
```

If the port ever needs to be changed after the initial build, you only need to rebuild the frontend with the `-f` arg:

```bash
sassbot build -f -p <port>
```

In case the dataset mentioned in the previous section is not to your liking,
you can really use any text sentiment dataset as long as:

- It is stored in a `csv` style file at path `<cloned-repo>/back/src/ml/data/processed/<data-file>`
- It's columns contain text (`str`) and then sentiment (`int`'s of either 0 or 1)
- It's values are separated by commas ( , )

Then during the build, run:

```bash
# The '--p-data' arg must be set as an empty
#  string to stop the data preprocessing step
# The full path to the data file does not have
#  to be specified, just it's name
sassbot build --t-data <data-file> --p-data ''
```

If you don't want to rebuild the frontend every time you train the text classifier, use the `-b` arg:

```bash
sassbot build -b --t-data <data-file> --p-data ''
```

It must be noted however, that a different dataset from the one the text
classification model was developed on will result in very different performances.

## Wait! It didn't work!

Darn, that's too bad.

Try checking if you entered the correct args and commands into the `sassbot` CLI. See all available options and usages with:

```bash
sassbot help
```

If **that** didn't work, double darn! You're going to have to start the project manually.

First, ensure you have the correct prerequisites (mentioned in _Getting Started_ above), then:

- Build the Svelte app

```bash
cd <cloned-repo>/front

yarn install
yarn build
```

- If you want to configure the port the website is served at, change the
`VITE_PORT` environment var in the file `<cloned-repo>/front/.env`. It is `5000`
by default.

- Configure the backend's `Python3.9` virtual environment. A virtual environment
is not strictly necessary, but recommended

```bash
cd <cloned-repo>/back

python3.9 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

- If using the [1.6M Twitter Tweets Dataset][twitter-dataset], download and save
it at the path `<cloned-repo>/back/src/ml/data/unprocessed/main-data-unprocessed.csv`
then preprocess it with:

```bash
python src/ml/setup.py process
```

- Else if using a custom dataset, ignore the above step and see
_Extra Configuration_ above for details on how this can be done

- Train and save the text classifier on the dataset

```bash
python src/ml/setup.py model
```

- Then set up and start the server

```bash
cd src
# Explicitly specifying the port is only necessary if the VITE_PORT
#  environment var is set to anything apart from 5000
flask run --port <port>
```

- Finally, visit the site at `localhost:<port>`

## Contributing

The project is happy to receive criticisms and have it's problems pointed out
on it's GitHub [issues page][repo-issues], or, if you are a member of the
`ScoobyApps` team,  send me a message on [Slack][slack].

## License

This project is unlicensed. Use it in whatever morally correct way you'd like.

[repo]: https://github.com/taennan/sass-bot.git
[repo-issues]: https://github.com/taennan/sass-bot/issues
[kaggle]: https://www.kaggle.com
[twitter-dataset]: https://www.kaggle.com/datasets/kazanova/sentiment140

[scooby-milestones]: https://scoobyapps.com/board/index.php?topic=10.msg13#new
[slack]: https://slack.com

[svelte]: https://svelte.dev
[flask]: https://flask.palletsprojects.com/en/2.1.x/
[tensorflow]: https://www.tensorflow.org
