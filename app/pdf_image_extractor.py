import minecart

THRESHOLD = 100


def extract_images(file):
    lists = []
    pdf_file = open(file, 'rb')
    doc = minecart.Document(pdf_file)
    print(doc.iter_pages())
    for index, page in enumerate(doc.iter_pages()):
        try:
            for image in page.images:
                im = image.as_pil()
                if im.width > THRESHOLD and im.height > THRESHOLD:
                    lists.append(im)
        except:
            pass
    return lists
