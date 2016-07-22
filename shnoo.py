#!/usr/bin/python3

import praw
import argparse
from textwrap import fill, wrap

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
                    help='max number of comment threads to display, per post')
parser.add_argument('--sort', action='store', metavar='sort_order', type=str, default='hot',
                    help='submission sort order: hot, rising, new, or top')
parser.add_argument('-f', '--fetch-all', action='store_const', dest='fetch_all', default=False, const=True,
                    help='fetch all comments from every thread (limited to 32 API requests)')
parser.add_argument('--links', action='store_const', dest='links_only', default=False, const=True,
                    help='display only links, no comments')
parser.add_argument('--no-color', dest='color', action='store_const', default=True, const=False,
                    help="don't use colors in output")
parser.add_argument('--no-url', dest='show_url', action='store_const', default=True, const=False,
                    help="don't display submission URL, just Reddit.com thread link")
parser.add_argument('--version', '-v', action='version', version=str(VERSION))

args = parser.parse_args()

if args.color:
    class colors:
        PINK = '\033[95m'
        BLUE = '\033[94m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        CYAN = '\033[96m'
        RED = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
else:
    class colors:
        PINK = BLUE = GREEN = YELLOW = RED = ENDC = BOLD = UNDERLINE = ''

def comment_tree(root, prepend='', op=''):
    name = 'deleted' if not root.author else root.author.name
    color = colors.BLUE
    if name == op:
        color = color + colors.BOLD + colors.UNDERLINE

    print("%s%s'%s'" % (prepend, color, name) + colors.ENDC + ' { ' + colors.CYAN
          + "'%s'" % root.permalink.split('/')[-1] + colors.ENDC + ':')
    print(prepend + INDENT + votestring(root))

    text = root.body
    for p in text.split('\n'):
        print(fill(p, args.l, initial_indent=prepend + INDENT,
                   subsequent_indent=prepend + INDENT), end='\n')

    for reply in root.replies:
        if hasattr(reply, 'body'):
            comment_tree(reply, prepend=prepend + INDENT, op=op)

    print(prepend + '}')

r = praw.Reddit(user_agent='shnoo: https://github.com/erosa/shnoo')
r.login(args.u, args.p, disable_warning=True)

if args.sort == 'top':
    submissions = r.get_subreddit(args.s).get_top(limit=args.n, comment_sort='best')
if args.sort == 'rising':
    submissions = r.get_subreddit(args.s).get_rising(limit=args.n, comment_sort='best')
if args.sort == 'new':
    submissions = r.get_subreddit(args.s).get_new(limit=args.n, comment_sort='best')
else:
    if args.sort != 'hot':
        print('%s[ERROR] %s is not a valid subreddit sort order; defaulting to Hot.%s' % (colors.RED, args.sort, colors.ENDC))
    submissions = r.get_subreddit(args.s).get_hot(limit=args.n, comment_sort='best')

def votestring(thing):
    color = colors.GREEN if thing.ups > 0 else colors.RED
    return '[ %sscore%s = %s%s%s ]' % (colors.YELLOW, colors.ENDC, color, str(thing.ups), colors.ENDC)

for i, submission in enumerate(submissions):
    if args.fetch_all:
        submission.replace_more_comments()

    print(fill(submission.title, args.l, initial_indent=colors.BOLD + colors.PINK + '# ',
               subsequent_indent=colors.BOLD + colors.PINK + '# '))
    print(colors.ENDC, end='')
    url = '[ %surl%s = %s ]' % (colors.YELLOW, colors.ENDC, submission.url) if args.show_url else ''
    print(votestring(submission) + url)
    print('[ %sop%s = %s ][ %spermalink%s = %s ]' % (colors.YELLOW, colors.ENDC, submission.author.name,
                                                 colors.YELLOW, colors.ENDC, submission.short_link), end='\n\n')

    if not args.links_only:
        for comment in submission.comments[:args.c]:
            if hasattr(comment, 'body'):
                comment_tree(comment, prepend=' ', op=submission.author.name)
