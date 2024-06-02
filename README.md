# Behringer Flow 8 MIDI Control Python
## Description

Python program for controlling the Behringer Flow 8 digital audio desk using MIDI over USB.

This program has only been tested on Linux but should work in theory on other platforms (driver dependent).

Uses the python library [MIDIUtil](https://github.com/sourcebox/midiutil) written by sourcebox under the BSD license.

## Installation
1. Connect to the Behringer Flow 8 desk via USB.
2. Clone the repo ```git clone https://github.com/JamboPE/Flow8Control.git```
3. Run the program in the command line: ```python3 flow8Control.py```

For linux users, this command can be added as alias in your ```.bashrc``` file.

## Usage
    Usage: flow8Control.py [FLAGS] [OPTIONS]
    
    flags:
        -c, -channel [CHANNEL]    Select channel to control
        -b, -bus [BUS]            Select bus to control (LR, Mon1, Mon2, FX1, FX2)
        -s, -snapshot [SNAPSHOT]  Load a snapshot
        -r, -reset                Reset desk to default state
        -h, -help                 Display this help message
        
    CHANNEL Options:
        -level [LEVEL]      Set fader level
        -balance [BALANCE]  Set balance level
        -mute [ON/OFF]      Set mute state
        -solo [ON/OFF]      Set solo state
        -EQ [BAND] [LEVEL]  Set EQ level [BAND: 1-4]
        -gain [GAIN]        Set gain level
        -lowcut [FREQ]      Set lowcut frequency
        -comp [COMP]        Set compressor level
        -phantom [ON/OFF]   Set phantom power state
        -mon1 [LEVEL]       Set monitor 1 send level
        -mon2 [LEVEL]       Set monitor 2 send level
        -fx1 [LEVEL]        Set FX 1 send level
        -fx2 [LEVEL]        Set FX 2 send level

    BUS Options:
        -level [LEVEL]      Set bus level
        -balance [BALANCE]  Set bus balance (main LR only)
        -limiter [LEVEL]    Set bus limiter level (excl. FX buses)
        -EQ [BAND] [LEVEL]  Set EQ level [BAND: 1-9] (excl. FX buses)
        -effect [EFFECT]    Set bus effect preset [1-16] (FX buses only)
        -fxmute [ON/OFF]    Set both FX buses mute state (FX buses only)
        -intensity [LEVEL]  Set the effect intensity (FX buses only)
        -fxoption [OPTION]  Set the effect option [1 or 2] (FX buses only)

## RAW Midi Documentation
Based on the [Quick Start Guide](https://mediadl.musictribe.com/media/PLM/data/docs/P0DNM/QSG_BE_0603-AEW_FLOW-8_WW.pdf) provided by Behringer (page 23).

### Midi Channels
| **Desk Channel**                                     | **MIDI Channel** |
|-------------------------------------------------|--------------|
| Channel 1                                       | 1            |
| Channel 2                                       | 2            |
| Channel 3                                       | 3            |
| Channel 4                                       | 4            |
| Channel 5/6                                     | 5            |
| Channel 7/8                                     | 6            |
| Ch. USB/BT                                      | 7            |
| Main Bus                                        | 8            |
| Mon1 Bus                                        | 9            |
| Mon2 Bus                                        | 10           |
| FX1 Bus                                         | 11           |
| FX2 Bus                                         | 12           |
| FX1 Slot Selection                              | 14           |
| FX2 Slot Selection                              | 15           |
| Snapshots - Whole Mixer, FX1/FX2 - Common Ctrl. | 16           |

### Desk Channel Commands
| **Command** | **Parameter**             | **Min. Value** | **Max. Value** | **Notes**        |
|-------------|---------------------------|----------------|----------------|------------------|
| CC 7        | Channel Level (to Main)   | 0              | 127            | -70 to +10dB     |
| CC 10       | Channel Balance (to Main) | 0              | 127            | 64 is centre     |
| CC 5        | Mute                      | 0              | 1-127          | 1-127 are all on |
| CC 6        | Solo                      | 0              | 1-127          | 1-127 are all on |
| CC 1        | EQ Low                    | 0              | 127            | 64 is centre     |
| CC 2        | EQ Low Mid                | 0              | 127            | 64 is centre     |
| CC 3        | EQ High Mid               | 0              | 127            | 64 is centre     |
| CC 4        | EQ High                   | 0              | 127            | 64 is centre     |
| CC 8        | Gain                      | 0              | 127            | -20 to 60dB      |
| CC 9        | Low Cut                   | 0              | 127            | 20 to 600Hz      |
| CC 11       | Compressor                | 0              | 100-127        | 0 to 100%        |
| CC 12       | 48V                       | 0              | 1-127          | 1-127 are all on |
| CC 14       | Send Level to Mon1        | 0              | 127            | -70 to +10dB     |
| CC 15       | Send Level to Mon2        | 0              | 127            | -70 to +10dB     |
| CC 16       | Send Level to FX1         | 0              | 127            | -70 to +10dB     |
| CC 17       | Send Level to FX2         | 0              | 127            | -70 to +10dB     |

### Bus Commands
| **Command** | **Parameter** | **Min. Value** | **Max. Value** | **Notes**                              |
|-------------|---------------|----------------|----------------|----------------------------------------|
| CC 7        | Bus Level     | 0              | 127            | -70 to +10dB                           |
| CC 10       | Bus Balance   | 0              | 127            | 64 is centre, only on Main bus         |
| CC 8        | Bus Limiter   | 0              | 127            | -30 to 0dB, not on FX buses            |
| CC 11       | EQ 62Hz       | 0              | 127            | -15 to +15dB, 64 is centre, not on FXs |
| CC 12       | EQ 125Hz      | 0              | 127            | -15 to +15dB, 64 is centre, not on FXs |
| CC 13       | EQ 250Hz      | 0              | 127            | -15 to +15dB, 64 is centre, not on FXs |
| CC 14       | EQ 500Hz      | 0              | 127            | -15 to +15dB, 64 is centre, not on FXs |
| CC 15       | EQ 1kHz       | 0              | 127            | -15 to +15dB, 64 is centre, not on FXs |
| CC 16       | EQ 2kHz       | 0              | 127            | -15 to +15dB, 64 is centre, not on FXs |
| CC 17       | EQ 4kHz       | 0              | 127            | -15 to +15dB, 64 is centre, not on FXs |
| CC 18       | EQ 8kHz       | 0              | 127            | -15 to +15dB, 64 is centre, not on FXs |
| CC 19       | EQ 16kHz      | 0              | 127            | -15 to +15dB, 64 is centre, not on FXs |

### FX Control Commands
MIDI Channels 14/15

| **Command** | **Parameter** | **Min. Value** | **Max. Value** | **Notes**                           |
|-------------|---------------|----------------|----------------|-------------------------------------|
| Prog. Chg.  | Effect Preset | 1              | 16             | Program Change 0 and 17-127 ignored |
| CC 1        | Parameter 1   | 0              | 100-127        | 0 to 100%                           |
| CC 2        | Parameter 2   | 0              | 1-127          | Value A = 0, Value B = 1-127        |

### Global Control
Midi Channel 16

| **Section** | **Command**  | **Parameter**       | **Min. Value** | **Max. Value** | **Notes**                                           |
|-------------|--------------|---------------------|----------------|----------------|-----------------------------------------------------|
| Snapshot    | Prog. Chg.   | Load Mixer Snapshot | 1              | 16             | Program Change 0 and 17-127 ignored, 16 resets desk |
| Fx1/Fx2     | CC 1         | FX Mute             | 0              | 1-127          | 0 = Unmute, 1-127 = Mute                            |
| Fx1/Fx2     | Note 0 (C-1) | Tap Tempo           | Velocity 1     | Velocity 127   | 50 to 250BPM, see quick start guide for more info   |


## Contributing

If you wish to contribute to this project, please email me at 
flow8-github@jdpe.co.uk

## License

Flow8Control:

    Copyright (c) 2024, Jamie Parker-East, <info@jdpe.co.uk>
    All rights reserved.

    Software is under the GNU General Public License v3.0

MIDIUtils:

    Copyright (c) 2012, Oliver Rockstedt, <info@sourcebox.de>
    All rights reserved.

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are met:
        * Redistributions of source code must retain the above copyright
        notice, this list of conditions and the following disclaimer.
        * Redistributions in binary form must reproduce the above copyright
        notice, this list of conditions and the following disclaimer in the
        documentation and/or other materials provided with the distribution.
        * Neither the name of the <organization> nor the
        names of its contributors may be used to endorse or promote products
        derived from this software without specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
    ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
    WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
    DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
    DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
    (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
    LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
    ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
    (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
