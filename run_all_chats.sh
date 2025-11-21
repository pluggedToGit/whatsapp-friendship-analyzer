#!/bin/bash

# Process each chat file individually
for file in data/raw/*.txt; do
    echo "Processing $file..."
    /Users/gautamramesh/Documents/projects/Learning/whatsapp-friendship-analyzer/.venv/bin/python -c "
import sys
from pathlib import Path
sys.path.append(str(Path('src')))
from parsers.whatsapp_parser import WhatsAppParser

parser = WhatsAppParser()
data = parser.parse_file('$file')
print(f'Parsed {len(data.get(\"messages\", []))} messages from $file')
"
done
