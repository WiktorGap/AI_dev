import requests
import os
from PIL import Image , UnidentifiedImageError
import io
from pathlib import Path
from fastai.vision.all import * 
import matplotlib.pyplot as plt

 


access_key = "YOUR API KEY FROM UNSPLASH"
current_path = os.getcwd()
catalogName = "harrypotter"
max_img = 50
term = "harry potter"

def search_images(term, max_images=max_img):
    print(f"Searching for '{term}' on Unsplash")
    image_urls = []
    per_page = 30
    pages_needed = (max_images // per_page) + 1

    for page in range(1, pages_needed + 1):
        url = f"https://api.unsplash.com/search/photos?query={term}&per_page={per_page}&page={page}&client_id={access_key}"
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Error: {response.status_code}, {response.text}")
            break
        results = response.json()
        for item in results.get("results", []):
            image_urls.append(item["urls"]["regular"])
            if len(image_urls) >= max_images:
                break
        if len(image_urls) >= max_images:
            break

    return (image_urls)



def getDir():
    DOWNLOAD_DIR = os.path.join(current_path, "characters", catalogName)
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    return DOWNLOAD_DIR


def download_images(keyword, folder_path, max_images=10):
    urls = search_images(keyword, max_images)
    os.makedirs(folder_path, exist_ok=True)
    for i, url in enumerate(urls):
        image_filename = f"{keyword}_{i + 1}.jpg"
        image_path = os.path.join(folder_path, image_filename)
        try:
            img_data = requests.get(url).content
            img = Image.open(io.BytesIO(img_data))
            img.verify()
            with open(image_path, "wb") as f:
                f.write(img_data)
            print(f"Downloaded: {image_filename}")
        except Exception as e:
            print(f"Error downloading {image_filename}: {e}")



pathsOfPhotos = []

def getPhotosPaths():
    for entry in os.listdir(downladDir):
        if os.path.isfile(os.path.join(downladDir, entry)) and entry.endswith(('.jpg', '.png')):
            pathsOfPhotos.append(os.path.join(downladDir, entry))
    return pathsOfPhotos

downladDir = getDir()
#download_images(term, folder_path=downladDir, max_images=max_img)
photosPahts = getPhotosPaths()
#print(photosPahts)



def fix_image_modes(folder_path='characters'):

    folder = Path(folder_path)
    count_fixed = 0
    for image_path in folder.rglob('*.[jp][pn]g'):  
        try:
            img = Image.open(image_path)
            if img.mode in ['P', 'RGBA']:
                img = img.convert('RGB')
                img.save(image_path)
                print(f"Converted: {image_path}")
                count_fixed += 1
        except UnidentifiedImageError:
            print(f"Unidentified image (skipped): {image_path}")
        except Exception as e:
            print(f"Error fixing {image_path}: {e}")

    print(f" Finished conversion. Total images fixed: {count_fixed}")


fix_image_modes()



if __name__=='__main__':
    path = Path('characters')

    print(f"Checking folder structure in {path}")
    for cat_folder in path.iterdir():
        if cat_folder.is_dir():
            imgs = list(cat_folder.glob('*.jpg')) + list(cat_folder.glob('*.png'))
            print(f"Category '{cat_folder.name}' has {len(imgs)} images")

    hero = DataBlock(
        blocks=(ImageBlock, CategoryBlock),
        get_items=get_image_files,
        splitter=RandomSplitter(valid_pct=0.2, seed=42),
        get_y=parent_label,
        item_tfms=Resize(128)
    )

    dls = hero.dataloaders(path)

    print(f"Train items: {len(dls.train_ds)}")
    print(f"Valid items: {len(dls.valid_ds)}")



    #hero = hero.new(item_tfms=Resize(128,ResizeMethod.Squish))
    #hero = hero.new(item_tfms=Resize(128,ResizeMethod.Pad,pad_mode='zeros'))
    #hero = hero.new(item_tfms=RandomResizedCrop(128,min_scale=0.3))
    #hero=hero.new(item_tfms=Resize(128),batch_tfms=aug_transforms(mult=2))
    hero = hero.new(item_tfms=RandomResizedCrop(224,min_scale=0.5),batch_tfms=aug_transforms())
    dls = hero.dataloaders(path)
    # dls.show_batch(max_n=15, nrows=3,unique=True)
    # plt.show()

    learn = vision_learner(dls,resnet18,metrics=error_rate)
    learn.fine_tune(6)
    

    interp = ClassificationInterpretation.from_learner(learn)
    interp.plot_confusion_matrix()
    plt.show()
    interp.plot_top_losses(5,nrows=1)
    plt.show()


    learn.export('character_rec_model_test.pkl')


