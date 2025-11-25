# ipod_theme_max_features
Theme your iPod nano 7th and 6th generation with custom icons, wallpapers, clock faces, change or hide labels, apply custom font, and more. Based on [ipod_sun](https://github.com/CUB3D/ipod_sun), [ipodhax](https://github.com/760ceb3b9c0ba4872cadf3ce35a7a494/ipodhax), and [silverutil](https://github.com/spotlightishere/silverutil), who collectively made 99.9% of the research and code to get us here.

This fork aims to make this utility with maximum functionality
* [x] Support for modding all languages
* [x] Support for changing sounds
* [x] Support for a new way to run iPod with modified resources(only for nano 7 iPods, not working on nano 6)
* [ ] Apply the capabilities we have with `star` exploit(all possible features)

Join [iPod nano 6/7 Themes discord server](https://discord.gg/SfWYYPUAEZ) to share and download pre-made themes, and [iPod nano hacking discord server](https://discord.gg/7PnGEXjW3X) for hacking iPod nano, then share your themes and setup with [r/ipod](https://www.reddit.com/r/ipod/)!

### Tutorial

Before using `ipod_theme`, you need to install some dependencies first.

[1] If you are running macOS or Linux, launch the Terminal app. If you are running Windows, install [Linux on Windows with WSL](https://learn.microsoft.com/windows/wsl/install), launch Ubuntu from the Start menu or Windows Terminal app, and follow instructions for Linux.

[2] Only if you're running macOS, install Homebrew and add it to the PATH environment:

```shell
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
echo >> ~/.zprofile
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

[3] Only if you're running macOS, install `arm-none-eabi-gcc`:

```shell
brew install arm-none-eabi-gcc
```

[4] Only if you're running Linux, install `xdg-utils`, `unzip`, `pkg-config`, `libssl-dev`, `python3-pip`, and `gcc-arm-none-eabi`:

```shell
sudo apt update && sudo apt install xdg-utils unzip pkg-config libssl-dev python3-pip gcc-arm-none-eabi -y
```

[5] Install Rust. When asked to proceed with standard installation, just press enter:

```shell
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

[6] Add Rust to the PATH environment.

```shell
. "$HOME/.cargo/env"
```

[7] Install `pyfatfs`, `fonttools`, and `pillow`:

```shell
export PIP_BREAK_SYSTEM_PACKAGES=1 && pip3 install pyfatfs fonttools pillow
```

#### 1) Download and unpack iPod firmware:

- Download and unzip `ipod_theme`, then cd into unzipped path:

```shell
mkdir -p ~/Downloads && cd ~/Downloads && curl -L -o ipod_theme-master.zip "https://github.com/nfzerox/ipod_theme/archive/refs/heads/master.zip" && unzip -o ipod_theme-master.zip && cd ipod_theme-master
```

- For iPod nano 7th generation, run:

```shell
./01_firmware_unpack_7g
```

- For iPod nano 6th generation, run:

```shell
./01_firmware_unpack_6g
```
Make sure you only run the unpack command that matches your iPod model. This automatically downloads the latest firmware, then extracts artwork and translation binaries from it. It will also generate a custom firmware that isn't themed, which you can safely ignore.

#### 2) Unpack and update artwork:

- Unpack the artwork.

```shell
python3 ./02_art_unpack.py
```

- For macOS or Linux, open the `body` folder with:

```shell
open ./body
```

- For Linux on Windows with WSL, open the `body` folder with:

```shell
explorer.exe `wslpath -w $(pwd)/body`
```

This opens the unpacked `body` folder, which contains all artwork including icons, wallpapers, clock faces, and more.

When replacing any artwork, your new artwork must exactly match the resolution and color format of the original. The color format is specified in the suffix of the artwork:

- `*_0004.png`: 4-bit greyscale
- `*_0008.png`: 8-bit greyscale
- `*_0064.png`: No more than 255 colors
- `*_0065.png`: No more than 65545 colors
- `*_0565.png`: RGB565
- `*_1888.png`: Any RGB with alpha

If the original artwork doesn't end with `_1888.png`, and your new artwork contains a larger number of total colors than the original, you must use Indexed Color in Photoshop to reduce the total number of colors. After reducing the total number of colors with Photoshop, open and re-save the processed artwork using Preview (Mac) or Paint (Windows).

If you don't have Photoshop or don't want to reduce the total number of colors, you can also delete the original artwork, then save yours as `*********_1888.png`. For example, delete `229442246_0065.png` and save yours as `229442246_1888.png`.

Don't replace too many non `*_1888.png` artwork with `*_1888.png`, as this will exceed the rsrc partition size limit and cause custom firmware repack to fail in step 6. To save space, only replace artwork that matches your iPod color. Never delete artwork without making a replacement.

After replacing icons, replace the tapdown shape mask. It is the artwork right before the first icon.

Advanced Tip: If you need to figure out which file an artwork corresponds to, you can generate a full replacement set with reference labels on solid fill using `python3 ./02_art_z_generate_reference_labels_only.py`. Take caution as this will override all existing artwork.

#### 3) Repack updated artwork:

```shell
python3 ./03_art_pack.py
```
This packs your custom artwork into `SilverImagesDB.LE.bin2`, which automatically gets used in step 6.

If it fails, the failing artwork is the one after the last successful artwork. Check the format of your new artwork, and make sure it exactly matches the original, then repeat this step.

If you want to remove all custom artwork and start over, repeat step 2.

#### 4) Unpack and repack translations (optional):

```shell
./04_optional_strings_unpack
```
This will open a huge list of choices where you can select either all languages or just certain ones, after which the languages will be unpacked along the path `path/to/ipod_theme/Languages/SilverDB."lang".LE`. Open this directory and find the `Str .yaml` file there and open it in your favorite text editor (or one that supports yaml files). You may edit values after `!String ` as you see fit. Unless you're trying to hide a label, the space character between `!String` and the translation is required.

To change app labels on the Home Screen, use Command+F to find the second instance of `Music`. This is where app label translations begin. You can change or delete `Music` from the line, and repeat the same for other app names.

The `iTunes U` app is hidden from iPod by default unless you've synced an iTunes U lecture from iTunes. The label for `iTunes U` is not translated and cannot be hidden.

Once you're done, save your changes and run:

```shell
./05_optional_strings_pack
```
This will show a list of your unpacked languages, you can select all or just some, after that this script packs your custom translations into `SilverDB."lang".LE.bin2` packs, which automatically gets used in step 6.

#### 5) Apply custom font (optional):

Find your favorite font on [Google Fonts](https://fonts.google.com/), then click Get Font > Download all. Unzip your download, then drill into the `static` folder.

Rename the font that ends in `-Regular.ttf` into `Helvetica.ttf`. Rename the font that ends in `-Bold.ttf` into `HelveticaBold.ttf`.

- For macOS or Linux, open the `Fonts` folder with:

```shell
open ./Fonts
```

- For Linux on Windows with WSL, open the `Fonts` folder with:

```shell
explorer.exe `wslpath -w $(pwd)/Fonts`
```

Copy `Helvetica.ttf` and `HelveticaBold.ttf` into the `Fonts` folder.

Tip: Not all fonts are compatible with iPod nano. If your iPod fails to boot after applying a custom font, try a different font, or remove your custom fonts from the `Fonts` folder.

#### 6) Replacing sounds:
When unpacking, a `Sounds` folder should appear in the folder. Open it and look through all the sounds. To replace a specific sound, select any sound you want to replace (it must match the extension of the original file, if it doesn't match, convert it) and add the `.new` extension to the file, after which the sound will be automatically used during packing

#### 7) Repack iPod firmware:

- For iPod nano 7th generation, run:

```shell
./06_firmware_pack_7g
```

- For iPod nano 6th generation, run:

```shell
./06_firmware_pack_6g
```
This repacks your artwork and translations into a new custom firmware with swapped osos and rsrc.

If you see any error in purple or pink, the firmware repack has failed. Even if Terminal shows "Successfully zipped the directory", the resulting firmware is likely corrupted and should never be used.

If you see `pyfatfs._exceptions.PyFATException: Not enough free space to allocate ******** bytes (******** bytes free)`, it means the repack failed because your replacement artwork (or sounds) is too large. You can subtract those two numbers and divide it by 1000 to determine how many KB of extra artwork(or sounds) to shave off. Then repeat step 2-3, but with fewer artwork replacements, or with reduced number of colors using Indexed Color with Photoshop, or with reduced quality of sounds using converters(any converter) then try step 7 again.

For iPod nano 7th generation (2012), the repacked firmware is called `iPod_1.1.2_39A10023_2012_repack.ipsw`. For iPod nano 7th generation (2015), the repacked firmware is called `iPod_1.1.2_39A10023_2015_repack.ipsw`.

For iPod nano 6th generation, the repacked firmware is called `iPod_1.2_36B10147_repack.ipsw`.

- For macOS or Linux, open the folder that contains the repacked firmware with:

```shell
open .
```

- For Linux on Windows with WSL, open the folder that contains the repacked firmware with:

```shell
explorer.exe .
```

#### 8) Flash custom firmware:

Connect your iPod to your computer. Before flashing custom firmware, back up your iPod. On macOS or Linux, double click the iPod icon on your Desktop to open it as a disk. On Windows, open File Explorer and double click your iPod.

On macOS, press `Command`+`Shift`+`.` to show hidden files. On Linux, press `Ctrl`+`H` (command may differ depending on distro) to show hidden files. On Windows, use View > Show > Hidden items to show hidden files. Make sure you can see the hidden `iPod_Control` folder which contains all your media, then copy everything from your iPod to a new folder on your computer.

Select your iPod in the sidebar of Finder or iTunes. If you are running Linux, you can use a Windows virtual machine and connect your iPod to the virtual machine. Hold down the Option key (Mac), or Shift key (Windows) and click Check for Update, then choose the repacked custom ipsw firmware from step 6.

After your iPod finishes updating, you should see your custom artwork. To see your custom translations or hidden app labels, open Settings > General > Language > Select any language you have edited > Save.

Note: When running custom themed firmware, iPod nano 6th generation may forget song ratings, playlist edits, or changed settings after reboot. To work around this, perform step 9, make your changes, then step 7 again. This doesn't affect iPod nano 7th generation.

#### 9) If your iPod shows "OK to disconnect" in black and white(Only relevant for iPod nano 6 owners):
If you restart your iPod, or if your iPod battery dies, it will boot into disk mode, showing "OK to disconnect" in black and white. This is expected for custom iPod nano firmware, because it relies on swapping regular OS and disk mode to work.

For iPod nano 7th generation:

- The problem is not relevant due to the new modification method

For iPod nano 6th generation:

- Press and hold both the volume down button and the power button until you see the Apple logo.
- Once you see the Apple logo, immediately release the power button.
- Then immediately press and hold both volume down and volume up buttons, until your see the Home Screen.

#### 10) Go back to stock firmware:
You can go back to stock firmware while preserving data. First download the stock firmware for your iPod:

- [iPod nano 7th generation (2015)](https://secure-appldnld.apple.com/ipod/sbml/osx/bundles/031-59796-20160525-8E6A5D46-21FF-11E6-89D1-C5D3662719FC/iPod_1.1.2_39A10023.ipsw)
- [iPod nano 7th generation (2012)](https://secure-appldnld.apple.com/iPod/SBML/osx/bundles/031-26260-201500810-D2BC269E-3FBC-11E5-885A-067B3A53DB92/iPod_1.0.4_37A40005.ipsw)
- [iPod nano 6th generation](https://secure-appldnld.apple.com/iPod/SBML/osx/bundles/041-1920.20111004.CpeEw/iPod_1.2_36B10147.ipsw)

Select your iPod in the sidebar of Finder or iTunes. Hold down the Option key (Mac) or Shift key (Windows), and click Check for Update, then choose the stock firmware you just downloaded.

Note: For iPod nano 7th generation (2012), you need to "update" from custom 1.1.2 firmware to stock 1.0.4 firmware. This is safe, you won't lose data or encounter functional issues.

#### 11) If your iPod doesn't boot at all, or shows a "Connect to iTunes" Recovery screen:
- Connect your iPod to a Windows PC or older Mac running macOS Mojave (10.14) or earlier. This also works if you use a Windows virtual machine on Linux, as long as you connect your iPod to the virtual machine.
- Open iTunes on your Windows PC or older Mac.
- For iPod nano 7th generation, press and hold both the Home button and the power button until iTunes detects it in DFU mode.
- For iPod nano 6th generation, press and hold both the volume down button and the power button until iTunes detects it in DFU mode.
- Click "Restore iPod".
- After restore completes, connect it back to your Mac.
- On macOS or Linux, double click the iPod icon on your Desktop to open it as a disk. On Windows, open File Explorer and double click your iPod.
- Delete everything on your iPod, copy your backup made in step 7 back to your iPod, then eject it from the sidebar of Finder (Mac), Files (Linux), or taskbar (Windows).
- Your iPod should spring back to life with all previous data.
