Chongqing Mini Guide
====================

The website is the single file index.html, plus optional local photos.
Upload index.html and apple-touch-icon.png to the root of your GitHub Pages repository.
The 7 routes, metro names and explanations are all built into index.html.

Photos: For now, small photo previews are loaded from linked external sites,
only as you scroll into an expanded route. The local photo files have not
been bundled because downloading remote image binaries was unavailable in
the authoring environment. You can leave things as they are; the page still
works online. To generate local files next to index.html on a computer with
normal web access:

  python3 -m pip install requests pillow
  python3 get_photos.py

This downloads and compresses Wikimedia Commons photos that have suitable
reuse licences. Images from non-Commons photo websites remain linked and
are not rehosted. Then upload the generated .webp photos beside index.html.
Attributions for the downloaded images are collected in PHOTO_CREDITS.txt.

Use Safari -> Share -> Add to Home Screen on iPhone.
