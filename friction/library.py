from random import choice
from tempfile import mkdtemp
import re
import os
from urllib.parse import urlencode
from zipfile import ZipFile

from PIL import Image
from rarfile import RarFile


def extract_zip(source, dest):
    ZipFile(source).extractall(dest)


def extract_rar(source, dest):
    RarFile(source).extractall(dest)


IMAGE_EXTS = ['.png', '.jpeg', '.jpg']
ARCHIVE_EXTS = {
    '.rar': extract_rar,
    '.zip': extract_zip,
}


class Library:
    def __init__(self, root):
        self.doujin_cache = {}
        self._choices_list = None
        self.choices = set()

        self.root = root
        print('scanning {}...'.format(self.root))
        self.scan_dir(self.root)

        if not self.choices:
            raise RuntimeError(
                'do you even have anything here? im looking for zips and rars '
                'and jaypegs and pings'
            )

        print('i found {} things!'.format(len(self.choices)))

    def add_choice(self, path):
        self.choices.add(
            re.sub(r'^{}/'.format(re.escape(self.root)), '', path)
        )

    def scan_dir(self, path):
        for entry in os.scandir(path):
            if entry.is_dir():
                self.scan_dir(entry.path)
                continue

            name, ext = os.path.splitext(entry.name)

            if ext in IMAGE_EXTS:
                self.add_choice(path)
                break

            if ext in ARCHIVE_EXTS:
                self.add_choice(entry.path)
                pass

    def doujin_for(self, path):
        if path not in self.choices:
            raise RuntimeError('sneaky')

        doujin = self.doujin_cache.get(path)

        if doujin is not None:
            return doujin

        print('reading {}'.format(path))
        full_path = os.path.join(self.root, path)
        if os.path.isdir(full_path):
            doujin = Doujin(path, full_path)
        else:
            ext = os.path.splitext(path)[1]
            target = mkdtemp()
            ARCHIVE_EXTS[ext](full_path, target)
            doujin = Doujin(path, target, recursive=True)

        self.doujin_cache[path] = doujin

        return doujin

    def choice(self, f=None):
        if self._choices_list is None:
            self._choices_list = list(self.choices)

        if f is not None:
            choices_list = [i for i in self._choices_list
                            if f.lower() in i.lower()]
            count = len(choices_list)
            if count == 0:
                return
            print('filtered to {} things'.format(count))
        else:
            choices_list = self._choices_list

        return self.doujin_for(choice(choices_list))


class Doujin:
    def scan_dir(self, path, recursive):
        for f in os.scandir(path):
            if os.path.splitext(f.name)[1] in IMAGE_EXTS:
                self.pages.append(f.path)
            elif recursive and f.is_dir():
                self.scan_dir(f.path, recursive)

    def __init__(self, path, full_path, recursive=False):
        self.path = path
        self.full_path = full_path
        self.pages = []
        self.scan_dir(full_path, recursive)
        self.photoswipe_items = []

        for i, page in enumerate(self.pages):
            with Image.open(page) as pil:
                self.photoswipe_items.append({
                    'src': '/item?{}'.format(urlencode({
                        'path': self.path,
                        'page': i,
                    })),
                    'w': pil.width,
                    'h': pil.height,
                })

    def json(self):
        return {
            'title': os.path.basename(self.path),
            'photoswipe': self.photoswipe_items,
        }
