# friction

a tool for viewing items from your massive collection of pornographic manga at
random

## prerequisites

- python 3.5 or newer (`os.scandir` is just too good)
- unrar, which is probably available from your package manager as `unrar`
- libjpeg and zlib (so that we can run [PIL][pil] and determine image
  resolutions)
- a directory full of porn manga (more details in 'caveats' below)

[pil]: http://pillow.readthedocs.io/en/3.0.x/installation.html

## setup

```
pip3 install friction
```

or, to upgrade from an older version:

```
pip3 install -U friction
```

## use

```
cd '~/Desktop/vegetable taxes'  # or wherever your porn is
friction
```

then open <http://localhost:5000/> in your browser of choice

for quick navigation between pages, you can swipe if you're on a touchscreen
device, or you can use your arrow keys

when you want something new, hit enter or the little x in the corner or reload
the page or scroll, and it'll pick another thing for you

if you have something in particular in mind, press o or tap/click at the bottom
left of the screen and you'll get a menu with a field you can type into to
filter what the choices are being made from. the filtering is pretty stupid, it
just checks to see if your query is present in the file's path. it's case
insensitive. on a computer with a keyboard, the intended workflow to change
your filter is to hit o, type something, and hit enter

the form that the filter field lives in also has rotation options, for if
you're using a computer with an inappropriate aspect ratio or you're lying down
or whatever

## caveats

### library format

your library can be structured and nested however you like, but friction has a
particular idea of what counts as a single manga, inspired by what i've
encountered in batches of scans i've seen

basically, one manga is either a flat directory containing images or a
zip/rar/cbz/cbr archive containing images in any structure

this precludes, for instance, archives that contain other archives, as i've not
seen anyone distributing scans in such a format with any regularity

if you have a library that's formatted differently and would like friction to
support it, please let me know

### fullscreen

friction doesn't use photoswipe's built-in fullscreen support, primarily
because it'd break every time you reloaded the page, and that'd be awful

your browser probably has an option to go fullscreen and hide the UI
completely; i know at least that desktop chrome and safari do

### listening and security

by default, friction listens at 127.0.0.1:5000, but you can change that with
the FH and FP environment variables, for example:

```
FH=0.0.0.0 FP=8009 friction
```

this will be necessary if, for instance, you're wanting to use a phone or
tablet or just a computer other than the one your library is on

you _could_ mount the library on your local machine and then run friction
locally, but it's pretty I/O heavy, so network storage is a huge bottleneck and
it's gonna be dog slow if you do

while there's no particular reason i can think of that'd make this dangerous,
i'd advise caution if you intend to host friction to untrusted third parties,
for instance on the public web. i've made effort to protect against access to
files that aren't in the library, but making this thing safe from attackers is
not my priority, so i offer no guarantees

it'd also be pretty easy to DOS your server if you have a large library of
archives, since friction extracts archived manga to a temporary directory and
only removes them when you quit, so you could very well run out of space if
someone continually reloads for a while

## thanks to

- [flask](http://flask.pocoo.org)
- [photoswipe](http://photoswipe.com)
