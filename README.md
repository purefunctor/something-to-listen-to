# something-to-listen-to
![GitHub Workflows](https://img.shields.io/github/checks-status/PureFunctor/something-to-listen-to/main?style=flat-square)
![Coveralls](https://img.shields.io/coveralls/github/PureFunctor/something-to-listen-to/main?style=flat-square)

A command-line tool for getting songs to listen to in Spotify.

## Development
Contributions are welcome! Feel free to open an issue to report bugs or to open a pull request to
add functionality. It's advised to open an issue first if you'd like to add or change a feature; in
this way, changes can be planned ahead which helps save some development time.

This project requires the following development requirements:
* Python (3.9.x)
* Poetry (1.1.x)
* Nox (2021.6.6)

### Tips

[Lint before you push](https://soundcloud.com/lemonsaurusrex/lint-before-you-push); make sure you
install `pre-commit` hooks when developing the project:
```sh
$ poetry run task pre-commit
```

Test your changes; the `test` task allows you to run tests and generate coverage data that you can
view:
```sh
$ poetry run task test
```

Lint and format your code; the `lint` task reports any linting errors through `flake8` while the
`format` tasks cleans up unformatted Python code with `black`.
```sh
$ poetry run task lint
$ poetry run task format
```

You can use `nox` to do it all at once:
```sh
$ nox
```

Virtual environments used by `nox` can be reused using the `-r` flag:
```sh
$ nox -r
```

Redundant installation steps can be eliminated using the `-R` flag:
```sh
$ nox -R
```
