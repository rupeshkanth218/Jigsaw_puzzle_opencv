from PIL import Image
def jigsaw_creator(img, row, col):
    # row -- how many cuts to make row wise
    # col -- how many cuts to make column wise
    w = img.width // col
    h = img.height // row
    x1, y1, x2, y2 = 0, 0, w, h
    size = 100
    count = 1
    for j in range(row):
        for i in range(col):
            img2 = img.crop(box=(x1 + (i * size), y1 + (j * size), x2 + (i * size), y2 + (j * size)))
            img2.save("pieces/img{}.png".format(count))
            count += 1

main_img = Image.open("elephant_resized.png")
jigsaw_creator(main_img, 2,2)
