# Voice-code-Access-Authentication-System

Security Voice-code Access is a software component designed to provide secure access control based on voice recognition using fingerprint and spectrogram concepts. The software can be trained on 8 individuals and operates in two modes:

## Modes of Operation:

### Mode 1 – Security Voice Code:
In this mode, access is granted only if a specific pass-code sentence is spoken. The following three sentences are considered valid passcodes:
1. "Open middle door"
2. "Unlock the gate"
3. "Grant me access"

### Mode 2 – Security Voice Fingerprint:
In this mode, access is granted to specific individual(s) who say the valid pass-code sentence. The user can select which individual(s) of the original 8 users are granted access. Access can be granted to one or more individuals.

## User Interface:

The UI provides the following elements:

- **Record Button:** Start recording the voice-code.
- **Spectrogram Viewer:** Visualize the spectrogram of the spoken voice-code.
- **Analysis Results Summary:** Display two tables:
  - Table 1: Shows how much the spoken sentence matches each of the saved three passcode sentences.
  - Table 2: Shows how much the spoken voice matches each of the 8 saved individuals.
- **Access Status Indicator:** Indicates the result of the algorithm, displaying either "Access Gained" or "Access Denied".

## Usage:

1. **Mode Selection:** Choose between Mode 1 (Security Voice Code) or Mode 2 (Security Voice Fingerprint).
2. **Passcode Entry:** Speak one of the valid passcode sentences for Mode 1.
3. **Individual Selection:** Select the individual(s) for whom access is to be granted in Mode 2.
4. **Recording:** Click on the record button to start recording the voice-code.
5. **Analysis:** View the spectrogram and analysis results to determine access status.
6. **Access Status:** Check the access status indicator for "Access Gained" or "Access Denied" based on the analysis.
