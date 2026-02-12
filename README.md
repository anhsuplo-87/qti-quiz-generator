# QTI Quiz Generator

A lightweight tool for converting structured JSON question banks into QTI-compliant XML packages (.zip) for LMS platforms.

## Project Team

- Starter: Du Pham Tien (ptdu@vnu.edu.vn)
- Maintainer: Ba Luong (bals@vnu.edu.vn)

## Overview

QTI Quiz Generator transforms a validated JSON question bank into:

- `test.xml`
- `imsmanifest.xml`
- Image assets
- Packaged `.zip` file (QTI import-ready)

The project focuses on:

- Schema validation
- Data integrity validation
- Image handling
- Clean modular architecture
- CLI-based workflow

## Features

### Question Support

- Multiple choice questions
- Text-based questions
- Image support for:
  - Questions
  - Answer options
- Multiple images per question
- Mixed text + image answers

### Validation Layer

- JSON Schema validation
- Integrity validation (image existence, structure checks)

### CLI Features

- Custom input JSON
- Custom output folder
- Verbose logging
- Debug mode

### Migration Tool

- Convert old JSON format (v0.2) → new format (v0.3+)
- Backward compatibility support

## Project Structure

```bash
src/
│
├── core/           # QTI building logic
├── validators/     # Schema + integrity validation
├── utils/          # Helper functions
├── convert.py      # JSON migration tool
└── cli.py          # Entry point (CLI)
```

## Version History

### Version 0.0 — Foundation

Initial prototype developed by **Du Pham Tien**.  
This version laid the groundwork for the JSON → QTI conversion concept.

- Core idea and initial implementation
- Basic JSON → QTI XML transformation
- Early structural design

Original repository (starter version): [QTI Convert](https://github.com/dupham2206/qti_convert)

> This version is acknowledged as the foundational work of the project.

### Version 0.1 - Starter Release

- Basic full-text question
- Support `multiple_choice_question`

### Project Maintenance & Development

Starting from **Version 0.2**, the project has been actively maintained and expanded by **Ba Luong**, focusing on:

- Extending feature support
- Improving architecture and modularity
- Adding validation layers
- Enhancing CLI usability
- Improving long-term maintainability and extensibility

### Version 0.2:

- Add image support for question
- Support maximum 1 image per question

### Version 0.3:

- Change `image` → `images`
- Add image support for answer options
- Support multiple images per question
- Support text + image per answer
- Provide convert tool (`option_cvt.py`)

### Version 0.4:

- Refactor into `core`, `utils`, `validators`
- Add JSON Schema validation
- Add integrity validation
- Rename `main.py` → `cli.py`
- Add `--verbose` logging
- Support `INFO` and `DEBUG` logging levels
- Upgrade convert tool → `convert.py`

## Environment Setup

```bash
pip install -r requirements.txt
```

## Usage

### Run with default sample

```bash
python src/cli.py
```

### Run with custom JSON

```bash
python src/cli.py \
    --json_file "YOUR_PATH_TO_JSON_FILE" \
    --output_folder "OUTPUT_FOLDER_NAME"
```

### Optional flags

```bash
--verbose
```

Enable debug-level logging.

### Convert Old JSON Format

Convert JSON from v0.2 → v0.3+ schema:

```bash
python src/convert.py -i old.json -o new.json
```

Or overwrite original:

```bash
python src/convert.py -i old.json --inplace
```

## JSON Structure & Folder Layout

### Recommended Folder Structure

To ensure correct image validation and QTI packaging, your question bank should follow this structure:

```bash
question_bank/
│
├── sample_question.json
├── image1.png
├── diagram_a.jpg
└── option_b.png
```

Or a cleaner structure:

```bash
question_bank/
│
├── sample_question.json
└── images/
    ├── image1.png
    ├── diagram_a.jpg
    └── option_b.png
```

> All image paths in JSON must be **relative to the JSON file location.**

If using subfolder:

```json
"images": ["images/image1.png"]
```

### JSON Schema (Current Version ≥ 0.3)

Each question inside `"bank"` must follow this format:

```json
{
  "question": "<p>What is 2 + 2?</p>",
  "images": ["example.png"],
  "options": [
    {
      "text": "3",
      "images": []
    },
    {
      "text": "4",
      "images": []
    }
  ],
  "answer": 1
}
```

#### Notes

- `question` supports **HTML content** (e.g., `<p>`, `<b>`, `<sub>`, `<sup>`, etc.).
- `options.text` is typically **plain text**.
- `images` must be a list (use `[]` if no images).
- `answer` is the index of the correct option (starting from 0).

#### Simple Rules

1. Keep image paths relative to the JSON file.
2. Make sure all referenced images exist.
3. `options` must not be empty.
4. `answer` must match a valid option index.

## AI Usage & Ethics Statement

This project may leverage AI tools (e.g., large language models) during development for:

- Code suggestions
- Refactoring guidance
- Documentation drafting
- Test case generation

However:

1. All AI-generated code is reviewed and validated manually.
2. AI outputs are treated as assistive suggestions — not authoritative sources.
3. Developers remain responsible for:
   - Code correctness
   - Security validation
   - Academic integrity
   - Compliance with institutional policies
4. No proprietary student data or sensitive information is submitted to AI systems.

We are committed to:

- Transparency in AI-assisted development
- Responsible usage
- Academic integrity
- Avoiding over-reliance on automated code generation
