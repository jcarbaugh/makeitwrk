#!/usr/bin/env python
from struct import pack, unpack
import sys

CHUNK_TYPES = {
    1: 'TRACK_CHUNK',
    2: 'STREAM_CHUNK',
    4: 'METER_CHUNK',
    5: 'TEMPO_CHUNK',
    6: 'SYSEX_CHUNK',
    7: 'MEMRGN_CHUNK',
    10: 'TIMEBASE_CHUNK',
    
    # variables
    3: 'VARS_CHUNK',
    26: 'VARS_CHUNK_VAR',
    
    # device stuff
    33: 'DEVICES',
    
    # track stuff?
    36: 'TRACK_NAME?',
    54: 'TRACK_PORT',
    45: 'TRACK_DATA?',
    
    255: 'END_CHUNK',
}

def solomon(arr, parts):
    for i in range(0, parts * 8, 8):
        yield arr[i:i+8]

def chunk_reader(wrkfile):
    
    if wrkfile.read(8) != b'CAKEWALK':
        raise ValueError('invalid file format')
    
    wrkfile.read(1) # byte I don't care about
    
    mm_version = wrkfile.read(2)
    major = ord(mm_version[1])
    minor = ord(mm_version[0])
    version = "%i.%i" % (major, minor)
    
    yield ('VERSION_CHUNK', 2, None, version)
    
    while 1:
        
        ch_type_data = wrkfile.read(1)[0]
        ch_type = CHUNK_TYPES.get(ch_type_data, ch_type_data)
        
        if ch_type == 'END_CHUNK':
            break
        
        ch_len = unpack('i', wrkfile.read(4))[0]
        
        ch_data_offset = wrkfile.tell()
        #print(ch_data_offset)
        
        ch_data = wrkfile.read(ch_len)
        
        yield (ch_type, ch_len, ch_data)
        
    yield ('END_CHUNK', None, None, None)
    
    wrkfile.close()


if __name__ == '__main__':
    
    for chunk in chunk_reader(sys.stdin):
        print(chunk)
        # if chunk[0] == 'TRACK_NAME?':
        #     (tnum, tname_len) = unpack('HB', chunk[2][:3])
        #     tname = chunk[2][3:3+tname_len].decode('utf-8')
        #     print("[%02i] %s" % (tnum, tname))
        # elif chunk[0] == 'TRACK_DATA?':
        #     (tnum, schunks) = unpack('=HxH', chunk[2][:5])
        #     print('   ', '------------')
        #     for s in solomon(chunk[2][7:], schunks):
        #         print('   ', unpack('8B', s))
                

"""
__TRACK_DATA__
#2   ?? CNT- ???? 16---------------
0900 00 0700 0000 B649 009023641E00 D449 009028643C00 104A 00902B643C00 4C4A 009029643C00 884A 009023641E00 A64A 009023641E00 E24A 009023641E00
0900 00 0700 0000 1E4B 009023641E00 3C4B 009028643C00 784B 00902B643C00 B44B 009029643C00 F04B 009023641E00 0E4C 009023641E00 4A4C 009023641E00
                  (30, 75, 0, 144, 35, 100, 30, 0)
                   submeasure .    .   .    .
                       measure.    .   .    .
                           ?  .    .   .    .
                              ?    .   .    .
                                   nt? .    .
                                       ?    .
                                            -----?
------------------------------------
0000 00 0800 0000 E010 009045643C00 1C11 009045643C00 5811 00904C643C00 9411 009045643C00 D011 00904D643C00 0C12 00904C643C00 4812 009048643C00 8412 009045643C00
0200 00 1400 0000 8016 00902664E001 3417 009026643C00 7017 009026647800 E817 009026647800 2418 009026643C00 6018 00902264E001 1419 009022643C00 5019 009022647800 C819 009022647800041A009022643C00401A00901F64E001F41A00901F643C00301B00901F647800A81B00901F647800E41B00901F643C00201C00902164E001D41C009021643C00101D009021647800881D009021647800C41D009021643C00
__TRACK_NAME__

#2 L2   NAME*                         INSTRUMENT?
0000 05 4F7267616E               FFFF 1500 FFFFFFFF 00000000000000 0A 0000000000
        O R G A N
0100 0B 536C617020426173732031   FFFF 2500 FFFFFFFF 00000000000000 0A 0000010000
        S L A P   B A S S   1 
0200 0B 536C617020426173732032   FFFF 2400 FFFFFFFF 00000000000000 FE 0000020000
        S L A P   B A S S   2 
0300 0C 4869676820537472696E6773 FFFF 2C00 FFFFFFFF 00000000000000 0A 0000030000
        H I G H   S T R I N G S 
0900 05 4472756D73               FFFF FFFF FFFFFFFF 00000000000000 0A 0000090000
        D R U M S
-------------------------------------------
0000 05 4472756D73               FFFF FFFF FFFFFFFF 00000000000000 0A 0000090000
        D R U M S 
"""