import streamlit as st
import string

# Historical Enigma rotor wirings (I, II, III)
ROTOR_WIRINGS = {
    "Rotor I": "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
    "Rotor II": "AJDKSIRUXBLHWTMCQGZNPYFVOE",
    "Rotor III": "BDFHJLCPRTXVZNYEIWGAKMUSQO"
}

REFLECTOR = "YRUHQSLDPXNGOKMIEBFZCWVJAT"
ALPHABET = string.ascii_uppercase

class EnigmaRotor:
    def __init__(self, wiring, position=0):
        self.wiring = wiring
        self.position = position
        self.notch = 16  # Q for historical accuracy
    
    def step(self):
        self.position = (self.position + 1) % 26
        return self.position == self.notch
    
    def forward(self, char):
        if char not in ALPHABET:
            return char
        index = (ALPHABET.index(char) + self.position) % 26
        char = self.wiring[index]
        index = (ALPHABET.index(char) - self.position) % 26
        return ALPHABET[index]
    
    def backward(self, char):
        if char not in ALPHABET:
            return char
        index = (ALPHABET.index(char) + self.position) % 26
        char = ALPHABET[self.wiring.index(ALPHABET[index])]
        index = (ALPHABET.index(char) - self.position) % 26
        return ALPHABET[index]

class EnigmaMachine:
    def __init__(self, rotor_types, rotor_positions, plugboard_pairs=""):
        self.rotors = [
            EnigmaRotor(ROTOR_WIRINGS[rotor_types[0]], rotor_positions[0]),
            EnigmaRotor(ROTOR_WIRINGS[rotor_types[1]], rotor_positions[1]),
            EnigmaRotor(ROTOR_WIRINGS[rotor_types[2]], rotor_positions[2])
        ]
        self.plugboard = self._create_plugboard(plugboard_pairs)
        self.reflector = REFLECTOR
    
    def _create_plugboard(self, pairs):
        plugboard = {char: char for char in ALPHABET}
        if pairs:
            for pair in pairs.split(','):
                pair = pair.strip().upper()
                if len(pair) == 2 and pair[0] in ALPHABET and pair[1] in ALPHABET:
                    plugboard[pair[0]] = pair[1]
                    plugboard[pair[1]] = pair[0]
        return plugboard
    
    def _step_rotors(self):
        if self.rotors[1].step():
            self.rotors[0].step()
        elif self.rotors[2].position == self.rotors[2].notch - 1:
            self.rotors[1].step()
            self.rotors[0].step()
        self.rotors[2].step()
    
    def encrypt_char(self, char):
        if char not in ALPHABET:
            return char
        
        self._step_rotors()
        
        # Through plugboard
        char = self.plugboard.get(char, char)
        
        # Forward through rotors
        char = self.rotors[2].forward(char)
        char = self.rotors[1].forward(char)
        char = self.rotors[0].forward(char)
        
        # Through reflector
        char = self.reflector[ALPHABET.index(char)]
        
        # Backward through rotors
        char = self.rotors[0].backward(char)
        char = self.rotors[1].backward(char)
        char = self.rotors[2].backward(char)
        
        # Through plugboard again
        char = self.plugboard.get(char, char)
        
        return char
    
    def encrypt(self, text):
        return ''.join(self.encrypt_char(char.upper()) for char in text if char.upper() in ALPHABET)

def encrypt_with_steps(rotor_types, rotor_positions, plugboard_pairs, text):
    """Encrypt and return detailed step-by-step information"""
    enigma = EnigmaMachine(rotor_types, rotor_positions, plugboard_pairs)
    steps = []
    
    for char in text.upper():
        if char not in ALPHABET:
            continue
            
        # Record positions before stepping
        positions_before = [r.position for r in enigma.rotors]
        
        # Step rotors
        enigma._step_rotors()
        
        # Record positions after stepping
        positions_after = [r.position for r in enigma.rotors]
        
        # Track transformation
        step_detail = {
            'input': char,
            'positions_before': positions_before,
            'positions_after': positions_after,
            'transformations': []
        }
        
        # Plugboard in
        char_step = enigma.plugboard.get(char, char)
        step_detail['transformations'].append(('Plugboard (In)', char_step))
        
        # Forward through rotors
        char_step = enigma.rotors[2].forward(char_step)
        step_detail['transformations'].append((f'{rotor_types[2]} (Forward)', char_step))
        
        char_step = enigma.rotors[1].forward(char_step)
        step_detail['transformations'].append((f'{rotor_types[1]} (Forward)', char_step))
        
        char_step = enigma.rotors[0].forward(char_step)
        step_detail['transformations'].append((f'{rotor_types[0]} (Forward)', char_step))
        
        # Reflector
        char_step = enigma.reflector[ALPHABET.index(char_step)]
        step_detail['transformations'].append(('Reflector', char_step))
        
        # Backward through rotors
        char_step = enigma.rotors[0].backward(char_step)
        step_detail['transformations'].append((f'{rotor_types[0]} (Backward)', char_step))
        
        char_step = enigma.rotors[1].backward(char_step)
        step_detail['transformations'].append((f'{rotor_types[1]} (Backward)', char_step))
        
        char_step = enigma.rotors[2].backward(char_step)
        step_detail['transformations'].append((f'{rotor_types[2]} (Backward)', char_step))
        
        # Plugboard out
        char_step = enigma.plugboard.get(char_step, char_step)
        step_detail['transformations'].append(('Plugboard (Out)', char_step))
        
        step_detail['output'] = char_step
        steps.append(step_detail)
    
    return steps

# Streamlit UI
st.set_page_config(page_title="Enigma Machine Simulator", page_icon="🔐", layout="wide")

st.title("🔐 Enigma Machine Simulator")
st.markdown("### Experience the legendary WWII encryption device")

# Sidebar configuration
st.sidebar.header("⚙️ Machine Configuration")

st.sidebar.subheader("Rotor Selection")
rotor_left = st.sidebar.selectbox("Left Rotor", ["Rotor I", "Rotor II", "Rotor III"], index=0, key="rotor_left")
rotor_middle = st.sidebar.selectbox("Middle Rotor", ["Rotor I", "Rotor II", "Rotor III"], index=1, key="rotor_middle")
rotor_right = st.sidebar.selectbox("Right Rotor", ["Rotor I", "Rotor II", "Rotor III"], index=2, key="rotor_right")

rotor_types = [rotor_left, rotor_middle, rotor_right]

st.sidebar.subheader("Rotor Positions")
pos1 = st.sidebar.slider("Left Rotor Position", 0, 25, 0, key="pos1")
pos2 = st.sidebar.slider("Middle Rotor Position", 0, 25, 0, key="pos2")
pos3 = st.sidebar.slider("Right Rotor Position", 0, 25, 0, key="pos3")

st.sidebar.subheader("Plugboard Settings")
plugboard = st.sidebar.text_input(
    "Plugboard Pairs",
    "AB,CD",
    help="Enter letter pairs separated by commas (e.g., AB,CD,EF)"
)

# Display current rotor positions
st.sidebar.markdown("---")
st.sidebar.markdown("### 🎯 Current Rotor Positions")
col1, col2, col3 = st.sidebar.columns(3)
with col1:
    st.metric("Left", f"{ALPHABET[pos1]} ({pos1})")
with col2:
    st.metric("Middle", f"{ALPHABET[pos2]} ({pos2})")
with col3:
    st.metric("Right", f"{ALPHABET[pos3]} ({pos3})")

# Main tabs
tab1, tab2, tab3, tab4 = st.tabs(["🔒 Encrypt", "🔓 Decrypt", "🔍 Step-by-Step", "📚 How It Works"])

with tab1:
    st.header("Encryption")
    st.markdown("**Instructions:** Configure your machine in the sidebar, then enter your message below.")
    
    plaintext = st.text_area("Enter message to encrypt:", height=100, key="encrypt_input")
    
    if st.button("🔒 Encrypt Message", type="primary", key="encrypt_btn"):
        if plaintext:
            enigma = EnigmaMachine(rotor_types, [pos1, pos2, pos3], plugboard)
            ciphertext = enigma.encrypt(plaintext)
            
            st.success("✅ Encryption Complete!")
            st.code(ciphertext, language=None)
            
            st.info(f"**📋 To decrypt this message:**\n- Set rotors to: {rotor_left}, {rotor_middle}, {rotor_right}\n- Set positions to: {pos1}, {pos2}, {pos3}\n- Set plugboard to: {plugboard}\n- Paste the encrypted text in the Decrypt tab")
        else:
            st.warning("Please enter a message to encrypt.")

with tab2:
    st.header("Decryption")
    st.markdown("**Instructions:** Set the rotors and positions to match the sender's **initial settings**, then paste the encrypted message.")
    
    ciphertext_input = st.text_area("Enter encrypted message:", height=100, key="decrypt_input")
    
    if st.button("🔓 Decrypt Message", type="primary", key="decrypt_btn"):
        if ciphertext_input:
            enigma = EnigmaMachine(rotor_types, [pos1, pos2, pos3], plugboard)
            decrypted = enigma.encrypt(ciphertext_input)  # Enigma is reciprocal
            
            st.success("✅ Decryption Complete!")
            st.code(decrypted, language=None)
        else:
            st.warning("Please enter a message to decrypt.")

with tab3:
    st.header("Step-by-Step Encryption Visualization")
    st.markdown("**See the internal workings:** Watch how each letter travels through the Enigma machine.")
    
    step_text = st.text_input("Enter text to analyze:", "HELLO", key="step_input")
    
    if st.button("🔍 Show Step-by-Step", type="primary", key="step_btn"):
        if step_text:
            steps = encrypt_with_steps(rotor_types, [pos1, pos2, pos3], plugboard, step_text)
            
            for i, step in enumerate(steps):
                st.markdown(f"### Letter {i+1}: **{step['input']}** → **{step['output']}**")
                
                # Rotor positions
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.info(f"**Rotor Positions:**\n\n"
                           f"Before: {step['positions_before'][0]}, {step['positions_before'][1]}, {step['positions_before'][2]}\n\n"
                           f"After: {step['positions_after'][0]}, {step['positions_after'][1]}, {step['positions_after'][2]}")
                
                with col2:
                    st.markdown("**Signal Path:**")
                    for stage, char in step['transformations']:
                        st.text(f"  {stage:25s} → {char}")
                
                st.markdown("---")
        else:
            st.warning("Please enter text to analyze.")

with tab4:
    st.header("How the Enigma Machine Works")
    
    st.markdown("""
    ### 🎯 Overview
    The Enigma machine was used by Nazi Germany during World War II to encrypt military communications. 
    It's a electro-mechanical cipher device that uses rotating wheels called **rotors** to scramble messages.
    
    ### ⚙️ Components
    
    **1. Rotors (Wheels)**
    - Three rotors selected from available types (I, II, III)
    - Each rotor has unique internal wiring
    - Rotors rotate before encrypting each letter
    - Creates different substitution for the same letter each time
    
    **2. Reflector**
    - Bounces the signal back through the rotors
    - Makes Enigma **reciprocal**: same settings encrypt AND decrypt
    - If A→G when encrypting, then G→A with same settings
    
    **3. Plugboard (Steckerbrett)**
    - Swaps pairs of letters before and after rotor encryption
    - Adds extra security layer
    - Example: AB swaps A↔B, so A becomes B and B becomes A
    
    ### 🔄 Encryption Process
    
    1. **Rotor Stepping**: Right rotor advances before each letter (like an odometer)
    2. **Plugboard In**: Letter passes through plugboard first
    3. **Forward Path**: Signal goes through Right → Middle → Left rotor
    4. **Reflector**: Signal bounces back
    5. **Backward Path**: Signal returns through Left → Middle → Right rotor
    6. **Plugboard Out**: Letter passes through plugboard again
    7. **Output**: Final encrypted letter
    
    ### 🔐 Why It's Secure
    
    - **150 trillion possible settings** (rotor choice, positions, plugboard)
    - **Same letter encrypts differently** each time due to rotor rotation
    - **Reciprocal property** simplified communication (same settings for encrypt/decrypt)
    
    ### 💡 Breaking Enigma
    
    Allied cryptanalysts at Bletchley Park (led by Alan Turing) broke Enigma by:
    - Exploiting operator mistakes and patterns
    - Using the "Bombe" machine to test settings rapidly
    - Leveraging known plaintext (e.g., weather reports)
    
    ### 🎮 Try It Yourself!
    
    **Example Communication:**
    1. Set rotors to I, II, III with positions 0, 0, 0
    2. Encrypt "ATTACK AT DAWN" in the Encrypt tab
    3. Share the encrypted text with your friend
    4. They set the same settings and decrypt in the Decrypt tab
    5. Use Step-by-Step tab


                             """)
