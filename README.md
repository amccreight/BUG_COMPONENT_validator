# BUG_COMPONENT_validator

Validator for the BUG_COMPONENT field in the Firefox source code.

Validation steps

1. Download a recent components file from TreeHerder. Look for the "bugzilla" job,
   go to the Artifacts tab, download `components-normalized.json.gz` and `gunzip` it.

2. Run `python3 validate.py --bmo components-normalized.json` to generate a Bugzilla URL.

3. Visit the URL. It will load a JSON file. Click on "save" and save it to `product.json`.

4. Run `python3 validate.py components-normalized.json --products product.json` to validate.

5. This will print out a list of invalid BUG_COMPONENTs, if any. You can look for these
   using SearchFox. Use the path filter box to restrict the search to `moz.build`. You
   might also need to check the case-sensitive box.
