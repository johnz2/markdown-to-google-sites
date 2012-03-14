# Author: john jensen (john@z2live.com)

import sys
import getopt

import unicodedata
import markdown2

def markdown_to_google_sites_entry(input_filename, debugging=False):
    markdown_to_google_sites(input_filename, verbose_output=debugging,
                            print_markdown_html=debugging)

def markdown_to_google_sites(input_filename, print_markdown_html=False,
                            verbose_output=False,
                            script_output_in_ascii=True,
                            script_output_banner_string="[markdown-to-google-sites] "):
    
    def script_print(print_string, is_verbose=False, show_banner=True):
        def clean_string_to_ascii(string):
            return unicodedata.normalize('NFKD', string).encode('ascii', 'ignore')
        
        if script_output_in_ascii:
            output_string = clean_string_to_ascii(print_string)
        else:
            output_string = print_string
    
        if show_banner:
            print("{0}{1}".format(script_output_banner_string, output_string))
        else:
            print(output_string)

    def markdown_file_to_html_string(input_filename,
                                     print_file_contents=False):

        def string_from_file(filename):
            f = open(filename)
            raw_string_from_file = f.read()
            return raw_string_from_file
            
        def markdown_string_to_html(md_string):
            string_converted_to_markdown = markdown2.markdown(md_string)
            return string_converted_to_markdown
        
        #
        md_string   = string_from_file(input_filename)
        html_string = markdown_string_to_html(md_string)

        if print_file_contents:
            script_print(html_string, show_banner=False)
        
        return html_string
    #
    html_string = markdown_file_to_html_string(input_filename)

    if print_markdown_html:
        script_print(html_string, show_banner=False)

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

            return markdown_to_google_sites("mdtest.md", True)
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