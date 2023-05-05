Goal of the project:

   Create a Python package to modify apt preferences files in line with https://manpages.debian.org/buster/apt/apt_preferences.5.en.html .


Features:
   - Parse apt preferences files into python objects list.
   - Generate new apt preference files based on the Python objects list.

Design decisions:

   If a line starts with `#` it will be ignored by the parser.
   The generator doesn't allow lines which start with `#`.

   
   If the line starts with `Explanation:` it will be represented as `str`.  
