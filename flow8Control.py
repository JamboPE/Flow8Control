import os
import sys
import lowcut as lowc

#os.system('python3 midiutil/midiutil.py -d "FLOW 8" -w 0xB0 7 111') # Set channel 1 to 0dB
def deskControl(channel, command, value):
    if command in [7,14,15,16,17]: # Fader level
        value = (value+70)*1.5875
    if command == 10: # Balance
        value = (value*64)+64
        if value > 127:
            value = 127
    if command == 8: # Gain
        value = (value+20)*1.5875
    if command == 9: # Lowcut
        value = lowc.getMidiValue(value)
    os.system('python3 midiutil/midiutil.py -d "FLOW 8" -w 0xB' + str(channel - 1) + ' ' + str(command) + ' ' + str(round(value)))

# TYPE
# -c #ch 

if __name__ == "__main__":
    sys.argv.pop(0)
    if "-channel" in sys.argv:
        sys.argv[sys.argv.index("-channel")] = "-c"
    if "-c" in sys.argv:
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
                level = float(sys.argv[sys.argv.index("-l") + 1])
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
                balance = float(sys.argv[sys.argv.index("-b") + 1])
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
                mute = str(sys.argv[sys.argv.index("-m") + 1])
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
                solo = str(sys.argv[sys.argv.index("-s") + 1])
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

        ## ADD EQ CONTROL

        if "-gain" in sys.argv:
            if channel == 7:
                print("Channel 7 does not have a gain control")
                sys.exit(1)
            try:
                gain = float(sys.argv[sys.argv.index("-g") + 1])
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
                lowcut = float(sys.argv[sys.argv.index("-lc") + 1])
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

    else:
        print("""
        Usage: flow8Control.py -c [CHANNEL] [OPTIONS]
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
""")