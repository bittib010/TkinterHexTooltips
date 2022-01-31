windowsNTFSVBR = {0: ['E8 52 90 ',
                      'Jump code (short jump, offset, NOP: 0xEB 0x52 0x90)'],
                  1: ['4E 54 46 53 20 20 20 20 ',
                      'OEM name ("NTFS")'],
                  2: ['00 02 ',
                      'Bytes per sector (512 = 0x0200)\nThis section also marks the start of the Bios Parameter Block'
                      'which ends right before the Bootstrap code starts.'],
                  3: ['08 ',
                      'Sectors per cluster (0x08)'],
                  4: ['00 00\n00 00 00 00 00 ',
                      'Must be zeros to distinguish NTFS from FAT. The two first bytes are considered reserved.'
                      'The next three bytes are always zero and the last two are unused.'],
                  5: ['F8 ',
                      'Media descriptor (0xF8)'],
                  6: ['00 00 ',
                      'Must be zeros.'],
                  7: ['3f 00 ',
                      'Sectors per track.'],
                  8: ['FF 00 ',
                      'Number of heads (probably 0xFF).'],
                  9: ['00 A8 03 00\n',
                      'Hidden sectors (sectors before the partition)'],
                  10: ['00 00 00 00 ',
                       'Must be zeros'],
                  11: ['80 00 80 00 ',
                       'Signature (0x80 0x00 0x80 0x00).'],
                  12: ['75 8C 24 4A 00 00 00 00\n',
                       'Total sectors in volume.'],
                  13: ['00 00 0C 00 00 00 00 00 ',
                       '$MFT cluster number.\nStarting logical cluster number for MFT'],
                  14: ['02 00 00 00 00 00 00 00\n',
                       '$MFTMirr cluster number.\nStarting logical cluster number for MFT mirror.'],
                  15: ['F6 00 00 00 ',
                       'Clusters per file record segment (see text for interpretation).'],
                  16: ['01 ',
                       'Clusters per index buffer/index block (1)'],
                  17: ['00 00 00 ',
                       'Must be zeros.'],
                  18: ['BA 53 DF 78 78 DF 78 D8\n',
                       'Volume serial number.'],
                  19: ['00 00 00 00 ',
                       'Currently unused checksum value.'],
                  20: [
                      'FA 33 C0 8E D0 BC 00 7C FB 68 C0 07\n'
                      '1F 1E 68 66 00 CB 88 16 0E 00 66 81 3E 03 00 4E\n'
                      '54 46 53 75 15 B4 41 BB AA 55 CD 13 72 0C 81 FB\n'
                      '55 AA 75 06 F7 C1 01 00 75 03 E9 DD 00 1E 83 EC\n'
                      '18 68 1A 00 B4 48 8A 16 0E 00 8B F4 16 1F CD 13\n'
                      '9F 83 C4 18 9E 58 1F 72 E1 3B 06 0B 00 75 DB A3\n'
                      '0F 00 C1 2E 0F 00 04 1E 5A 33 DB B9 00 20 2B C8\n'
                      '66 FF 06 11 00 03 16 0F 00 8E C2 FF 06 16 00 E8\n'
                      '4B 00 2B C8 77 EF B8 00 BB CD 1A 66 23 C0 75 2D\n'
                      '66 81 FB 54 43 50 41 75 24 81 F9 02 01 72 1E 16\n'
                      '68 07 BB 16 68 52 11 16 68 09 00 66 53 66 53 66\n'
                      '55 16 16 16 68 B8 01 66 61 0E 07 CD 1A 33 C0 BF\n'
                      '0A 13 B9 F6 0C FC F3 AA E9 FE 01 90 90 66 60 1E\n'
                      '06 66 A1 11 00 66 03 06 1C 00 1E 66 68 00 00 00\n'
                      '00 66 50 06 53 68 01 00 68 10 00 B4 42 8A 16 0E\n'
                      '00 16 1F 8B F4 CD 13 66 59 5B 5A 66 59 66 59 1F\n'
                      '0F 82 16 00 66 FF 06 11 00 03 16 0F 00 8E C2 FF\n'
                      '0E 16 00 75 BC 07 1F 66 61 C3 A1 F6 01 E8 09 00\n'
                      'A1 FA 01 E8 03 00 F4 EB FD 8B F0 AC 3C 00 74 09\n'
                      'B4 0E BB 07 00 CD 10 EB F2 C3 0D 0A 41 20 64 69\n'
                      '73 6B 20 72 65 61 64 20 65 72 72 6F 72 20 6F 63\n'
                      '63 75 72 72 65 64 00 0D 0A 42 4F 4F 54 4D 47 52\n'
                      '20 69 73 20 63 6F 6D 70 72 65 73 73 65 64 00 0D\n'
                      '0A 50 72 65 73 73 20 43 74 72 6C 2B 41 6C 74 2B\n'
                      '44 65 6C 20 74 6F 20 72 65 73 74 61 72 74 0D 0A\n'
                      '00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n'
                      '00 00 00 00 00 00 8A 01 A7 01 BF 01 00 00 ''',
                      'Bootstrap code.'],
                  21: ['55 AA',
                       'Signature (0x55 0xAA).']}

windowsNTFSVBRInfo = '''Volume Boot Record - VBR
'''

windowsNTFSMFTFileRecord = {1: ['46 49 4C 45 ',
                                'Signature. It must be "FILE".'],
                            2: ['30 00 ',
                                'Offset to the update sequence.'],
                            3: ['03 00 ',
                                'Update sequence size in words.'],
                            4: ['FA 6A 32 61 00 00 00 00\n',
                                '$LogFile Sequence Number (LSN).'],
                            5: ['01 00 ',
                                'Sequence Number.'],
                            6: ['01 00 ',
                                'Hard link count'],
                            7: ['38 00 ',
                                'Offset to the first attribute.'],
                            8: ['01 00 ',
                                'Flags: In use, Directory. Here, the "directory flag" flag is set.'],
                            9: ['B0 01 00 00 ',
                                'Real size of the FILE record.'],
                            10: ['00 04 00 00\n',
                                 'Allocated size of the FILE record.'],
                            11: ['00 00 00 00 00 00 00 00 ',
                                 'Base FILE record.'],
                            12: ['07 00 ',
                                 'Next attribute ID.'],
                            13: ['00 00 ',
                                 'N/A ???, or part of the previous - Next Attribute ID?'],
                            14: ['00 00 00 00\n',
                                 'ID of this record.'],
                            15: ['F2 00 ',
                                 'Update Sequence number'],
                            16: ['00 00 00 00 ',
                                 'Update Sequence Array.'],
                            17: ['00 00 ',
                                 'N/A???'],
                            18: ['10 00 00 00 ',
                                 'Attribute $10\n'
                                 'Attribute Type.\n'],
                            19: ['60 00 00 00\n',
                                 'Attribute $10\n'
                                 'Attribute Length (including header)'],
                            20: ['00 ',
                                 'Attribute $10\n'
                                 'Non-resident flag'],
                            21: ['00 ',
                                 'Attribute $10\n'
                                 'Name length'],
                            22: ['18 00 ',
                                 'Attribute $10\n'
                                 'Name offset'],
                            23: ['00 00 ',
                                 'Attribute $10\n'
                                 'Flags: compressed, encrypted, sparse.'],
                            24: ['00 00 ',
                                 'Attribute $10\n'
                                 'Attribute ID'],
                            25: ['48 00 00 00 ',
                                 'Attribute $10\n'
                                 'Length of the attribute'],
                            26: ['18 00 ',
                                 'Attribute $10\n'
                                 'Offset to the attribute data.'],
                            27: ['00 ',
                                 'Attribute $10\n'
                                 'Indexed flag'],
                            28: ['00\n',
                                 'Attribute $10\n'
                                 'Padding'],
                            29: ['09 C1 A7 DE D5 AC D5 01 ',
                                 'Attribute $10 - $STANDARD_INFORMATION\n'
                                 'File Created (UTC). Add the calculations here.'],
                            30: ['09 C1 A7 DE D5 AC D5 01\n',
                                 'Attribute $10 - $STANDARD_INFORMATION\n'
                                 'File Modified (UTC)'],
                            31: ['09 C1 A7 DE D5 AC D5 01 ',
                                 'Attribute $10 - $STANDARD_INFORMATION\n'
                                 'Record Changed (UTC)'],
                            32: ['09 C1 A7 DE D5 AC D5 01\n',
                                 'Attribute $10 - $STANDARD_INFORMATION\n'
                                 'Last Time Accessed (UTC)'],
                            33: ['06 00 00 00 ',
                                 'Attribute $10 - $STANDARD_INFORMATION\n'
                                 'File Permissions: Read only, hidden, system, archive, device, normal, temporary, '
                                 'sparse file, '
                                 'reparse point, compressed, offline, not content indexed, encrypted.'],
                            34: ['00 00 00 00 ',
                                 'Attribute $10 - $STANDARD_INFORMATION\n'
                                 'Maximum number of versions'],
                            35: ['00 00 00 00 ',
                                 'Attribute $10 - $STANDARD_INFORMATION\n'
                                 'Verssion number'],
                            36: ['00 00 00 00\n',
                                 'Attribute $10 - $STANDARD_INFORMATION\n'
                                 'Class ID.'],
                            37: ['00 00 00 00 ',
                                 'Attribute $10 - $STANDARD_INFORMATION\n'
                                 'Owner ID.'],
                            38: ['00 01 00 00 ',
                                 'Attribute $10 - $STANDARD_INFORMATION\n'
                                 'Security ID'],
                            39: ['00 00 00 00 00 00 00 00\n',
                                 'Attribute $10 - $STANDARD_INFORMATION\n'
                                 'Quota charged.'],
                            40: ['00 00 00 00 00 00 00 00 ',
                                 'Attribute $10 - $STANDARD_INFORMATION\n'
                                 'Update Sequence Number'],
                            41: ['30 00 00 00 ',
                                 'Attribute $30\n'
                                 'Attribute type'
                                 'This marks the beginning of Attribute $30'],
                            42: ['68 00 00 00\n',
                                 'Attribute $30\n'
                                 'Length (including header)'],
                            43: ['00 ',
                                 'Attribute $30\nNon-resident flag'],
                            44: ['00 ',
                                 'Attribute $30\nName Length'],
                            45: ['18 00 ',
                                 'Attribute $30\nName offset'],
                            46: ['00 00 ',
                                 'Attribute $30\n'
                                 'Flags: compressed, encrypted, sparse.'],
                            47: ['03 00 ',
                                 'Attribute $30\n'
                                 'Attribute ID'],
                            48: ['4a 00 00 00 ',
                                 'Attribute $30\n'
                                 'Length of the attribute'],
                            49: ['18 00 ',
                                 'Attribute $30\n'
                                 'Offset to the attribute data.'],
                            50: ['01 ',
                                 'Attribute $30\n'
                                 'Indexed flag.'],
                            51: ['00\n',
                                 'Attribute $30\n'
                                 'Padding'],
                            52: ['05 00 00 00 00 00 ',
                                 'Attribute $30 - $FILE_NAME\n'
                                 'Parent directory file record number'],
                            53: ['05 00 ',
                                 'Attribute $30 - $FILE_NAME\n'
                                 'Parent directory sequence number'],
                            55: ['09 C1 A7 DE D5 AC D5 01\n',
                                 'Attribute $30 - $FILE_NAME\n'
                                 'File Created (UTC)'],
                            56: ['09 C1 A7 DE D5 AC D5 01 ',
                                 'Attribute $30 - $FILE_NAME\n'
                                 'File Modified (UTC)'],
                            57: ['09 C1 A7 DE D5 AC D5 01\n',
                                 'Attribute $30 - $FILE_NAME\n'
                                 'Record Changed (UTC)'],
                            58: ['09 C1 A7 DE D5 AC D5 01 ',
                                 'Attribute $30 - $FILE_NAME\n'
                                 'Last Access Time (UTC)'],
                            59: ['00 40 00 00 00 00 00 00\n',
                                 'Attribute $30 - $FILE_NAME\n'
                                 'Allocated Size. Value = 16 384'],
                            60: ['00 40 00 00 00 00 00 00 ',
                                 'Attribute $30 - $FILE_NAME\n'
                                 'Real Size. Value = 16 384'],
                            61: ['06 00 00 00 ',
                                 'Attribute $30 - $FILE_NAME\n'
                                 'File attributes: read-only, hidden, system, archive, device, normal, temporary,'
                                 'sparse file, reparse poine, compressed, offline, not content indexed,'
                                 'encrypted, directory, index view.'],
                            62: ['00 00 00 00\n',
                                 'Attribute $30 - $FILE_NAME\n'
                                 '(Used by EAs and reparse)'],
                            63: ['04 ',
                                 'Attribute $30 - $FILE_NAME\n'
                                 'File name length.'],
                            64: ['03 ',
                                 'Attribute $30 - $FILE_NAME\n'
                                 'File name namespace'],
                            65: ['24 00 4D 00 46 00 54 00 ',
                                 'Attribute $30 - $FILE_NAME\n'
                                 'File name: Value = "$MFT".'],
                            66: ['00 00 00 00 00 00\n',
                                 'Attribute $30\n What does this belong to?'],
                            67: ['80 00 00 00 ',
                                 'Attribute $80\n'
                                 'Attribute type.'],
                            68: ['60 00 00 00 ',
                                 'Attribute $80\n'
                                 'Length (Including Header)'],
                            69: ['01 ',
                                 'Attribute $80\n'
                                 'Non-resident flag'],
                            70: ['00 ',
                                 'Attribute $80\n'
                                 'Name Length.'],
                            71: ['40 00 ',
                                 'Attribute $80\n'
                                 'Name offset.'],
                            72: ['00 00 ',
                                 'Attribute $80\n'
                                 'Flags: compressed, encrypted and parsed.'],
                            73: ['06 00\n',
                                 'Attribute $80\n'
                                 'Attribute ID. Value = 6.'],
                            74: ['00 00 00 00 00 00 00 00 ',
                                 'Attribute $80\n'
                                 'First VCN. Value = 0.'],
                            75: ['FF 81 01 00 00 00 00 00\n',
                                 'Attribute $80\n'
                                 'Last VCN. Value = 98,815.'],
                            76: ['40 00 ',
                                 'Attribute $80\n'
                                 'Data runs offset.'],
                            77: ['00 00 ',
                                 'Attribute $80\n'
                                 'Compression unit size.'],
                            78: ['00 00 00 00 ',
                                 'Attribute $80\n'
                                 'Padding'],
                            79: ['00 00 20 18 00 00 00 00\n',
                                 'Attribute $80\n'
                                 'Allocated size. Value = 404,750,336.'],
                            80: ['00 00 20 18 00 00 00 00 ',
                                 'Attribute $80\n'
                                 'Real Size. Value = 404,750,336.'],
                            81: ['00 00 20 18 00 00 00 00\n',
                                 'Attribute $80\n'
                                 'Initialized size. Value = 404,750,336.'],
                            82: ['32 ',
                                 'Attribute $80 - $DATA - Data run\n'
                                 'Size'],
                            83: ['00 71 ',
                                 'Attribute $80 - $DATA - Data run\n'
                                 'Cluster count. Value = 28,928.'],
                            84: ['00 00 0C ',
                                 'Attribute $80 - $DATA - Data run\n'
                                 'First Cluster. Value = 786,432.'],

                            85: ['41 ',
                                 'Attribute $80 - $DATA - Data run\n'
                                 'Size'],
                            86: ['42 ',
                                 'Attribute $80 - $DATA - Data run\n'
                                 'Cluster count. Value = 66.'],
                            87: ['77 9B B7 00 ',
                                 'Attribute $80 - $DATA - Data run\n'
                                 'First Cluster. Value = 12,819,319.'],

                            88: ['33 ',
                                 'Attribute $80 - $DATA - Data run\n'
                                 'Size'],
                            89: ['FE 8E 00\n',
                                 'Attribute $80 - $DATA - Data run\n'
                                 'Cluster count. Value = 36,606.'],
                            90: ['C3 08 07 ',
                                 'Attribute $80 - $DATA - Data run\n'
                                 'First Cluster. Value = 13,280,314.'],

                            91: ['43 ',
                                 'Attribute $80 - $DATA - Data run\n'
                                 'Size'],
                            92: ['C0 81 00 ',
                                 'Attribute $80 - $DATA - Data run\n'
                                 'Cluster count. Value = 33,216.'],
                            93: ['F0 D5 C9 00 ',
                                 'Attribute $80 - $DATA - Data run\n'
                                 'First Cluster. Value = 26,507,818.'],
                            1131: ['00 00 00 00 00\n',
                                   'Attribute $80\n'
                                   'Padding???'],
                            94: ['B0 00 00 00 ',
                                 'Attribute $B0\n'
                                 'Attribute type.'],
                            95: ['48 00 00 00 ',
                                 'Attribute $B0\n'
                                 'Length (including header).'],
                            96: ['01 ',
                                 'Attribute $B0\n'
                                 'Non-resident flag.'],
                            97: ['00 ',
                                 'Attribute $B0\n'
                                 'Name length.'],
                            98: ['40 00 ',
                                 'Attribute $B0\n'
                                 'Name offset.'],
                            99: ['00 00 ',
                                 'Attribute $B0\n'
                                 'Flags: compressed, encrypted, sparse.'],
                            100: ['05 00\n',
                                  'Attribute $B0\n'
                                  'Attribute ID.'],
                            101: ['00 00 00 00 00 00 00 00 ',
                                  'Attribute $B0\n'
                                  'First VCN. Value = 0.'],
                            102: ['0D 00 00 00 00 00 00 00\n',
                                  'Attribute $B0\n'
                                  'Last VCN. Value = 13'],
                            103: ['40 00 ',
                                  'Attribute $B0\n'
                                  'Data runs offset.'],
                            104: ['00 00 ',
                                  'Attribute $B0\n'
                                  'Compression unit size.'],
                            105: ['00 00 00 00 ',
                                  'Attribute $B0\n'
                                  'Padding.'],
                            106: ['00 E0 00 00 00 00 00 00\n',
                                  'Attribute $B0\n'
                                  'Allocated size. Value = 57,344.'],
                            107: ['08 D0 00 00 00 00 00 00 ',
                                  'Attribute $B0\n'
                                  'Real size. Value = 53,256.'],
                            108: ['08 D0 00 00 00 00 00 00\n',
                                  'Attribute $B0\n'
                                  'Initialized size. Value = 53,256.'],
                            109: ['31 ',
                                  'Attribute $B0 - $BITMAP - Data run\n'
                                  'Size.'],
                            110: ['0E ',
                                  'Attribute $B0 - $BITMAP - Data run\n'
                                  'Cluster count. Value = 14'],
                            111: ['0C 4F 01 ',
                                  'Attribute $B0 - $BITMAP - Data run\n'
                                  'First cluster. Value = 85,772.'],
                            112: ['00 00 00 ',
                                  'Attribute $B0 - $BITMAP - Data run\n'
                                  'Padding???'],
                            113: ['FF FF FF FF',
                                  'End marker.']



                            }

windowsNTFSMFTInfo = '''Master File Table (MFT) Info
Understanding the MFT is crucial to achieve a fully good understanding of NTFS. Every file or direcroty has at least one
entry in the MFT.


https://docs.microsoft.com/en-us/windows/win32/devnotes/master-file-table'''

template = {0: ['', ''],
            1: ['',
                ''],
            2: ['',
                ''],
            3: ['',
                ''],
            4: ['',
                ''],
            5: ['',
                ''],
            6: ['',
                ''],
            7: ['',
                ''],
            8: ['',
                '']}
