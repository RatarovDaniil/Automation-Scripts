from lxml import etree
import os
from PIL import Image

def parse_labels(path_to_file):
    with open(path_to_file) as fobj:
        xml = fobj.read()
    root = etree.fromstring(xml)
    boxes = []
    for elem in root.getchildren():
        if elem.tag == "object":
            for object_field in elem.getchildren():
                if object_field.tag == "bndbox":
                    box = {}
                    for bnbbox_elem in object_field:
                        box[bnbbox_elem.tag] = bnbbox_elem.text
                    boxes.append(box)
    new_boxes = []
    for box in boxes:
        new_box = []
        new_box.append(int(box["xmin"]))
        new_box.append(int(box["ymin"]))
        new_box.append(int(box["xmax"]))
        new_box.append(int(box["ymax"]))
        new_boxes.append(new_box)

    return new_boxes

def crop_images(file_path, boxes):
    img = Image.open(file_path)
    cropped_imgs = []
    for box in boxes:
        #xmin, xmax, ymin, ymax
        cropped_imgs.append(img.crop(box))

    return cropped_imgs

def main(PATH_TO_LABELES, PATH_TO_SAVE, extension):
    for file in os.listdir(PATH_TO_LABELES):
        if file.endswith(".xml"):
            file_path = os.path.join(PATH_TO_LABELES, file)
            boxes = parse_labels(os.path.join(PATH_TO_LABELES, file))
            file_path = os.path.join(os.path.dirname(file_path), os.path.splitext(os.path.basename(file))[0] + "." + extension)
            images = crop_images(file_path, boxes)
            cnt = 0
            for img in images:
                img_path = os.path.join(PATH_TO_SAVE, os.path.splitext(os.path.basename(file))[0] + "_cropped_" + str(cnt) + "." + extension)
                img.save(img_path)
                cnt += 1

if __name__ == "__main__":
    #main()
    pass
