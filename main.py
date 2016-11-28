from PIL import Image
import shutil
import os
from myutil import open_json, make_sure_path_exists, copy_folder, resize, resize_folder
from mosaic import mosaic

# reads herodata.json and pulls hero and ability images from source folder to local folders
def get_source_images(src, images_path, tiles_path):
    make_sure_path_exists(tiles_path)
    make_sure_path_exists(images_path)

    # get names of all heroes and their abilities
    herodata = open_json('herodata.json')
    heroes = []
    abilities = []
    for h in herodata.keys():
        if h == 'npc_dota_hero_zuus':
            heroes.append('zuus_alt1')
        else:        
            heroes.append(h.replace('npc_dota_hero_', ''))
        for a in herodata[h]['abilities']:
            if a['name'] == 'morphling_morph':
                abilities.append('morphling_morph_agi')
                abilities.append('morphling_morph_str')
                continue
            elif a['name'] in ['tusk_launch_snowball', 'attribute_bonus']:
                continue
            abilities.append(a['name'])

    abilities = list(set(abilities))
    heroes = list(set(heroes))

    # copy hero and ability images
    for a in abilities:
        src_path = os.path.join(src, tiles_path, a + '.png')
        out_file = os.path.join(tiles_path, a + '.png')
        shutil.copy2(src_path, out_file)

    for a in heroes:
        src_path = os.path.join(src, 'heroes', a + '.png')
        shutil.copy2(src_path, os.path.join('heroes', a + '.png'))

def generate_mosaics(images_path, dst, tiles_path, tile_width, tile_height):
    make_sure_path_exists(dst)
    files = [x.replace('.png', '') for x in os.listdir(images_path)]

    for f in files:
        img_path = os.path.join(images_path, f + ".png")
        print f
        out_file = os.path.join(dst, f + ".png")
        mosaic(img_path, out_file, tiles_path, tile_width, tile_height)

def main():
    src = 'path/to/source/images'
    source_tiles_path = 'spellicons' #copied source tiles folder
    tiles_path = 'spellicons64x64' #resized tiles folder
    images_path = 'heroes' #copied source image folder to mosaic process
    tile_width = 64
    tile_height = 64
    dst = 'out' #mosaic output folder
    
    #get_source_images(src, images_path, source_tiles_path)
    
    # resize copied source tiles to the desired tile size
    resize_folder(source_tiles_path, tiles_path, (tile_width, tile_height))
    
    generate_mosaics(images_path, dst, tiles_path, tile_width, tile_height)

    #postprocess mosaic output
    #resize_folder(dst, 'out1920x1080/', (1920, 1080))
    
if __name__ == "__main__":
    main()