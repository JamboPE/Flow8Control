import os
import sys
import lowcut as lowc

def help():
    print("""
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
    """)

def deskControl(channel, command, value):
    if channel < 8:
        if command in range(1,5):
            value = (value+15)*4.2333
        elif command in [7,14,15,16,17]: # Fader level
            value = (value+70)*1.5875
        elif command == 10: # Balance
            value = (value*64)+64
            if value > 127:
                value = 127
        elif command == 8:
            value = (value+20)*1.5875
        elif command == 9: # Lowcut
            value = lowc.getMidiValue(value)
    elif channel != 16: # buses
        if command == 7: # Fader level
            value = (value+70)*1.5875
        elif command == 8:
            value = 127 - round((-value)*4.2333)
            if value <= 0:
                value = 0
        elif command in range(11,20):
            value = (value+15)*4.2333
    if channel < 11:
        os.system('python3 midiutil/midiutil.py -d "FLOW 8" -w 0xB' + str(channel - 1) + ' ' + str(command) + ' ' + str(round(value)))
    else:
        channel -= 11
        hexCode = {
            0: "A",
            1: "B",
            2: "C",
            3: "D",
            4: "E",
            5: "F",
            6: "G",
        }
        channel = hexCode[channel]
        os.system('python3 midiutil/midiutil.py -d "FLOW 8" -w 0xB' + str(channel) + ' ' + str(command) + ' ' + str(round(value)))

if __name__ == "__main__":
    sys.argv.pop(0)
    if "-channel" in sys.argv:
        sys.argv[sys.argv.index("-channel")] = "-c"
    if "-bus" in sys.argv:
        sys.argv[sys.argv.index("-bus")] = "-b"
    if "-snapshot" in sys.argv:
        sys.argv[sys.argv.index("-snapshot")] = "-s"
    if "-reset" in sys.argv:
        sys.argv[sys.argv.index("-reset")] = "-r"
    if "-b" in sys.argv and "-c" in sys.argv and "-s" in sys.argv and "-r" in sys.argv:
        help()
        sys.exit(1)
    elif "-c" in sys.argv:
        try:
            channel = int(sys.argv[sys.argv.index("-c") + 1])
        except IndexError:
            print("Please provide a channel number")
            sys.exit(1)
        except ValueError:
            print("Invalid channel number")
            sys.exit(1)
        if channel < 1 or channel > 7:
            print("Channel number out of range (1-7)")
            sys.exit(1)
        
        if "-level" in sys.argv:
            try:
                level = float(sys.argv[sys.argv.index("-level") + 1])
            except IndexError:
                print("Please provide a level value")
                sys.exit(1)
            except ValueError:
                print("Invalid level value")
                sys.exit(1)
            if level < -70 or level > 10:
                print("Level value out of range (-70 to 10)")
                sys.exit(1)
            deskControl(channel, 7, level)

        if "-balance" in sys.argv:
            try:
                balance = float(sys.argv[sys.argv.index("-balance") + 1])
            except IndexError:
                print("Please provide a balance value")
                sys.exit(1)
            except ValueError:
                print("Invalid balance value")
                sys.exit(1)
            if balance < -1 or balance > 1:
                print("Level value out of range (-1 to 1)")
                sys.exit(1)
            deskControl(channel, 10, balance)

        if "-mute" in sys.argv:
            try:
                mute = str(sys.argv[sys.argv.index("-mute") + 1])
            except IndexError:
                print("Please provide a mute state")
                sys.exit(1)
            if mute != "on" and mute != "off":
                print("Mute value must be on or off")
                sys.exit(1)
            if mute == "on":
                mute = 1
            if mute == "off":
                mute = 0
            deskControl(channel, 5, mute)

        if "-solo" in sys.argv:
            try:
                solo = str(sys.argv[sys.argv.index("-solo") + 1])
            except IndexError:
                print("Please provide a solo state")
                sys.exit(1)
            if solo != "on" and solo != "off":
                print("Solo value must be on or off")
                sys.exit(1)
            if solo == "on":
                solo = 1
            if solo == "off":
                solo = 0
            deskControl(channel, 6, solo)

        if "-EQ" in sys.argv:
            try:
                band = int(sys.argv[sys.argv.index("-EQ") + 1])
                level = float(sys.argv[sys.argv.index("-EQ") + 2])
            except IndexError:
                print("Please provide a band and level value")
                sys.exit(1)
            except ValueError:
                print("Invalid band or level value")
                sys.exit(1)
            if band < 1 or band > 4:
                print("Band value out of range (1 to 4)")
                sys.exit(1)
            if level < -15 or level > 15:
                print("Level value out of range (-15 to 15)")
                sys.exit(1)
            deskControl(channel, band, level)

        if "-gain" in sys.argv:
            if channel == 7:
                print("Channel 7 does not have a gain control")
                sys.exit(1)
            try:
                gain = float(sys.argv[sys.argv.index("-gain") + 1])
            except IndexError:
                print("Please provide a gain value")
                sys.exit(1)
            except ValueError:
                print("Invalid gain value")
                sys.exit(1)
            if gain < -20 or gain > 60:
                print("Gain value out of range (-20 to 60)")
                sys.exit(1)
            deskControl(channel, 8, gain)
        
        if "-lowcut" in sys.argv:
            if channel == 7:
                print("Channel 7 does not have a lowcut control")
                sys.exit(1)
            try:
                lowcut = float(sys.argv[sys.argv.index("-lowcut") + 1])
            except IndexError:
                print("Please provide a lowcut frequency")
                sys.exit(1)
            except ValueError:
                print("Invalid lowcut frequency")
                sys.exit(1)
            if lowcut < 20 or lowcut > 600:
                print("Lowcut frequency out of range (20 to 600)")
                sys.exit(1)
            deskControl(channel, 9, lowcut)
        
        if "-comp" in sys.argv:
            if channel == 7:
                print("Channel 7 does not have a compressor control")
                sys.exit(1)
            try:
                comp = float(sys.argv[sys.argv.index("-comp") + 1])
            except IndexError:
                print("Please provide a compressor value")
                sys.exit(1)
            except ValueError:
                print("Invalid compressor value")
                sys.exit(1)
            if comp < 0 or comp > 100:
                print("Compressor value out of range (0 to 100)")
                sys.exit(1)
            deskControl(channel, 11, comp)

        if "-phantom" in sys.argv:
            if channel not in [1,2]:
                print("Phantom power is only available on channels 1 and 2")
                sys.exit(1)
            try:
                ph = str(sys.argv[sys.argv.index("-phantom") + 1])
            except IndexError:
                print("Please provide a phantom power state")
                sys.exit(1)
            if ph != "on" and ph != "off":
                print("Phantom power value must be on or off")
                sys.exit(1)
            if ph == "on":
                ph = 1
            if ph == "off":
                ph = 0
            deskControl(channel, 12, ph)

        if "-mon1" in sys.argv:
            try:
                level = float(sys.argv[sys.argv.index("-mon1") + 1])
            except IndexError:
                print("Please provide a monitor 1 send value")
                sys.exit(1)
            except ValueError:
                print("Invalid monitor 1 send value")
                sys.exit(1)
            if level < -70 or level > 10:
                print("Send value out of range (-70 to 10)")
                sys.exit(1)
            deskControl(channel, 14, level)

        if "-mon2" in sys.argv:
            try:
                level = float(sys.argv[sys.argv.index("-mon2") + 1])
            except IndexError:
                print("Please provide a monitor 2 send value")
                sys.exit(1)
            except ValueError:
                print("Invalid monitor 2 send value")
                sys.exit(1)
            if level < -70 or level > 10:
                print("Send value out of range (-70 to 10)")
                sys.exit(1)
            deskControl(channel, 15, level)

        if "-fx1" in sys.argv:
            try:
                level = float(sys.argv[sys.argv.index("-fx1") + 1])
            except IndexError:
                print("Please provide an FX 1 send value")
                sys.exit(1)
            except ValueError:
                print("Invalid FX 1 send value")
                sys.exit(1)
            if level < -70 or level > 10:
                print("Send value out of range (-70 to 10)")
                sys.exit(1)
            deskControl(channel, 16, level)

        if "-fx2" in sys.argv:
            try:
                level = float(sys.argv[sys.argv.index("-fx2") + 1])
            except IndexError:
                print("Please provide an FX 2 send value")
                sys.exit(1)
            except ValueError:
                print("Invalid FX 2 send value")
                sys.exit(1)
            if level < -70 or level > 10:
                print("Send value out of range (-70 to 10)")
                sys.exit(1)
            deskControl(channel, 17, level)

    elif "-b" in sys.argv:
        try:
            bus = str(sys.argv[sys.argv.index("-b") + 1])
        except IndexError:
            print("Please provide bus name")
            sys.exit(1)
        except ValueError:
            print("Invalid bus name")
            sys.exit(1)
        if bus not in ["LR","Mon1","Mon2","FX1","FX2"]:
            print("Bus name not valid (LR, Mon1, Mon2, FX1, FX2)")
            sys.exit(1)

        if bus == "LR":
            channel = 8
        elif bus == "Mon1":
            channel = 9
        elif bus == "Mon2":
            channel = 10
        elif bus == "FX1":
            channel = 11
        elif bus == "FX2":
            channel = 12

        if "-level" in sys.argv:
            try:
                level = float(sys.argv[sys.argv.index("-level") + 1])
            except IndexError:
                print("Please provide a level value")
                sys.exit(1)
            except ValueError:
                print("Invalid level value")
                sys.exit(1)
            if level < -70 or level > 10:
                print("Level value out of range (-70 to 10)")
                sys.exit(1)
            deskControl(channel, 7, level)

        if "-balance" in sys.argv:
            if channel != 8:
                print("Balance control only available on main LR bus")
                sys.exit(1)
            try:
                balance = float(sys.argv[sys.argv.index("-balance") + 1])
            except IndexError:
                print("Please provide a balance value")
                sys.exit(1)
            except ValueError:
                print("Invalid balance value")
                sys.exit(1)
            if balance < -1 or balance > 1:
                print("Level value out of range (-1 to 1)")
                sys.exit(1)
            deskControl(channel, 10, balance)

        if "-limiter" in sys.argv:
            if channel in range(11,13):
                print("Limiter control not available on FX buses")
                sys.exit(1)
            try:
                limiter = float(sys.argv[sys.argv.index("-limiter") + 1])
            except IndexError:
                print("Please provide a limiter value")
                sys.exit(1)
            except ValueError:
                print("Invalid limiter value")
                sys.exit(1)
            if limiter < -30 or limiter > 0:
                print("Limiter value out of range (-30 to 0)")
                sys.exit(1)
            deskControl(channel, 8, limiter)

        if "-EQ" in sys.argv:
            if channel not in range(8,11):
                print("EQ control not available on FX buses")
                sys.exit(1)
            try:
                band = int(sys.argv[sys.argv.index("-EQ") + 1])
                level = float(sys.argv[sys.argv.index("-EQ") + 2])
            except IndexError:
                print("Please provide a band and level value")
                sys.exit(1)
            except ValueError:
                print("Invalid band or level value")
                sys.exit(1)
            if band < 1 or band > 9:
                print("Band value out of range (1 to 9)")
                sys.exit(1)
            if level < -15 or level > 15:
                print("Level value out of range (-15 to 15)")
                sys.exit(1)
            nineBandEQ = {
                1: 11,
                2: 12,
                3: 13,
                4: 14,
                5: 15,
                6: 16,
                7: 17,
                8: 18,
                9: 19
            }
            deskControl(channel, nineBandEQ[band], level)

        if "-effect" in sys.argv:
            if channel not in range(11,13):
                print("Effect control only available on FX buses")
                sys.exit(1)
            try:
                effect = int(sys.argv[sys.argv.index("-effect") + 1])
            except IndexError:
                print("Please provide an effect preset")
                sys.exit(1)
            except ValueError:
                print("Invalid effect preset")
                sys.exit(1)
            if effect < 1 or effect > 16:
                print("Effect preset out of range (1 to 16)")
                sys.exit(1)
            if channel == 11:
                os.system('python3 midiutil/midiutil.py -d "FLOW 8" -w 0xCD '+str(effect))
            elif channel == 12:
                os.system('python3 midiutil/midiutil.py -d "FLOW 8" -w 0xCE '+str(effect))

        if "-fxmute" in sys.argv:
            if channel not in range(11,13):
                print("FX mute control only available on FX buses")
                sys.exit(1)
            try:
                fxmute = str(sys.argv[sys.argv.index("-fxmute") + 1])
            except IndexError:
                print("Please provide an FX mute state")
                sys.exit(1)
            if fxmute != "on" and fxmute != "off":
                print("FX mute value must be on or off")
                sys.exit(1)
            elif fxmute == "on":
                fxmute = 1
            elif fxmute == "off":
                fxmute = 0
            deskControl(16, 1, fxmute)

        if "-intensity" in sys.argv:
            if channel not in range(11,13):
                print("Intensity control only available on FX buses")
                sys.exit(1)
            try:
                intensity = float(sys.argv[sys.argv.index("-intensity") + 1])
            except IndexError:
                print("Please provide an intensity value")
                sys.exit(1)
            except ValueError:
                print("Invalid intensity value")
                sys.exit(1)
            if intensity < 0 or intensity > 100:
                print("Intensity value out of range (0 to 100)")
                sys.exit(1)
            if channel == 11:
                channel = 14
            elif channel == 12:
                channel = 15
            deskControl(channel, 1, intensity)

        if "-fxoption" in sys.argv:
            if channel not in range(11,13):
                print("Option control only available on FX buses")
                sys.exit(1)
            try:
                option = int(sys.argv[sys.argv.index("-fxoption") + 1])
            except IndexError:
                print("Please provide an option value")
                sys.exit(1)
            except ValueError:
                print("Invalid option value")
                sys.exit(1)
            if option < 1 or option > 2:
                print("Option value out of range (1 or 2)")
                sys.exit(1)
            if channel == 11:
                channel = 14
            elif channel == 12:
                channel = 15
            deskControl(channel, 2, option-1)

    if "-s" in sys.argv:
        try:
            snapshot = int(sys.argv[sys.argv.index("-s") + 1])
        except IndexError:
            print("Please provide a snapshot number")
            sys.exit(1)
        except ValueError:
            print("Invalid snapshot number")
            sys.exit(1)
        if snapshot < 1 or snapshot > 15:
            print("Snapshot number out of range (1 to 15)")
            sys.exit(1)
        os.system('python3 midiutil/midiutil.py -d "FLOW 8" -w 0xCF '+str(snapshot))
    
    if "-r" in sys.argv:
        os.system('python3 midiutil/midiutil.py -d "FLOW 8" -w 0xCF 16')

    else:
        help()