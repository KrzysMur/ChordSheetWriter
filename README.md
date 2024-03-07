
# ChordSheetWriter
Simple and easy to use program to write chord sheets

Download csw.exe from the latest release to use this program.

# Requirements

- MikTex

To use source code:
- Python > 3.10 (3.12 recommended)
- PyQt6 package in Python environment

# How to write chordsheet?

Header of file may contain:

title=[title of the song] 

author=[author of the song]

album=[currently not used] 

key=[key of the song] 

tempo=[tempo of the song] 

chords=[chords used in the song separated with comas]

capo = [capo for guitar]

##

| - normal bar line

[ ] - repeat bar lines

|chord_chord_chord_chord| - chords in a bar must be seperated with underscore

(4/4) - time signature in parentheses
##

For example:

    title=Mountain Time
    author=Joe Bonamassa
    album=Out of Time
    key=E
    tempo=102
    chords=E, D, Bm, C#m, A, E/G#, B
    capo = 2
    
    (4/4) [E_D|E_D|E_D|Bm_C#m_D_Bm]
    [B|A_E/G#|B|A_E/G#]
    [E_D|E_D|E_D|Bm_C#m_D_Bm]
    [B|A_E/G#]
    [B|A_E/G#|B|A_E/G#]
    [E_D|E_D|E_D|Bm_C#m_D_Bm]
    |E|Bm|E|Bm_C#m_D_Bm|
    [E_D|E_D|E_D|Bm_C#m_D_Bm]
    [E_D|E_D|E_D|Bm_C#m_D_Bm]
    [E_D|E_D|E_D|Bm_C#m_D_Bm]
    [E_D|E_D|E_D|Bm_C#m_D_Bm]
