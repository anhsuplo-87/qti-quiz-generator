# QTI Quiz Generator

From json input to QTI (xml) output folder (.zip file).

- Starter: Du Pham Tien (ptdu@vnu.edu.vn)
- Maintainer: Ba Luong (bals@vnu.edu.vn)

## Change logs

Version 0.1:

- Simple full text question
- Support `multiple_choice_question` type

Version 0.2:

- Adding image for question (`sample-image`)
- Support maximum 1 image per question

Version 0.3:

- Change "image" to "images"
- Adding image for answer
- Support multiple images per question
- Support both text and image per answer
- Provide convert tool `option_cvt.py` (convert json from v0.2 -> v0.3+)

## Environment Setup

```
pip install -r requirements.txt
```

## Default sample_question.json

```
python main.py
```

## Run with your json question file

```
python main.py --json_file "YOUR_PATH_TO_JSON_QUESTION_FILE" --folder_save "YOUR_SAVE_FOLDER_NAME_AND_ZIP"
```

## Convert json v0.2 -> v0.3+

```
python option_cvt.py
```
