
import argparse
import os
import pprint
import re
import sys
from pathlib import Path

from markdown_it import MarkdownIt
from markdown_it.renderer import RendererHTML
from markdown_it.token import Token
from markdownify import markdownify


def rule_add_toc_after_h1(renderer: RendererHTML, tokens: list[Token], idx, options, env):
    t = tokens[idx]
    #print(f"matched rule: token(type={t.type}, tag={t.tag})")
    if t.tag == 'h1':
        #import pdb; pdb.set_trace()
        fence = Token(type='fence', tag='code', info='{contents}', content=':local:\n:depth: 2\n', nesting=0, block=True)
        tokens.insert(idx + 1, fence)
    return renderer.renderToken(tokens, idx, options, env)


def markdownify_code_language_callback(el) -> str:
    try:
        code_lang = el.find('code')['class'][0]
        #import pdb; pdb.set_trace()
        match = re.search(r'\{[^}]*\}', code_lang)
        return match.group(0)
    except:
        return ''


def main():
    parser = argparse.ArgumentParser(
        usage=
f"""{sys.argv[0]} [-o OUTPUT-PATH] INPUT-FILE

Parse the Markdown file specified by INPUT-FILE and rewrite it with Sphinx directives.

The optional OUTPUT-PATH controls where the rewritten input is written to. If not
specified then the rewritten input is printed to stdout. If OUTPUT-PATH does not exist
then a new file is created at that path. If OUTPUT-PATH refers to an existing directory
then <INPUT-FILENAME> is created in that directory, overwriting the file if it exists.
Otherwise the file at OUTPUT-PATH is overwritten.

If --create-directories is specified then any missing intermediate directories in the
OUTPUT-PATH are created before writing the output file.
""")

    # parse command-line arguments
    parser.add_argument("infile", type=str, metavar="INPUT-FILE",
                        help="The input Markdown file.")
    parser.add_argument("-o","--out", dest='outpath', type=str, default=None, metavar="OUTPUT-PATH",
                        help="The optional output path.")
    parser.add_argument("-c","--create-directories", dest='create_dirs', action='store_true',
                        help="If specified then create intermediate directories as needed.")
    args = parser.parse_args(sys.argv[1:])

    # construct the markdown parser and add render rules
    md = MarkdownIt()
    md.add_render_rule('heading_close', rule_add_toc_after_h1)

    # load the input file and render as HTML
    input = None
    with open(args.infile, 'r') as f:
        input = f.read()
    #tokens = md.parse(input)
    #pprint.pp(tokens)
    html = md.render(input)

    # render HTML string back to markdown
    output = markdownify(html, code_language_callback=markdownify_code_language_callback)

    if args.outpath:
        outpath = args.outpath
        if os.path.isdir(outpath):
            outdir = Path(outpath)
            outpath = outdir / Path(args.infile).name

        if args.create_dirs:
            os.makedirs(Path(outpath).parent, exist_ok=True)

        print(f"writing output to {outpath}")
        with open(outpath, "w") as f:
            f.write(output)
    else:
        sys.stdout.write(output)


if __name__ == '__main__':
    try:
        main()
    except BrokenPipeError:
        pass