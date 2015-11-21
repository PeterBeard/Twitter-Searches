# Twitter-Searches
Twitter-searches is a command-line utility for performing Twitter searches.

# Requirements
* tweepy
* openpyxl

# Configuration
Configuration is stored in config.ini. Copy sample_config.ini to initialize this file, then fill in your details. Supported output formats are CSV, XLS, and XLSX.

# Usage
```
usage: twitter-search.py [-h] [-l LANG] [-f FORMAT] [-o OUTFILE] [-t TIME]
                         [-n NUMBER]
                         term

positional arguments:
  term                  The term(s) to search for

optional arguments:
  -h, --help            show this help message and exit
  -l LANG, --lang LANG  The desired language of returned tweets (ISO 639-1)
  -f FORMAT, --format FORMAT
                        The output format. Options are csv or xls.
  -o OUTFILE, --outfile OUTFILE
                        The name of the output file. Output will be on STDOUT
                        if not specified.
  -t TIME, --time TIME  The distance in the past to search. Understands days,
                        hours, minutes, seconds (d, h, m, s).
  -n NUMBER, --number NUMBER
                        The number of tweets to return. Default is no limit.
```

By default, search results will be written to STDOUT in the desired format, so something like this:

```twitter-search.py "something" > test.csv```

will work. This doesn't work with XLS or XLSX as they are binary formats.
