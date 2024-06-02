#!/usr/bin/env python3

import argparse
import os
import signal
import sys
import time

import rtmidi


def signal_handler(signal, frame):
    """Handler for Ctrl-C"""
    sys.exit(0)


def midi_in_callback(value, args):
    """Function called when MIDI data is received"""
    data = value[0]
    if args.hex:
        print('[' + ', '.join('0x%02X' % x for x in data) + ']')
    else:
        print(data)


def get_port(client, device_id):
    """Return open port for a device"""
    try:
        # Try to parse device id as number first
        dev_id = int(device_id)
        if not dev_id < len(client.get_ports()):
            raise Exception('Device id out of range')
    except ValueError:
        # If this fails, try to find a port name starting with it
        for i, name in enumerate(client.get_ports()):
            if name.lower().startswith(device_id.lower()):
                return client.open_port(i)
        # If this also fails, try to find a port name that contains
        # a substring of it
        for i, name in enumerate(client.get_ports()):
            if device_id.lower() in name.lower():
                return client.open_port(i)
        raise Exception('Device "%s" not found' % device_id)

    return client.open_port(dev_id)


def main():
    if len(sys.argv) < 2:
        # Show help when no arguments are given
        sys.argv.append('-h')

    # Setup command line parser
    parser = argparse.ArgumentParser(description='MIDI utility')
    parser.add_argument('-l', '--list', action='store_true',
                        help='List connected devices')
    parser.add_argument('-d', '--device', metavar='ID',
                        help='Selected device')
    parser.add_argument('-w', '--write', type=str, nargs='+', metavar='DATA',
                        help='Write data')
    parser.add_argument('-r', '--read', action='store_true',
                        help='Read data')
    parser.add_argument('-x', '--hex', action='store_true',
                        help='Show/interprete data as hex')
    parser.add_argument('-s', '--sysex-file', metavar='FILE',
                        help='Sysex file to transmit')
    args = parser.parse_args()

    try:
        if args.list:
            # List command, show all connected devices
            print()
            print('Available ports:')
            print()
            print('\tInput:')
            print('\t', 'ID', 'Name', sep='\t')
            for i, name in enumerate(rtmidi.MidiIn().get_ports()):
                print('\t', i, name, sep='\t')
            print()
            print('\tOutput:')
            print('\t', 'ID', 'Name', sep='\t')
            for i, name in enumerate(rtmidi.MidiOut().get_ports()):
                print('\t', i, name, sep='\t')
            print()

        elif args.write:
            # Write command, send data
            if not args.device:
                raise Exception('No device specified.')
            outport = get_port(rtmidi.MidiOut(), args.device)
            if args.hex:
                data = [int(x, 16) for x in args.write]
            else:
                data = [int(x, 0) for x in args.write]
            outport.send_message(data)
            del outport

        elif args.read:
            # Read command, receive data until Ctrl-C is pressed
            signal.signal(signal.SIGINT, signal_handler)
            if not args.device:
                raise Exception('No device specified.')
            inport = get_port(rtmidi.MidiIn(), args.device)
            inport.set_callback(midi_in_callback, args)
            inport.ignore_types(False, False, False)
            while True:
                time.sleep(1)

        elif args.sysex_file:
            # Send sysex file command
            if not args.device:
                raise Exception('No device specified.')
            outport = get_port(rtmidi.MidiOut(), args.device)
            file_path = args.sysex_file
            if not (os.path.exists(file_path) and os.path.isfile(file_path)):
                raise Exception('File "%s" does not exist.' % file_path)
            with open(file_path, "rb") as f:
                data = f.read()
                data_pos = 0
                while True:
                    sysex_start_pos = data.find(b"\xF0", data_pos)
                    sysex_end_pos = data.find(b"\xF7", data_pos)
                    if sysex_start_pos >= 0 and sysex_end_pos >= 0:
                        message = data[sysex_start_pos:sysex_end_pos + 1]
                        print("Sending sysex message with %i bytes." %
                              len(message))
                        outport.send_message(message)
                        time.sleep(0.05)
                        data_pos = sysex_end_pos + 1
                    else:
                        break

    except Exception as e:
        print('Error:', e)


if __name__ == '__main__':
    main()
