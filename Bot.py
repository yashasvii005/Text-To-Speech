from gtts import gTTS
import os
import sys

def get_user_choice():
    while True:
        print("Choose input method:")
        print("1. Type text")
        print("2. Load from a text file")
        choice = input("Enter 1 or 2: ").strip()
        if choice in ('1', '2'):
            return choice
        print("Invalid choice. Please enter 1 or 2.\n")

def get_text_from_user():
    print("Enter the text you want to convert to speech (end with a blank line):")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    return "\n".join(lines)

def get_text_from_file():
    while True:
        path = input("Enter the path to your .txt file: ").strip().strip('"')
        if os.path.isfile(path):
            try:
                with open(path, encoding="utf-8") as f:
                    return f.read()
            except Exception as e:
                print(f"Error reading file: {e}")
        else:
            print("File not found! Please try again.\n")

def get_output_filename(default="output.mp3"):
    name = input(f"Enter the filename for output (default: {default}): ").strip()
    if not name:
        return default
    if not name.lower().endswith('.mp3'):
        name += ".mp3"
    return name

def main():
    print("=== Text-to-Speech (gTTS) Bot ===")
    choice = get_user_choice()
    if choice == '1':
        text = get_text_from_user()
    else:
        text = get_text_from_file()

    if not text.strip():
        print("No text to convert! Exiting.")
        sys.exit(1)

    out_file = get_output_filename()
    print("Generating speech... Please wait.")

    try:
        tts = gTTS(text)
        tts.save(out_file)
        print(f"\nAudio saved as '{out_file}'")
    except Exception as e:
        print("Error during conversion:", e)
        sys.exit(1)

    play_now = input("\nDo you want to play the audio now? (y/n): ").strip().lower()
    if play_now == 'y':
        try:
            if sys.platform.startswith('win'):
                os.startfile(out_file)
            elif sys.platform == 'darwin':
                os.system(f"open '{out_file}'")
            else:
                os.system(f"xdg-open '{out_file}'")
        except Exception:
            print("Failed to play audio automatically. Please open it manually.")

if __name__ == "__main__":
    main()
