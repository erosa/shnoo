# shnoo.py

For when you need that reddit fix, but your classmates/manager/fellow
coffeeshop patrons don't need to know about it.

Or, for when you're tired of reddit.com's appealing and intuitive user interface and want to
stare at awkwardly-formatted console output instead.

I suggest piping output to a text file and viewing with a pager like `less` or `more`. If
you want to view colored output using vim, check out the
[AnsiEsc](http://www.vim.org/scripts/script.php%3Fscript_id%3D302) vim script.

<img src="http://imgur.com/38MBDj9.jpg" height="400" />   <img
src="http://imgur.com/Pjsl1a8.jpg" height="400" />

## Examples

Get the current top 5 stories from /r/news along with the top 3 comment threads, and save output
to topnews.txt:

```
$ ./shnoo.py -u USER -p PASSWORD -s news -n 5 -c 3 > topnews.txt
```

Get the 25 best comment threads from the all-time #1 AskReddit post (10/10 with rice), with the maximum number of comments expanded in each thread:

```
$ ./shnoo.py -u USER -p PASSWORD -s AskReddit -c 50 -f --sort top
```

Get the top 50 ShowerThoughts submissions, showing just title, author, score, and
permalink; no comments or submission url.

```
$ ./shnoo.py -u USER -p PASSWORD --links -s showerthoughts -n 50 --no-url
```

## Usage

```
usage: shnoo.py [-h] [-u username] [-s subreddit] [-p password] [-l linewidth]
                [-n num_posts] [-c max_comments] [--sort sort_order] [-f]
                [--links] [--no-color] [--no-url] [--version]

Get your Reddit fix at the CLI .

optional arguments:
  -h, --help         show this help message and exit
  -u username        reddit username
  -s subreddit       subreddit
  -p password        reddit password
  -l linewidth       maximum output line width
  -n num_posts       number of posts to output
  -c max_comments    max number of comment threads to display
  --sort sort_order  submission sort order: hot, rising, new, or top
  -f, --fetch-all    fetch all comments from every thread (limited to 32 API
                     requests)
  --links            display only links, no comments
  --no-color         don't use colors in output
  --no-url           don't display submission URL, just Reddit.com thread link
  --version, -v      show program's version number and exit
```

## Todo

- [ ] implement OAuth features
- [ ] add interactive option
- [ ] enable contributions
