### Focus of this fork:

This fork is geared toward personal use, with narrower scope than the Scrybble Remarks project:
- Consistent coordinates for drawing/highlight annotations on pdf output, for portrait-orientation books, on tablet software 3.3.2.1666. 
- Revised obsidian output

The following are not goals of this fork. Please use upstream:
- OCR 
- Non-pdf outputs (svg, png). These may still work, but not currently checking
- Support for keyboard input or textboxes

___

# Scrybble remarks

With Remarks, you can export notebooks and PDFs from your ReMarkable.

1. Export your notebooks as PDF
2. Extract highlights as text



## Goals

This is a fork of https://github.com/lucasrla/remarks. This fork has a few goals

- Support ReMarkable v3
- Support Type Folio output
- Retain support for older ReMarkable versions
- Note: This fork **does not** support all original output variants offered by the original remarks. The focus lies only on getting PDFs and text highlights out. You can use other tools such as Pandoc for conversion.

This project assumes familiarity with `git`, `python` and the commandline.

## A visual example

Highlight and annotate PDFs

<!-- How to host images on GitHub but outside your repository? Open an issue, upload your images, and voila! Trick learned from http://felixhayashi.github.io/ReadmeGalleryCreatorForGitHub/ -->

<img width="300" alt="IMG_0642-low.jpg" src="https://user-images.githubusercontent.com/1920195/88480247-3d776680-cf2b-11ea-9c30-061ec0e5cc60.jpg">

And then use `remarks` to export annotated pages to `Markdown`, `PDF`, `PNG`, or `SVG` on your computer:

<img width="300" alt="demo-remarks-png.png" src="https://user-images.githubusercontent.com/1920195/88480249-410aed80-cf2b-11ea-919b-22fb550ed9d7.png">

> <mark>WHAT IS LIFE?</mark>
> 
> Based on lectures delivered under the auspices of the <mark>Dublin Institute for</mark> <mark>Advanced Studies at Trinity College,</mark> Dublin, in February 1943
> 
> <mark>To</mark>
> <mark>the memory of My</mark> <mark>Parents</mark>

## Installing Remarks

Linux is recommended, Windows should work too.

- Install Python 3.10+ and [Poetry](https://python-poetry.org/docs/)

```bash
## Get remarks on your computer
git clone https://github.com/lucasrla/remarks.git && cd remarks
## Install the dependencies
poetry install
```

## Using Remarks

To get `remarks` up and running on your local machine, follow the instructions below:

### 1. Copy reMarkable's "raw" document files to your computer

In order to reconstruct your highlights and annotations, `remarks` relies on specific files that are created by the reMarkable device as you use it. Because these specific files are internal to the reMarkable device, first we need to transfer them to your computer.

There are several options for getting them to your computer. Find below some suggestions. Choose whatever fits you:

- **Use `rsync`** ([i](https://en.wikipedia.org/wiki/Rsync))  
  Check out the repository [@lucasrla/remarkable-utils](https://github.com/lucasrla/remarkable-utils) for the SSH & `rsync` setup I use (which includes automatic backups based on `cron`). 

- **Use `scp`** ([i](https://en.wikipedia.org/wiki/Secure_copy_protocol))  
  On your reMarkable tablet, go to `Menu > Settings > Help`, then under `About` tap on `Copyrights and licenses`. In `General information`, right after the section titled "GPLv3 Compliance", there will be the username (`root`), password and IP address needed for `SSH`ing into it. Using these credentials, `scp` the contents of `/home/root/.local/share/remarkable/xochitl` from your reMarkable to a directory on your computer. (Copying may take a while depending on the size of your document collection and the quality of your WiFi network.) To prevent any unintented interruptions, you can (optionally) switch off the `Auto sleep` feature in `Menu > Settings > Battery` before transferring your files.

- **Use [@juruen/rmapi](https://github.com/juruen/rmapi) or [@subutux/rmapy](https://github.com/subutux/rmapy)**  
  Both are free and open source software that allow you to access your reMarkable tablet files through reMarkable's cloud service.

- **Copy from reMarkable's official desktop application**  
  If you have a [reMarkable's official desktop app](https://support.remarkable.com/s/article/Desktop-app) installed, _most_ of the files we need are already easily available on your computer. For macOS users, the files are located at `~/Library/Application\ Support/remarkable/desktop`. To avoid interfering with reMarkable's official app, copy and paste all the contents of `~/Library/Application\ Support/remarkable/desktop` to another directory (one that you can safely interact with – say, `~/Documents/remarkable/docs`). Please note that this method won't allow you to use remarks' EPUB functionality. That's because this directory doesn't seem to include the [PDF files that reMarkable auto converts your EPUBs to](https://github.com/lucasrla/remarks/pull/34).

## Usage and Demo

Run `remarks` and check out what arguments are available:


```sh
# Alan Turing's 1936 foundational paper (with a few highlights and scribbles)

# Original PDF file downloaded from:
# "On Computable Numbers, with an Application to the Entscheidungsproblem"
# https://londmathsoc.onlinelibrary.wiley.com/doi/abs/10.1112/plms/s2-42.1.230

python -m remarks demo/on-computable-numbers/xochitl remarks-example/
```

A few other examples:

```sh
# Assuming your `xochitl` files are at `~/backups/remarkable/xochitl/`

python -m remarks ~/backups/remarkable/xochitl/ example_1/

python -m remarks ~/backups/remarkable/xochitl/ example_2/
```

## Tests

Run `pytest` in the root directory of the project after installing the dependencies using `poetry`. This will create files in the `tests/out` directory. The contents of this directory can safely be deleted.

Example:

```sh
python -m pytest -q remarks/test_initial.py
```

## Credits and Acknowledgements

- [Scrybble](https://scrybble.ink) A paid user-friendly service that helps non-technical ReMarkable users synchronize their notebooks to Obsidian. Financially supports @Azeirah to work on remarks.

- [lucasrla](https://github.com/lucasrla) who wrote the original implementation of remarks

- [@JorjMcKie](https://github.com/JorjMcKie) who wrote and maintains the great [PyMuPDF](https://github.com/pymupdf/PyMuPDF)

- [u/stucule](https://www.reddit.com/user/stucule/) who [posted to r/RemarkableTablet](https://www.reddit.com/r/RemarkableTablet/comments/7c5fh0/work_in_progress_format_of_the_lines_files/) the first account (that I could find online) about reverse engineering `.rm` files

- [@ax3l](https://github.com/ax3l) who wrote [lines-are-rusty](https://github.com/ax3l/lines-are-rusty) / [lines-are-beautiful](https://github.com/ax3l/lines-are-beautiful) and also [contributed to reverse engineering of `.rm` files](https://plasma.ninja/blog/devices/remarkable/binary/format/2017/12/26/reMarkable-lines-file-format.html)

- [@edupont, @Liblor, @florian-wagner, and @jackjackk for their contributions to rM2svg](https://github.com/reHackable/maxio/blob/33cdc1706b29698c15aac647619374e895ed3869/tools/rM2svg)

- [@ericsfraga, @jmiserez](https://github.com/jmiserez/maxio/blob/ee15bcc86e4426acd5fc70e717468862dce29fb8/tmp-rm16-ericsfraga-rm2svg.py), [@peerdavid](https://github.com/peerdavid/rmapi/blob/master/tools/rM2svg), [@phill777](https://github.com/phil777/maxio) and [@lschwetlick](https://github.com/lschwetlick/maxio/blob/master/rm_tools/rM2svg.py) for updating rM2svg to the most recent `.rm` format

- [@lschwetlick](https://github.com/lschwetlick) who wrote [rMsync](https://github.com/lschwetlick/rMsync) and also two blog posts about reMarkable-related software [[1](http://lisaschwetlick.de/blog/2018/03/25/reMarkable/), [2](http://lisaschwetlick.de/blog/2019/06/10/reMarkable-Update/)]

- [@soulisalmed](https://github.com/soulisalmed) who wrote [biff](https://github.com/soulisalmed/biff)

- [@benlongo](https://github.com/benlongo) who wrote [remarkable-highlights](https://github.com/benlongo/remarkable-highlights)

For more reMarkable resources, check out [awesome-reMarkable](https://github.com/reHackable/awesome-reMarkable) and [remarkablewiki.com](https://remarkablewiki.com/).

## License

`remarks` is [Free Software](https://www.gnu.org/philosophy/free-sw.html) distributed under the [GNU General Public License v3.0](https://choosealicense.com/licenses/gpl-3.0/).

## Disclaimers

This is a hobby project of an enthusiastic reMarkable user. There is no warranty whatsoever. Use it at your own risk.

> The author(s) and contributor(s) are not associated with reMarkable AS, Norway. reMarkable is a registered trademark of reMarkable AS in some countries. Please see https://remarkable.com for their products.
