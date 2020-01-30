# Tests

These scripts were meant to be executed manually to try the task steps on
different datasets. The tests also serve as a documentation and guidelines on how
to use the scripts included in this package.

The following datasets can be tested:

## 1. bigbrain.sh

  The BigBrain atlas

## colin.sh

  Colin Nifti

## kg-1

  Unregistered/unaligned stack of tiffs

## kg-2

  One multipage tiff, suggested by Timo

  >
as I wrote earlier, I would suggest to visualize a volumetric image from human brain from Pavone’s group. Here’s one provided as a 4GB tif:
https://kg.ebrains.eu/search/instances/Dataset/44ac63f7dc4c5f0f5db43fb829193537

> This image is currently not viewable at all. Users would have to download and care about visualization themselves. For most of them, it will fail as they do not know the right offline tools (Vaa3d should actually work)

## kg-3

  Aligned stack of tiffs, suggested by Xiao

  > Perhaps we should use a volume which had already been registered? I had a brief look in datasets contributed by Pavone, and this is the first hit:
  >
  > "Hippocampal image volume derived from Thy1-GFP-M transgenic mouse"
  >
  > https://kg.ebrains.eu/search/?q=pavone&facet_type[0]=Dataset#Dataset/8fb1a664ca3390bae960cc1aa11f5827

  > And upon downloading and looking into the tiffinfo of the tiff stack, it seems they have the same dimension:
