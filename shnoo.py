#!/usr/bin/python3

import praw
import argparse
from textwrap import fill

VERSION = 0.1
INDENT = '    '

parser = argparse.ArgumentParser(description='Get your Reddit fix at the CLI .')
parser.add_argument('-u', action='store', metavar='username', type=str,
                    help='reddit username')
parser.add_argument('-s', action='store', metavar='subreddit', type=str,
                    help='subreddit')
parser.add_argument('-p', action='store', metavar='password', type=str,
                    help='reddit password')
parser.add_argument('-l', action='store', metavar='linewidth', type=int, default=100,
                    help='maximum output line width')
parser.add_argument('-n', action='store', metavar='num_posts', type=int, default=3,
                    help='number of posts to output')
parser.add_argument('-c', action='store', metavar='max_comments', type=int, default=100,
                    help='max number of comment threads to display')
parser.add_argument('--sort', action='store', metavar='submission sort order', type=str, default='hot',
                    help='submission sort order: hot, rising, new, or top')
parser.add_argument('-f', '--fetch-all', action='store_const', dest='fetch_all', default=False, const=True,
                    help='fetch all comments from every thread (limited to 32 API requests)')
parser.add_argument('--links', action='store_const', dest='links_only', default=False, const=True,
                    help='display only links, no comments')
parser.add_argument('--no-color', dest='color', action='store_const', default=True, const=False,
                    help="don't use colors in output")
parser.add_argument('--version', '-v', action='version', version=str(VERSION))

args = parser.parse_args()

if args.color:
    class colors:
        HEADER = '\033[95m'
        BLUE = '\033[94m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        RED = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
else:
    class colors:
        HEADER = BLUE = GREEN = YELLOW = RED = ENDC = BOLD = UNDERLINE = ''

def comment_tree(root, prepend='', op=''):
    name = 'deleted' if not root.author else root.author.name
    color = colors.BLUE
    if name == op:
        color = color + colors.BOLD + colors.UNDERLINE

    print("%s%s'%s'" % (prepend, color, name) + colors.ENDC + ": " + colors.YELLOW
          + "'%s':" % root.permalink.split('/')[-1] + colors.ENDC)
    printstats(root, prepend + INDENT)

    text = root.body
    for p in text.split('\n'):
        print(fill(p, args.l, initial_indent=prepend + INDENT,
                   subsequent_indent=prepend + INDENT), end='\n')

    for reply in root.replies:
        if hasattr(reply, 'body'):
            comment_tree(reply, prepend=prepend + INDENT, op=op)

    print(prepend + '}')

r = praw.Reddit(user_agent='reddit cli by Liz')
r.login(args.u, args.p, disable_warning=True)

if args.sort == 'top':
    submissions = r.get_subreddit(args.s).get_top(limit=args.n, comment_sort='best')
if args.sort == 'hot':
    submissions = r.get_subreddit(args.s).get_hot(limit=args.n, comment_sort='best')
if args.sort == 'rising':
    submissions = r.get_subreddit(args.s).get_rising(limit=args.n, comment_sort='best')
if args.sort == 'new':
    submissions = r.get_subreddit(args.s).get_new(limit=args.n, comment_sort='best')

def printstats(thing, prepend=''):
    print('%s[%sup%s%s = %s%s%s%s, ' % (prepend, colors.YELLOW, colors.ENDC, colors.BOLD, colors.ENDC,
          colors.GREEN, str(thing.ups), colors.ENDC), end='')
    print('%sdown%s%s = %s%s%s%s]' % (colors.YELLOW, colors.ENDC, colors.BOLD, colors.ENDC,
          colors.RED, str(thing.downs), colors.ENDC))

for i, submission in enumerate(submissions):
    if args.fetch_all:
        submission.replace_more_comments()

    print(colors.BOLD + colors.HEADER + '# (%d/%d) %s\n' % (i + 1, args.n, submission.title) +
          colors.BOLD + colors.HEADER + '# %s - %s' % (submission.author.name, submission.short_link))
    printstats(submission)

    for comment in submission.comments[:args.c]:
        if hasattr(comment, 'body'):
            comment_tree(comment, prepend=' ', op=submission.author.name)
