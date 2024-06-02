# Behringer Flow 8 MIDI Control Python

This program has only been tested on Linux.

# Setup
1. Connect to the Behringer Flow 8 desk via USB.
2. Install the python dependencies: ```pip install MIDIUtil```
3. Run the program .

## Usage
    Usage: python3 ./flow8Control.py -c [CHANNEL] [OPTIONS]
            Options:
                -level [LEVEL]      Set fader level
                -balance [BALANCE]  Set balance level
                -mute [ON/OFF]      Set mute state
                -solo [ON/OFF]      Set solo state
                -gain [GAIN]        Set gain level
                -lowcut [FREQ]      Set lowcut frequency
                -comp [COMP]        Set compressor level
                -phantom [ON/OFF]   Set phantom power state
                -mon1 [LEVEL]       Set monitor 1 send level
                -mon2 [LEVEL]       Set monitor 2 send level
                -fx1 [LEVEL]        Set FX 1 send level
                -fx2 [LEVEL]        Set FX 2 send level

## Midi Commands
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