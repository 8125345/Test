from argparse import ArgumentParser


parser = ArgumentParser()
parser.add_argument('img', help='Image file', default='1')
parser.add_argument('-ima', help='Image file', default='2')
parser.add_argument('--images', help='Image file', default='3')


args = parser.parse_args()
print(args.img)
print(args.ima)
print(args.images)
