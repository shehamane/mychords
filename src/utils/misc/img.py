from PIL import Image

from data.structure_config import IMG_DIR_PATH, IMG_FORMAT


async def concat_images(pathes):
    images = [Image.open(x) for x in pathes]
    widths, heights = zip(*(i.size for i in images))

    total_width = sum(widths)
    max_height = max(heights)

    new_im = Image.new('RGB', (total_width, max_height), (255, 255, 255))

    x_offset = 0
    for im in images:
        _, height = im.size
        height_delta = (max_height - height) // 2
        new_im.paste(im, (x_offset, height_delta))
        x_offset += im.size[0]

    path = IMG_DIR_PATH + 'tmp' + IMG_FORMAT
    new_im.save(path)
    return path
