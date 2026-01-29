# OFX Viewer

A Python tool to view and print OFX (Open Financial Exchange) files from banks.

## Features

- Parse OFX files from various banks
- View detailed transaction information
- Print summary reports suitable for printing
- Command-line interface for easy usage

## Installation

1. Clone this repository:
```bash
git clone https://github.com/NeloReis/ofx_viwer.git
cd ofx_viwer
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

View OFX file contents (default behavior):
```bash
python ofx_viewer.py statement.ofx
```

### View Detailed Information

Display detailed transaction information:
```bash
python ofx_viewer.py statement.ofx --view
```

### Print Summary

Generate a printable summary:
```bash
python ofx_viewer.py statement.ofx --print
```

### Both View and Print

Display detailed information and print summary:
```bash
python ofx_viewer.py statement.ofx --view --print
```

## Sample File

A sample OFX file (`sample_statement.ofx`) is included in the repository for testing purposes.

Try it out:
```bash
python ofx_viewer.py sample_statement.ofx
```

## Command-Line Options

- `ofx_file` - Path to the OFX file (required)
- `-v, --view` - View detailed OFX file contents
- `-p, --print` - Print summary suitable for printing
- `-h, --help` - Show help message

## Requirements

- Python 3.6 or higher
- ofxparse library (installed via requirements.txt)

## License

MIT License - see LICENSE file for details
