# Gooey
![Version](https://img.shields.io/github/v/release/GooeyBot/Gooey?include_prereleases)
[![GooeyBot](https://circleci.com/gh/GooeyBot/Gooey.svg?style=shield)](https://app.circleci.com/pipelines/github/GooeyBot/Gooey)
[![Issues](https://img.shields.io/github/issues/GooeyBot/Gooey)](https://github.com/GooeyBot/Gooey/issues)

> Gooey is a Reddit bot framework built around PRAW to simplify the creation of bots for non-technical users.

<p align="center">
  <img src="https://imgur.com/u0P6WdQ.png">
</p>

Gooey is meant to be a GUI (pronounced Gooey) for building bots visually with minimal amounts of code and Python knowledge. It can support everything from simple moderation tasks similar to Reddit AutoModerator to advanced features such as responding to commands and subreddit currencies/economies.

## Demo

See below for how easy it is to recreate the delta system from [/r/changemyview](https://www.reddit.com/r/changemyview/) using Gooey!

![gooey-demo gif](https://imgur.com/ZP3OyJ9.gif)

## Installation & Usage

#### NOTE: This installation and usage documentation is very much a work in progress and will likely change significantly prior to release of Gooey

For now, Gooey only supports Unix distributions (i.e. Linux, Mac). Windows is a possibility, however priority is for users who want to host the bot on their own machine (or a lightweight single-board-computer like Raspberry Pi), or deploy to a cloud hosting service such as Heroku.

First, open up a terminal window, then:

1. `git clone` this repository -- Downloads the source code
2. `cd gooey` -- Change directory to the `gooey` folder
3. `sh setup.sh` -- This will set up your machine with Gooey, including downloading requirements and setting up a virtual environment
4. `flask run` -- Start a server in development mode!
5. Your server is listening by default on `localhost:5000`! You can now navigate to a web browser and visit `http://localhost:5000/` to access the control panel.

#### The next section will definitely change in the future!

You can create a bot configuration or manage an existing configuration from the control panel. 

Creating a bot is easy -- You'll need a standard Reddit account (recommended not to use your personal one!), and then you can navigate to [https://www.reddit.com/prefs/apps](https://www.reddit.com/prefs/apps) to register a new script. If you need help, you can refer to [this post](https://www.reddit.com/r/RequestABot/comments/cyll80/a_comprehensive_guide_to_running_your_reddit_bot/) under the `OAuth` section for how these fields should be filled out.

After that, you can copy them over to Gooey by clicking `Create a Bot`! You'll also get the option to select what kind of bot Gooey is (NOTE: As of June 2020 the only option is `Economy`, more to come later).

Next, you'll need to tell Gooey what to do. Begin by enabling functions and adding attributes, then click save.

For now, the only way to run the bot is through the terminal, so you'll need to navigate to `gooey/gooey` and run `python gooey.py`. This will start the bot with the configuration you generated.

## Under the Hood

Gooey is actually 2 parts: **Control Panel** and **Gooey**.

#### Control Panel

Control panel is a Flask app that generates JSON configurations to be read by Gooey. It uses WTForm to dynamically load forms from a schema which in turn tells Control Panel how to build each configuration.

#### Gooey

Gooey is a Reddit bot built around PRAW that can load functions based on a configuration file. It loads the correct handler and acts on comments or submissions to call the correct functions and respond in a user-configurable way.

## Still TODO:

* Support more bot functions!
* Deployable to Heroku Free Tier
  * This means converting from the existing SQLite database to something else
  * Need to scale a worker to connect the front end to the bot
* Import existing configurations
  * This would make configurations shareable!
* Documentation for developers

## Meta

Tyler Porter – tyler.b.porter@gmail.com

Distributed under the MIT license. See ``LICENSE`` for more information.

[https://github.com/pawptart/Gooey/blob/master/LICENSE](https://github.com/pawptart/Gooey/blob/master/LICENSE)

## Attributions

Lava lamp icon made by <a href="https://www.flaticon.com/authors/those-icons" title="Those Icons">Those Icons</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a>.