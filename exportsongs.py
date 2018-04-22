import os, sys
import mido

def readFile(path):
    inFile = open(path, 'r')
    
    offset = inFile.readline()
    mtrk = inFile.readline() # "MTrk"

    offset = int(offset.split(':')[1])
    offset = 0

    midi = mido.MidiFile(type=1)
    midi.add_track('jb_tempo')
    midi.add_track('main')

    tempo = midi.tracks[0]
    track = midi.tracks[1]

    prevAbsTicks = 0

    for line in inFile.readlines():
        ev = line.split(' ')
        
        if (len(ev) <= 1):
            continue
        
        absTicks = int(ev[0])
        evType = ev[1]
        delTicks = absTicks - prevAbsTicks

        if (evType == 'Tempo'):
            # Tempo
            t = int(ev[2])

            # Adds midi event
            tempo.append(mido.MetaMessage('set_tempo', time = delTicks, tempo = t))
        elif (evType == 'On' or evType == 'Off'):
            # Channel, note, velocity
            ch = int(ev[2].split('=')[1]) - 1 # 0-index
            n  = int(ev[3].split('=')[1])
            v  = int(ev[4].split('=')[1])

            # Adds midi event
            track.append(mido.Message('note_' + evType.lower(), time = delTicks, channel = ch, note = n, velocity = v))
        else:
            # TODO: Parse additional events?
            pass
        
        # Sets previous ticks
        prevAbsTicks = absTicks
    
    #midi.save('thefightsong.mid')
    
def convertSong(sc9Path, otherFiles, songName):
    print(str.format('Converting \'{}\'', songName))

    pass

def exportSongs(jambandRoot, exportRoot):
    songPath = os.path.join(jambandRoot, 'songs')
    
    if (not os.path.exists(songPath)):
        print(str.format('\'{}\' does not exist, quiting', songPath))

    files = []

    # Gets all files in song directory (not recursive)
    for (dirPath, dirNames, fileNames) in os.walk(songPath):
        files.extend(fileNames)
        break

    # Removes non .sc9 files (Song data)
    songs = filter(lambda a: a.endswith('.SC9'), files)

    # Removes .sc9 files
    files = filter(lambda a: not a.endswith('.SC9'), files)

    for song in songs:
        name = os.path.splitext(os.path.basename(song))[0]
        songFiles = filter(lambda a: name in a, files)

        convertSong(song, songFiles, name)

    return

def main(args):
    if (len(args) < 3):
        print("args: [path_to_jamband_install] [path_to_export]")
        return

    pathJamband = os.path.abspath(args[1])
    pathExport = os.path.abspath(args[2])

    exportSongs(pathJamband, pathExport)

if (__name__ == '__main__'):
    main(sys.argv)