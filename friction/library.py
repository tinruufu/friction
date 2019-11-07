from hashlib import md5
import os
from random import choice
import re
from shutil import rmtree
from tempfile import mkdtemp
from urllib.parse import urlencode
from zipfile import ZipFile, BadZipFile

from PIL import Image
from rarfile import RarFile, NotRarFile, RarUnknownError

try:
    from magic import from_file
except ImportError as e:
    magic_imported = False
else:
    magic_imported = True


def extract_zip(source, dest):
    ZipFile(source).extractall(dest)


def extract_rar(source, dest):
    rf = RarFile(source)
    try:
        rf.extractall(dest)
    except RarUnknownError as e:
        raise RuntimeError(
            'got an error while extracting {f}:\n\n{error}\n\n'
            'you may need to install `unrar` with your favourite package '
            'manager'.format(f=source, error=e)
        )


RAR = 'application/x-rar'
ZIP = 'application/zip'

IMAGE_EXTS = ['.png', '.jpeg', '.jpg']
ARCHIVE_EXTS = {
    '.rar': RAR,
    '.cbr': RAR,
    '.zip': ZIP,
    '.cbz': ZIP,
}

ARCHIVE_HANDLERS = {
    RAR: extract_rar,
    ZIP: extract_zip,
}


class FrictionError(Exception):
    def __init__(self, message, status=400):
        super().__init__()
        self.status_code = status
        self.message = message


class Library:
    def __init__(self, root):
        self.doujin_cache = {}
        self._choices_list = None
        self.choices = {}
        self.cached_extractions = set()

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
        relpath = re.sub(r'^{}/'.format(re.escape(self.root)), '', path)
        self.choices[md5(relpath.encode()).hexdigest()] = relpath

    def scan_dir(self, path):
        for entry in os.scandir(path):
            if entry.name.startswith('.'):
                continue

            if entry.is_dir():
                self.scan_dir(entry.path)
                continue

            name, ext = os.path.splitext(entry.name)

            if ext.lower() in IMAGE_EXTS:
                self.add_choice(path)
                break

            if ext.lower() in ARCHIVE_EXTS:
                self.add_choice(entry.path)

    def doujin_for(self, identifier):
        path = self.choices.get(identifier)

        if path is None:
            raise FrictionError('nothing by that identifier, sorry')

        doujin = self.doujin_cache.get(path)

        if doujin is not None:
            return doujin

        print('reading {}'.format(path))
        full_path = os.path.join(self.root, path)
        if os.path.isdir(full_path):
            doujin = Doujin(path, full_path, identifier)
        else:
            target = mkdtemp()
            self.cached_extractions.add(target)

            if magic_imported:
                mime = from_file(full_path, mime=True)
                if mime not in ARCHIVE_HANDLERS:
                    raise FrictionError(
                        '<code>{}</code> is not an archive we support'
                        '<br/><br/>magic thinks it looks like <code>{}</code>'
                        .format(path, mime)
                    )
            else:
                mime = ARCHIVE_EXTS[os.path.splitext(path)[1]]

            try:
                ARCHIVE_HANDLERS[mime](full_path, target)
            except (NotRarFile, BadZipFile):
                raise FrictionError(
                    '<code>{}</code> was not in format we expected{}'.format(
                        path, '' if magic_imported else
                        '<br/><br/>install libmagic if you keep running into '
                        'this, see the readme for details'
                    )
                )
            doujin = Doujin(path, target, identifier, recursive=True)

        self.doujin_cache[path] = doujin

        return doujin

    def choice(self, f=None):
        if self._choices_list is None:
            self._choices_list = list(self.choices.items())

        if f:
            choices_list = [i for i in self._choices_list
                            if f.lower() in i[1].lower()]
            count = len(choices_list)
            if count == 0:
                return
            print('filtered to {} things'.format(count))
        else:
            choices_list = self._choices_list

        return self.doujin_for(choice(choices_list)[0])

    def delete_caches(self):
        if self.cached_extractions:
            print('\rdeleting cached archive extractions, hang on a sec...')
            for dirname in self.cached_extractions:
                rmtree(dirname)
            self.cached_extractions = set()


class Doujin:
    def scan_dir(self, path, recursive):
        for f in sorted(os.scandir(path), key=lambda di: di.path):
            if (
                (os.path.splitext(f.name)[1].lower() in IMAGE_EXTS) and
                (not f.name.startswith('.'))
            ):
                self.pages.append(f.path)
            elif recursive and f.is_dir():
                self.scan_dir(f.path, recursive)

    def __init__(self, path, full_path, identifier, recursive=False):
        self.identifier = identifier
        self.path = path
        self.full_path = full_path
        self.pages = []
        self.scan_dir(full_path, recursive)
        if not self.pages:
            raise FrictionError('there are no images in <code>{}</code>'
                                .format(path))
        self.photoswipe_items = []

        for i, page in enumerate(self.pages):
            with Image.open(page) as pil:
                self.photoswipe_items.append({
                    'src': '/item?{}'.format(urlencode({
                        'identifier': self.identifier,
                        'page': i,
                    })),
                    'w': pil.width,
                    'h': pil.height,
                })

    def json(self):
        return {
            'id': self.identifier,
            'title': os.path.basename(self.path),
            'photoswipe': self.photoswipe_items,
        }
