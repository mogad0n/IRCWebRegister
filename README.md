# IRC Web Registration

## Introduction

This is a basic still WIP framework for registering an account on an ircd using a webform.

## Features

- It relies on the draft IRCv3 spec [draft/account-registration](https://ircv3.net/specs/extensions/account-registration.html)
- It utilizes the flask framework and `WEBIRC` to relay remote host ip address.
- Can be tweaked to allow registration attempts from exit-nodes and other unsavory hosts allowing them to securely work with the `require-sasl` constraint if needed.

## Requirements

This will work with python3.6 and above.

It is recommended to work within a virtual environment.

1. `mkdir ircwebreg && cd ircwebreg`
2. Clone this repository.
3. `python3 -m venv venv`
4. `source venv/bin/activate`
5. `pip install -r requirements.txt`

## Installation and Setup

Todo!

### Note

Only works with setups not requiring verification at this moment.
