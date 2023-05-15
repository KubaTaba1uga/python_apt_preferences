Goal of the project:

   Create a Python package to modify apt preferences files in line with https://manpages.debian.org/buster/apt/apt_preferences.5.en.html.


Features:
   - Parse apt preferences' files into Python objects list.
   - Generate new apt preferences' files based on Python objects list.

Planned-features:
   - Support multiple pins in single preference.

Design decisions:

   If a line starts with `#` it will be ignored by the parser.
   The generator doesn't allow creating lines starting with `#`.
