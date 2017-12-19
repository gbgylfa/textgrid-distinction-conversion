# textgrid-distinction-conversion

textgrid_distinction_conversion.py: Uses audiolabel to go through all of the aligned .TextGrid files in a directory and replace S on the phone tier with Z where it is appropriate in Castilian Spanish, based on orthography on the corresponding word tier.

The script takes two arguments: the directory containing the text grids and the directory for the output files. Note that this script assumes that your tiers are in order with phone tier first, then word tier, then phone tier, then word tier, and so on, with no extra tiers, and that words are in uppercase - standard output format for the FASE aligner.
