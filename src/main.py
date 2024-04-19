from generation.chargen import generate_image


if __name__ == '__main__':
    character = {'race': 'dwarf', 'dnd_class': 'wizard', 'background': 'tavern'}
    generate_image(character)
