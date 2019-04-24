
from pyvoce import SpeechInterface
import time
import sys

def synthesisTest():
	interface = SpeechInterface()

	interface.init('libraries\\voce-0.9.1\\lib', True, False, '', '')

	interface.synthesize('This is a speech synthesis test.')
	interface.synthesize('Type a message to hear it spoken aloud.')

	print("This is a speech synthesis test.  " 
		+ "Type a message to hear it spoken aloud.")
	print("Type 's' + 'enter' to make the "
		+ "synthesizer stop speaking.  Type 'q' + 'enter' to quit.")

	try:
		s = ""
		while not s == "q":
			# Read a line from keyboard.
			s = input()

			if s == "s":
				interface.stopSynthesizing()
			else:
				# Speak what was typed.
				interface.synthesize(s)

	except Exception:
		print("Error!", Exception)
		raise

	interface.destroy()


def recognitionTest():

	interface = SpeechInterface()
	interface.init("libraries\\voce-0.9.1\\lib", False, True, "libraries\\voce-0.9.1\\samples\\recognitionTest\\grammar", "digits")

	print("This is a speech recognition test. " 
		+ "Speak digits from 0-9 into the microphone. " 
		+ "Speak 'quit' to quit.")
	print("Enabledness: ", interface.isRecognizerEnabled())
	quit = False
	while not quit:
		# Normally, applications would do application-specific things 
		# here.  For this sample, we'll just sleep for a little bit.
		try:
			time.sleep(0.2)
		except Exception:
			print("Error!")
			raise

		while interface.getRecognizerQueueSize() > 0:
			s = interface.popRecognizedString()

			# Check if the string contains 'quit'.
			if "quit" in s:
				quit = true

			print("You said: " + s)
			# interface.synthesize(s)

	interface.destroy()

if __name__ == "__main__":
	print("Synthesis Test")
	synthesisTest()
	print("Recognition Test")
	recognitionTest()
