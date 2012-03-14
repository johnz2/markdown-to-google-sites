import sys
import getopt

import codecs
import unicodedata
import markdown2

def markdown_to_google_docs_script_entry(input_filename, debugging=False):
    markdown_to_google_docs(input_filename, verbose_output=debugging,
                            print_markdown_html=debugging)

def markdown_to_google_docs(input_filename, print_markdown_html=False,
                            verbose_output=False):
                  
    def cleanup_string_for_console(string):
        return unicodedata.normalize('NFKD', string).encode('ascii', 'ignore')

    def markdown_file_to_html_string(input_filename,
                                     print_file_contents=False):

        def string_from_file(filename):
            f = open(filename)
            raw_string_from_file = f.read()
            #f = codecs.open(filename, encoding='utf-8')
            #return raw_string_from_file.encode('utf8')
            return raw_string_from_file
            
        def markdown_string_to_html(md_string):
            string_converted_to_markdown = markdown2.markdown(md_string)
            return string_converted_to_markdown
        
        #
        md_string   = string_from_file(input_filename)
        html_string = markdown_string_to_html(md_string)

        if print_file_contents:
            print(cleanup_string_for_console(html_string))
        
        return html_string
    #
    html_string = markdown_file_to_html_string(input_filename)

    if print_markdown_html:
        print(cleanup_string_for_console(html_string))

    return 1

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h", ["help"])

            return markdown_to_google_docs_script_entry("mdtest.md", True)
        except getopt.error, msg:
             raise Usage(msg)
        # more code, unchanged
    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2

if __name__ == "__main__":
    sys.exit(main())



print "what"