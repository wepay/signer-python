# WePay Signer for Python

[![Source](http://img.shields.io/badge/source-wepay/signer–python-blue.svg?style=flat-square)](https://github.com/wepay/signer-python)
[![Downloads](https://img.shields.io/pypi/dm/wepay-signer.svg?style=flat-square)](https://github.com/wepay/signer-python/releases)
[![Release](https://img.shields.io/github/release/wepay/signer-python.svg?style=flat-square)](https://github.com/wepay/signer-python/releases)
[![Pypi Release](https://img.shields.io/pypi/v/wepay-signer.svg?style=flat-square)](https://pypi.python.org/pypi/wepay-signer)
[![Open Issues](http://img.shields.io/github/issues/wepay/signer-python.svg?style=flat-square)](https://github.com/wepay/signer-python/issues)
[![Build Status](http://img.shields.io/travis/wepay/signer-python/master.svg?style=flat-square)](https://travis-ci.org/wepay/signer-python)
[![Implementation](https://img.shields.io/pypi/implementation/wepay-signer.svg?style=flat-square)](https://python.org)
[![Python Versions](https://img.shields.io/pypi/pyversions/wepay-signer.svg?style=flat-square)](https://python.org)
[![Package Format](https://img.shields.io/pypi/format/wepay-signer.svg?style=flat-square)](http://pythonwheels.com)
[![Stability](https://img.shields.io/pypi/status/wepay-signer.svg?style=flat-square)](https://pypi.python.org/pypi/wepay-signer)
[![Coverage Status](http://img.shields.io/coveralls/wepay/signer-python/master.svg?style=flat-square)](https://coveralls.io/r/wepay/signer-python?branch=master)
[![Code Climate](http://img.shields.io/codeclimate/github/wepay/signer-python.svg?style=flat-square)](https://codeclimate.com/github/wepay/signer-python)
[![Code Quality](http://img.shields.io/scrutinizer/g/wepay/signer-python.svg?style=flat-square)](https://scrutinizer-ci.com/g/wepay/signer-python)
[![License](https://img.shields.io/github/license/wepay/signer-python.svg?style=flat-square)](https://github.com/wepay/signer-python/blob/master/LICENSE.rst)
[![Author](http://img.shields.io/badge/author-@skyzyx-blue.svg?style=flat-square)](https://github.com/skyzyx)

The **Signer** class is designed for those who are signing data on behalf of a public-private keypair.

In principle, the "client party" has public key (i.e., `client_id`) and a matching private key (i.e., `client_secret`) that can be verified by both the signer and the client (but nobody else as we don't want to make forgeries possible).

The "signing party" has a simple identifier which acts as an additional piece of entropy in the algorithm, and can help differentiate between multiple signing parties if the client party does something like try to use the same public-private keypair independently of a signing party (as is common with GPG signing).

Based on a simplified version of the AWS Signature v4.

This project uses [Semantic Versioning](http://semver.org) for managing backwards-compatibility.

* [API Reference](https://wepay.github.io/signer-python/)

## Examples

```python
from __future__ import print_function
from wepay.signer import Signer
import textwrap

client_id = 'your_client_id'
client_secret = 'your_client_secret'

signer = Signer(client_id, client_secret)
signature = signer.sign(
    token=your_token,
    page=wepay_page_to_visit,
    redirect_uri=partner_page_to_return_to
)

print(textwrap.wrap(signature, 64))
#=> dfbffab5b6f7156402da8147886bba3eba67bd5baf2e780ba9d39e8437db7c47
#=> 35e9a0b834aa21ac76f98da8c52a2a0cd1b0192d0f0df5c98e3848b1b2e1a037

querystring = signer.generate_query_string_params(
    token=your_token,
    page=wepay_page_to_visit,
    redirect_uri=partner_page_to_return_to
)

#=> client_id=your_client_id&
#=> page=https://wepay.com/account/12345&
#=> redirect_uri=https://partnersite.com/home&
#=> stoken=dfbffab5b6f7156402da8147886bba3eba67bd5baf2e780ba9d39e8437db7c47...&
#=> token=token=acb1b5b8-af32-5356-bd2a-5bac74366e4c
```

## Installation

Testing occurs against the following versions:

* Python 2.7
* Python 3.3
* Python 3.4
* Python 3.5
* Python 3.6 (dev)
* Pypy (≈2.7.10)
* Pypy3 (≈3.2.5)

```bash
pip install wepay-signer
```

And include it in your scripts:

```python
from wepay.signer import Signer
```


## Development

* You can develop in any supported version of Python.

* Using [pyenv] to manage your Pythons is _highly-recommended_. Testing locally **depends** on it.

* Install [VirtualEnv] for your development environment, and _activate_ the environment.

  ```bash
  pip install virtualenv
  virtualenv .vendor
  source .vendor/bin/activate
  ```

* Install the `requirements.txt`.

  ```bash
  pip install -r requirements.txt
  ```

* When you make changes, make sure that you run the linter and fix anything that's broken.

  ```bash
  make lint
  ```


## Testing

We use [tox] to handle local testing across multiple versions of Python. We install multiple versions of Python at a time with [pyenv].

1. Install [pyenv] on your own before running tests.

1. You need to install all of the supported versions of Python. (This will take a while.) If you would prefer to install your own copies of the supported Python versions (listed above), feel free to manage them yourself.

   ```bash
   make install-python
   ```

1. You can run the tests as follows:

   ```bash
   make test
   ```


## API Reference

### Building local docs

```bash
make docs
open docs/signer/index.html
```

### Building and pushing docs

```bash
make pushdocs
```

Docs can be viewed at <https://wepay.github.io/signer-python/>.


## Deploying

1. The `Makefile` (yes, `Makefile`) has a series of commands to simplify the development and deployment process.
1. Also install [Chag](https://github.com/mtdowling/chag). This is used for managing the CHANGELOG and annotating the Git release correctly.

### Updating the CHANGELOG

Make sure that the CHANGELOG.md is human-friendly. See http://keepachangelog.com if you don’t know how.

### `make`

Running `make` by itself will show you a list of available sub-commands.

```bash
$ make
all
build
clean
docs
install
install-python
lint
push
pushdocs
readme
tag
test
version
```

### `make readme`

If you make changes to `README.md`, then this will use [Pandoc] to output a `README.rst` file in the [reStructuredText] format used by [distutils], [Sphinx] and most of the Python community.

You must have [Pandoc] installed on your local system.

> **NOTE:** Initial install via `brew install pandoc` takes about 8–10 hours. Updates are much faster. [Using the installer](https://github.com/jgm/pandoc/releases) is **much** faster for initial installation, but updates are entirely manual.

### `make version`

Sets the version number that will be used by other `make` tasks related to packaging and bundling.

### `make tag`

This will make sure that the `CHANGELOG.md` is properly datestamped, add the CHANGELOG contents to the Git commit message, commit them, then create a Git commit which can be pushed upstream.

### `make buildpip`

This will bundle-up your package in preparation for uploading to [Pypi].

### `make pushpip`

This will take your bundled package and upload it securely to [Pypi] using the `twine` package.

### Drafting a GitHub release

1. Go to https://github.com/wepay/signer-python/tags
1. Find the new tag that you just pushed. Click the ellipsis (`…`) to see the commit notes. Copy these.
1. To the right, choose _Add release notes_. Your _Tag version_ should be pre-filled.
1. The _Release title_ should match your _Tag version_.
1. Inside _Describe this release_, paste the notes that you copied on the previous page.
1. Choose _Publish release_.
1. Your release should now be the latest. https://github.com/wepay/signer-python/releases/latest


## Contributing
Here's the process for contributing:

1. Fork Signer to your GitHub account.
2. Clone your GitHub copy of the repository into your local workspace.
3. Write code, fix bugs, and add tests with 100% code coverage.
4. Commit your changes to your local workspace and push them up to your GitHub copy.
5. You submit a GitHub pull request with a description of what the change is.
6. The contribution is reviewed. Maybe there will be some banter back-and-forth in the comments.
7. If all goes well, your pull request will be accepted and your changes are merged in.


## Authors, Copyright & Licensing

* Copyright (c) 2015-2016 [WePay](http://wepay.com)

See also the list of [contributors](https://github.com/wepay/signer-python/graphs/contributors) who participated in this project.

Licensed for use under the terms of the [Apache 2.0] license.

  [Apache 2.0]: http://opensource.org/licenses/Apache-2.0
  [distutils]: https://docs.python.org/3/library/distutils.html
  [Pandoc]: http://pandoc.org
  [pyenv-virtualenvwrapper]: https://github.com/yyuu/pyenv-virtualenvwrapper
  [pyenv]: https://github.com/yyuu/pyenv
  [reStructuredText]: http://docutils.sourceforge.net/rst.html
  [Sphinx]: http://www.sphinx-doc.org
  [tox]: https://tox.readthedocs.io
  [VirtualEnv]: https://virtualenv.pypa.io/en/stable/
  [Pypi]: https://pypi.python.org/pypi
