import os
import copy
import json
import shutil
import xmltodict

from validators.schema import validate_question_json
from validators.integrity import check_question_integrity

import logging
logger = logging.getLogger("qti_builder")


# XML helpers
def xml_file_to_dict(xml_file):
    logger.debug(f"Loading XML file: {xml_file}")
    with open(xml_file, "r", encoding="utf-8") as file:
        return xmltodict.parse(file.read())


def dict_to_xml_file(xml_dict, xml_file):
    logger.debug(f"Writing XML file: {xml_file}")
    xml_content = xmltodict.unparse(xml_dict, pretty=True)
    with open(xml_file, "w", encoding="utf-8") as file:
        file.write(xml_content)


# Option material builder
def build_option_material(option, all_image_files):
    text = option.get("text", "")
    images = option.get("images", [])

    logger.debug(
        f"Building option material | text length={len(text)} | images={images}")

    html_parts = [f'<div>{text}</div>']

    for img in images:
        logger.debug(f"Adding option image: {img}")
        html_parts.append(
            f'<p style="text-align:center;">'
            f'<img src="$IMS-CC-FILEBASE$/{img}" style="max-width:90%;" />'
            f'</p>'
        )
        all_image_files.add(img)

    html_content = "\n".join(html_parts)

    return {
        'material': {
            'mattext': {
                '@texttype': 'text/html',
                '#text': html_content
            }
        }
    }


# Core builder
def add_question_to_xml_dict(xml_dict, json_data):
    logger.info("Building questions into XML structure...")

    sample_item = xml_dict['questestinterop']['assessment']['section']['item'][0]

    xml_dict['questestinterop']['assessment']['section']['item'] = []
    xml_dict['questestinterop']['assessment']['@title'] = json_data['title']

    image_base_path = json_data['image_base']
    all_image_files = set()

    for i, json_item in enumerate(json_data['bank']):
        logger.debug(f"Processing question index {i}")

        # Validate [Schema + Integrity]
        validate_question_json(json_item)
        check_question_integrity(json_item, image_base_path)

        xml_item = copy.deepcopy(sample_item)

        xml_item['@ident'] = str(i + 1)
        xml_item['@title'] = f'Question {str(i + 1).zfill(2)}'

        # Question block
        images = json_item.get("images", [])
        html_parts = [json_item['question']]

        for img in images:
            logger.debug(f"Adding question image: {img}")
            html_parts.append(
                f'<p style="text-align:center;">'
                f'<img src="$IMS-CC-FILEBASE$/{img}" style="max-width:90%;" />'
                f'</p>'
            )
            all_image_files.add(img)

        html_content = "\n".join(html_parts)

        xml_item['presentation']['material'] = {
            'mattext': {
                '@texttype': 'text/html',
                '#text': html_content
            }
        }

        # Options
        sample_response = xml_item['presentation']['response_lid']['render_choice']['response_label'][0]

        xml_item['presentation']['response_lid']['render_choice']['response_label'] = [
            copy.deepcopy(sample_response)
            for _ in range(len(json_item['options']))
        ]

        for j, option in enumerate(json_item['options']):

            if isinstance(option, str):
                option = {"text": option, "images": []}

            logger.debug(f"Processing option {j} for question {i}")

            response_label = xml_item['presentation']['response_lid']['render_choice']['response_label'][j]
            response_label['@ident'] = str(j)
            response_label.update(
                build_option_material(option, all_image_files)
            )

        # Answer
        xml_item['resprocessing']['respcondition']['conditionvar']['varequal']['#text'] = str(
            json_item['answer'])

        xml_dict['questestinterop']['assessment']['section']['item'].append(
            xml_item)

    logger.info(f"Total unique images collected: {len(all_image_files)}")

    return xml_dict, all_image_files


# Manifest + Copy
def update_manifest_with_images(imsmanifest_dict, image_files):
    logger.info("Updating imsmanifest.xml with image resources...")

    resource = imsmanifest_dict['manifest']['resources']['resource']

    if not isinstance(resource['file'], list):
        resource['file'] = [resource['file']]

    existing_files = {f['@href'] for f in resource['file']}

    for image in image_files:
        if image not in existing_files:
            logger.debug(f"Adding image to manifest: {image}")
            resource['file'].append({'@href': image})

    return imsmanifest_dict


def copy_images(image_files, source_folder, output_folder):
    logger.info("Copying image files...")

    for image in image_files:
        src_path = os.path.join(source_folder, image)
        dst_path = os.path.join(output_folder, image)

        logger.debug(f"Copying {image}")

        if not os.path.exists(src_path):
            raise FileNotFoundError(f"Missing image: {src_path}")

        if not os.path.exists(dst_path):
            shutil.copy2(src_path, dst_path)


# High-level build function
def build_qti_package(sample_folder, json_file, output_folder):
    logger.info("Starting QTI package build...")

    image_base_path = os.path.dirname(json_file)

    logger.info(f"Reading JSON file: {json_file}")
    with open(json_file, "r", encoding="utf-8") as f:
        json_data = json.load(f)

    json_data['image_base'] = image_base_path

    # Load XML template
    xml_file = os.path.join(sample_folder, 'test.xml')
    xml_dict = xml_file_to_dict(xml_file)

    xml_dict, image_files = add_question_to_xml_dict(xml_dict, json_data)

    os.makedirs(output_folder, exist_ok=True)

    # Save test.xml
    dict_to_xml_file(xml_dict, os.path.join(output_folder, 'test.xml'))

    # Update manifest
    imsmanifest_file = os.path.join(sample_folder, 'imsmanifest.xml')
    imsmanifest_dict = xml_file_to_dict(imsmanifest_file)

    imsmanifest_dict = update_manifest_with_images(
        imsmanifest_dict, image_files)

    dict_to_xml_file(
        imsmanifest_dict,
        os.path.join(output_folder, 'imsmanifest.xml')
    )

    copy_images(image_files, image_base_path, output_folder)

    shutil.make_archive(output_folder, 'zip', output_folder)

    logger.info("QTI package build completed successfully.")
