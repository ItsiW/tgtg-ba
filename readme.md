# The Good Taste Guide™

## Running locally on linux

install ```entr```

```
ls-files | entr python build.py
```
and in a separate terminal
```
cd build
python3 -m http.server 8080
```
open link [```localhost:8080```](localhost:8080) (if you open ```0.0.0.0:8080``` then the map will not render).

## Adding Memes

If you wish to add a meme, just put the raw file in ```raw/memes```, there is pre-processing in ```build.py``` to handle them.
