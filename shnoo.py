import praw
import argparse
from textwrap import fill

VERSION = 0.1

class colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

parser = argparse.ArgumentParser(description='Enjoy a Reddit sample at the CLI.')
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
parser.add_argument('--version', '-v', action='version', version=str(VERSION))

args = parser.parse_args()

def comment_tree(root, prepend=''):
    name = 'deleted' if not root.author else root.author.name
    text = colors.GREEN + '[' + name + ']' \
           + colors.ENDC + root.body + '\n'
    print(fill(text, args.l, subsequent_indent=prepend,
               replace_whitespace=False),
          end='\n\n')
    for reply in root.replies:
        comment_tree(reply, prepend=prepend + '     ')

r = praw.Reddit(user_agent='reddit cli by Liz')
r.login(args.u, args.p, disable_warning=True)
submissions = r.get_subreddit(args.s).get_top(limit=args.n)

for i, submission in enumerate(submissions):
    submission.replace_more_comments()
    sep = '=' * (2 + len(submission.title))
    print(colors.BOLD + colors.HEADER + '(%d/%d) %s\n' % (i, args.n, submission.title) +
          submission.permalink + colors.ENDC, end='\n\n')
    for comment in submission.comments:
        comment_tree(comment)
