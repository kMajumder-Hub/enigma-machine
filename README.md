# enigma-machine
Interactive Enigma Machine simulator with rotor selection, step-by-step encryption visualization, and educational content. Built with Streamlit.

## 🚀 Live Demo

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://enigma-ww2.streamlit.app/)

**Try it now:** [https://enigma-ww2.streamlit.app/](https://enigma-ww2.streamlit.app/)

## ✨ Features

- 🔐 **Historical Enigma Simulation** - Three authentic rotors (I, II, III) with historical wirings
- ⚙️ **Rotor Order Selection** - Configure any combination of rotors in left, middle, and right positions
- 🔌 **Plugboard (Steckerbrett)** - Additional letter-pair substitutions for enhanced encryption
- 📊 **Step-by-Step Visualization** - Watch the signal path through each component in real-time
- 🎓 **Educational Content** - Learn how the Enigma machine worked and its historical significance
- 🔄 **Reciprocal Encryption** - Same settings encrypt AND decrypt messages
- 💻 **Intuitive UI** - User-friendly interface with clear instructions

## 🎯 How to Use

1. **Configure** your Enigma machine in the sidebar:
   - Select rotor order (Rotor I, II, or III for each position)
   - Set initial rotor positions (0-25)
   - Add plugboard pairs (optional, e.g., "AB,CD,EF")

2. **Encrypt** your message in the Encryption tab

3. **Share** the encrypted message and your initial settings

4. **Decrypt** by setting the same rotor configuration and pasting the encrypted message

## 🛠️ Local Installation

```bash
# Clone the repository
git clone https://github.com/kMajumder-Hub/enigma-machine.git
cd enigma-machine

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run enigma_app.py
```

## 📚 About the Enigma Machine

The Enigma machine was an encryption device used by Germany during World War II. Breaking the Enigma code was one of the greatest achievements of Allied cryptanalysis, with significant contributions from Alan Turing and the team at Bletchley Park.

This simulator demonstrates the core principles:
- **Rotors**: Mechanical wheels that scramble letters and rotate after each keypress
- **Reflector**: Sends the signal back through the rotors in reverse
- **Plugboard**: Additional layer of substitution encryption
- **Reciprocal Property**: The same settings that encrypt also decrypt

## 📝 License

MIT License - Feel free to use and modify!
