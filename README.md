# Apt Preferences

## Description

Python package to modify apt preferences files in line with https://manpages.debian.org/buster/apt/apt_preferences.5.en.html.

I don't like using awk and sed for updating preferences cause it's got messier the bigger amount of preferences is connected to a package.
If regexes are used in packages names then it's even harder. This package along with re should make more complex preferences scenarios easy to automate. 

And i wanted to learn LARK so that is also a big pron of the project.

## Table of Contents (Optional)

If your README is long, add a table of contents to make it easy for users to find what they need.

- [Installation](#installation)
- [Usage](#usage)
- [Credits](#credits)
- [License](#license)

## Installation

Create virtual environment
```
make venv
```

Activate virtual environment
```
. .venv/bin/activate
```

Install package
```
make install
```

## Usage

Provide instructions and examples for use. Include screenshots as needed.

To add a screenshot, create an `assets/images` folder in your repository and upload your screenshot to it. Then, using the relative filepath, add it to your README using the following syntax:

    ```md
    ![alt text](assets/images/screenshot.png)
    ```

## Credits

List your collaborators, if any, with links to their GitHub profiles.

If you used any third-party assets that require attribution, list the creators with links to their primary web presence in this section.

If you followed tutorials, include links to those here as well.

## License

The last section of a high-quality README file is the license. This lets other developers know what they can and cannot do with your project. If you need help choosing a license, refer to [https://choosealicense.com/](https://choosealicense.com/).

---

🏆 The previous sections are the bare minimum, and your project will ultimately determine the content of this document. You might also want to consider adding the following sections.

## Badges

![badmath](https://img.shields.io/github/languages/top/lernantino/badmath)

Badges aren't necessary, per se, but they demonstrate street cred. Badges let other developers know that you know what you're doing. Check out the badges hosted by [shields.io](https://shields.io/). You may not understand what they all represent now, but you will in time.

## Features

If your project has a lot of features, list them here.

## How to Contribute

If you created an application or package and would like other developers to contribute it, you can include guidelines for how to do so. The [Contributor Covenant](https://www.contributor-covenant.org/) is an industry standard, but you can always write your own if you'd prefer.

## Tests

Go the extra mile and write tests for your application. Then provide examples on how to run them here.
   
   
   
   Goal of the project:

   


Features:
   - Parse apt preferences' files into Python objects list.
   - Generate new apt preferences' files based on Python objects list.

Planned-features:
   - Support multiple pins in single preference.

Design decisions:

   If a line starts with `#` it will be ignored by the parser.
   The generator doesn't allow creating lines starting with `#`.
