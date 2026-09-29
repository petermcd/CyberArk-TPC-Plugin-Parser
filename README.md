# CyberArk TPC Plugin Parser

CyberArk TPC Plugin Parser is a package intended to make it easy to work with CyberArk process
and platform ini files.

The lexer and parser breaks down the files to their constituent parts so that they can be
further processed by other applications.

## Installation

CyberArk TPC Plugin Parser can be installed using Pip:

```bash
pip install cyberark-tpc-plugin-parser
```

## Usage

The main point of entry is the parser, this takes the content of the process and prompts
files as arguments:

```python
from tpc_plugin_parser.parser import Parser

with open("/path/to/files/process.ini") as process_fh:
    process_content: str = process_fh.read()

with open("/path/to/files/prompts.ini") as prompts_fh:
    prompts_content: str = prompts_fh.read()

process_parser = Parser(file_contents=process_content)
process_file_tokens = process_parser.parsed_file

prompts_parser = Parser(file_contents=prompts_content)
prompt_file_tokens = prompts_parser.parsed_file
```
