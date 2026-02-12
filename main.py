import xmltodict
import json
import argparse
import os
import copy


def xml_file_to_dict(xml_file):
    with open(xml_file, "r", encoding="utf-8") as file:
        xml_content = file.read()
    return xmltodict.parse(xml_content)


def dict_to_xml_file(xml_dict, xml_file):
    xml_content = xmltodict.unparse(xml_dict, pretty=True)
    with open(xml_file, "w", encoding="utf-8") as file:
        file.write(xml_content)


def add_question_to_xml_dict(xml_dict, json_data):
    sample_item = xml_dict['questestinterop']['assessment']['section']['item'][0]

    # reset items
    xml_dict['questestinterop']['assessment']['section']['item'] = []
    xml_dict['questestinterop']['assessment']['@title'] = json_data['title']

    all_image_files = set()

    for i, json_item in enumerate(json_data['bank']):
        xml_item = copy.deepcopy(sample_item)

        # basic info
        # format xx: 01, 02, 03, 04, ...
        xml_item['@ident'] = str(i + 1)
        xml_item['@title'] = 'Question ' + str(i + 1).zfill(2)

        # question + image block
        material_block = {
            'mattext': {
                '@texttype': 'text/plain',
                '#text': json_item['question']
            }
        }

        # image check
        images = json_item.get("images", [])
        image_files = set()

        if images:
            html_parts = [f"{json_item['question']}"]

            for img in images:
                html_parts.append(
                    f'<p><img src="$IMS-CC-FILEBASE$/{img}" /></p>'
                )
                image_files.add(img)

            html_content = "\n".join(html_parts)

            material_block = {
                'mattext': {
                    '@texttype': 'text/html',
                    '#text': f"<![CDATA[{html_content}]]>"
                }
            }

            all_image_files.update(image_files)

        else:
            material_block = {
                'mattext': {
                    '@texttype': 'text/plain',
                    '#text': json_item['question']
                }
            }

        xml_item['presentation']['material'] = material_block
        sample_response = xml_item['presentation']['response_lid']['render_choice']['response_label'][0]

        xml_item['presentation']['response_lid']['render_choice']['response_label'] = [
            copy.deepcopy(sample_response)
            for _ in range(len(json_item['options']))
        ]

        for j, option in enumerate(json_item['options']):
            xml_item['presentation']['response_lid']['render_choice']['response_label'][j]['@ident'] = str(
                j)

            xml_item['presentation']['response_lid']['render_choice']['response_label'][j]['material']['mattext'] = {
                '@texttype': 'text/plain',
                '#text': option
            }

        # answer
        xml_item['resprocessing']['respcondition']['conditionvar']['varequal']['#text'] = str(
            json_item['answer'])

        xml_dict['questestinterop']['assessment']['section']['item'].append(
            xml_item)

    return xml_dict, all_image_files


def update_manifest_with_images(imsmanifest_dict, image_files):
    resource = imsmanifest_dict['manifest']['resources']['resource']

    # make sure resource['file'] is list type
    if not isinstance(resource['file'], list):
        resource['file'] = [resource['file']]

    existing_files = {f['@href'] for f in resource['file']}

    for image in image_files:
        if image not in existing_files:
            resource['file'].append({'@href': image})

    return imsmanifest_dict


def copy_images(image_files, source_folder, output_folder):
    for image in image_files:
        src_path = os.path.join(source_folder, image)
        dst_path = os.path.join(output_folder, image)

        if not os.path.exists(src_path):
            print(f"[WARNING] Image not found: {src_path}")
            continue

        if not os.path.exists(dst_path):
            import shutil
            shutil.copy2(src_path, dst_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Convert JSON file to QTI XML package')

    parser.add_argument('--sample_folder', type=str,
                        default='xml-sample/sample-image', help='Folder containing sample files')
    parser.add_argument('--json_file', type=str,
                        default='json-sample/sample_image_question.json', help='JSON file to convert, (same folder with images)')
    parser.add_argument('--folder_save', type=str,
                        default='output', help='XML folder to save')

    args = parser.parse_args()

    print(f"Reading {args.json_file} json files . . .", end=" ")
    json_data = json.load(open(args.json_file, 'r', encoding="utf-8"))
    print("Done!")

    # load test.xml
    xml_file = os.path.join(args.sample_folder, 'test.xml')
    xml_dict = xml_file_to_dict(xml_file)

    xml_dict, image_files = add_question_to_xml_dict(xml_dict, json_data)

    os.makedirs(args.folder_save, exist_ok=True)

    # save test.xml
    xml_file_save = os.path.join(args.folder_save, 'test.xml')
    dict_to_xml_file(xml_dict, xml_file_save)

    # load & update imsmanifest.xml
    imsmanifest_file = os.path.join(args.sample_folder, 'imsmanifest.xml')
    imsmanifest_dict = xml_file_to_dict(imsmanifest_file)

    imsmanifest_dict = update_manifest_with_images(
        imsmanifest_dict, image_files)

    # save imsmanifest.xml
    imsmanifest_file_save = os.path.join(args.folder_save, 'imsmanifest.xml')
    dict_to_xml_file(imsmanifest_dict, imsmanifest_file_save)

    copy_images(image_files, os.path.dirname(args.json_file), args.folder_save)

    # zip folder
    import shutil
    shutil.make_archive(args.folder_save, 'zip', args.folder_save)

    print("QTI package generated successfully.")
