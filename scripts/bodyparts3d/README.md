# Skeleton pictures from BodyParts3D

The pictures in `data/figures/anatomy/` are drawn from [BodyParts3D](https://dbarchive.biosciencedbc.jp/en/bodyparts3d/download.html), a set of 3D models of the human body: BodyParts3D, © The Database Center for Life Science, licensed under [CC BY-SA 2.1 JP](https://creativecommons.org/licenses/by-sa/2.1/jp/deed.en). The pictures are adaptations, so they carry the same licence, and every question that shows one says so under it (`figure.credit`, `license`, `source`).

Each picture is the skeleton (or part of it) with one or more parts coloured red. `jobs.py` lists them: which parts to colour (`hi`), which to frame (`focus`), which to draw at all (`only`, `hide`), the view (`front`, `back`, `left`, `right`, `top`, `bottom` or a direction), the size, and `xray` to make everything else see-through. `parts.tsv` is the BodyParts3D parts used: the bones, costal cartilages and intervertebral discs (drawn grey-blue).

To draw them again, or new ones for another chapter:

```sh
cd scripts/bodyparts3d
# the models: a copy of BodyParts3D 3.0 converted to STL, with only the parts listed in parts.tsv checked out
git clone --filter=blob:none --no-checkout https://github.com/Kevin-Mattheus-Moerman/BodyParts3D bp3d
cut -f1 parts.tsv | sed 's|.*|assets/BodyParts3D_data/stl/&.stl|' | git -C bp3d checkout HEAD --pathspec-from-file=-
ln -s bp3d/assets/BodyParts3D_data/stl stl
npm install --no-save three@0.160.0 playwright
python3 jobs.py            # writes jobs.json; name some jobs to draw only those: python3 jobs.py femur tibia
node shoot.js jobs.json out
for f in out/*.png; do convert "$f" -trim -bordercolor white -border 14 -resize 75% -quality 78 -define webp:method=6 "../../data/figures/anatomy/$(basename "$f" .png).webp"; done
```

`bp3d/`, `stl`, `node_modules/`, `jobs.json` and `out/` are working files; don't commit them.
