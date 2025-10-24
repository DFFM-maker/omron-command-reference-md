import traceback

# Other import statements and code...

def convert(langs=None):
    # Existing functionality

    # Original line: langs=["Italian", "English"]
    # Updated line to auto-detect:
    langs = langs

    # Existing code...

try:
    # Main execution block
except Exception as e:
    print(f'An error occurred: {e}')
    # Adding traceback to show full error details
    traceback.print_exc()