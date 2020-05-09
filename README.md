# Check-URLs
Script checks accessibility of URLs provided by user.

## Input
* URLs have to provided via txt file named "urls_input.txt" stored in same location as script.
* URLs should be divided by line breaks. Even if there is space or even no space between URLs instead of line break, script validates URLs and then starts to check.

## Output
* Result is saved into txt file named "urls_output.txt".
* Summary report includes validated overview of accessible and non-accessible URLs and their total counts.

## Output Sample
Accessible URLs: 3</b>
\|- https://www.facebook.com/</b>
\|- https://www.youtube.com/
\|- http://www.google.com/
Non-accessible URLs: 1
\|- http://error
