import os


def check_question_integrity(question: dict, image_base_path: str):
    """
    image_base_path = folder contain images
    """

    options = question["options"]
    answer = question["answer"]

    # normalize options
    normalized_options = []
    for opt in options:
        if isinstance(opt, str):
            normalized_options.append({"text": opt, "images": []})
        else:
            normalized_options.append({
                "text": opt.get("text", ""),
                "images": opt.get("images", [])
            })

    # check answer validity
    if isinstance(answer, int):
        if answer < 0 or answer >= len(normalized_options):
            raise ValueError(
                f"Answer index {answer} out of range (0-{len(normalized_options)-1})"
            )

    elif isinstance(answer, str):
        try:
            answer_index = int(answer)
        except:
            raise ValueError("Answer must be integer index or numeric string.")

        if answer_index < 0 or answer_index >= len(normalized_options):
            raise ValueError(
                f"Answer index {answer} out of range (0-{len(normalized_options)-1})"
            )
    else:
        raise ValueError("Answer must be int or numeric string.")

    # collect all images
    all_images = set()

    # question images
    for img in question.get("images", []):
        all_images.add(img)

    # option images
    for opt in normalized_options:
        for img in opt.get("images", []):
            all_images.add(img)

    # check file existence
    for img in all_images:
        img_path = os.path.join(image_base_path, img)

        if not os.path.isfile(img_path):
            raise ValueError(
                f"Image file not found: {img} (expected at {img_path})"
            )
