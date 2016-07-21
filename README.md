# shnoo.py

For when you need that reddit fix, but your classmates/manager/fellow
coffeeshop patrons don't need to know about it.

Or, for when you're tired of reddit.com's appealing and intuitive user interface and want to
stare at awkwardly-formatted console output instead.

## Usage

```
[17:55:32][root@dev][/s/shnoo]$ ./shnoo.py -h
usage: shnoo.py [-h] [-u username] [-s subreddit] [-p password] [-l linewidth]
                [-n num_posts] [-c max_comments]
                [--sort submission sort order] [-f] [--links] [--no-color]
                [--version]

Get your Reddit fix at the CLI .

optional arguments:
  -h, --help            show this help message and exit
  -u username           reddit username
  -s subreddit          subreddit
  -p password           reddit password
  -l linewidth          maximum output line width
  -n num_posts          number of posts to output
  -c max_comments       max number of comment threads to display
  --sort submission sort order
                        submission sort order: hot, rising, new, or top
  -f, --fetch-all       fetch all comments from every thread (limited to 32
                        API requests)
  --links               display only links, no comments
  --no-color            don't use colors in output
  --version, -v         show program's version number and exit
```

## Examples

Get the current top 5 stories from /r/news along with the top 3 comment threads, and save output
to topnews.txt:

```
shnoo.py -u USER -p PASSWORD -s news -n 5 -c 3 > topnews.txt
```

Get the 50 best comment threads from the all-time #1 AskReddit post (10/10 with rice), with the maximum number of comments expanded in each thread:

```
shnoo.py -u USER -p PASSWORD -s AskReddit -c 50 -f --sort top
```
