# pyVoce
# a wrapper, in python, for voce.
# this time, using py4j

from py4j.java_gateway import JavaGateway

# jpype.java.lang.System.out.println(1)


class SpeechInterface:
	# get voce in here
	
	def __init__(self, _classpath='.;.\\libraries\\voce-0.9.1\\lib\\voce.jar'):
		self.gateway = JavaGateway.launch_gateway(classpath=_classpath, die_on_exit=True)
		print("gateway Initialised!!!")
		self.jSpeechInterface = self.gateway.jvm.voce.SpeechInterface

	# @staticmethod
	def init(self, vocePath, initSynthesis, initRecognition, grammarPath,  grammarName):
		# define the classpath
		# classpath = "C:\\Users\\Taiwo\\Documents\\Olusegun\\work\\VoicePY\\voce-0.9.1\\lib"
		self.jSpeechInterface.init(vocePath, initSynthesis, initRecognition, grammarPath, grammarName)

	# @staticmethod
	def destroy(self):
		self.jSpeechInterface.destroy()
		self.gateway.close()
	"""
	args: {String: message}
	return: void
	"""
	# @staticmethod
	def synthesize(self, message):
		self.jSpeechInterface.synthesize(message)

	# @staticmethod
	def stopSynthesizing(self):
		self.jSpeechInterface.stopSynthesizing()

	# @staticmethod
	def getRecognizerQueueSize(self):
		return self.jSpeechInterface.getRecognizerQueueSize()

	# @staticmethod
	def popRecognizedString(self):
		return self.jSpeechInterface.popRecognizedString()

	# @staticmethod
	def setRecognizerEnabled(self, enabled):
		self.jSpeechInterface.setRecognizerEnabled(enabled)

	# @staticmethod
	def isRecognizerEnabled(self):
		return self.jSpeechInterface.isRecognizerEnabled()



import nussl

class SourceSeparation:
	'''
	this class in the pyvoce library uses nussl to implement audio source separation
	different results could be obtained as desired
	the goal is just to hava a single wrapper, so, it's all doable from within the same single package
	dasall
	so, it may end up being stripped down, just having specific functionalities from nussl

	need to define the methods to be implemented and the names to be used

	I could implement filters, which can be drawn by the user on the frontend
	
	this class is instantiated for each file.
	'''

	def __init__(self, _file_name='', _save_to_file=False, _num_sources=2):
		if not _file_name == '':
			self.file_name = _file_name
			self.audio_data = nussl.AudioSignal(self.file_name)
		self.save_to_file = _save_to_file
		self.num_sources = _num_sources

	def set_file(self, _file_name):
		self.file_name = _file_name
		self.audio_data = nussl.AudioSignal(self.file_name)

	def set_save_to_file(_save_to_file=True):
		self.save_to_file = _save_to_file

	def save_audio_to_file(self, audio_signals, output_folder=None, _stem=""):
		# save resulting audio signals to files and return a list of filenames
		# make a directory to store output if needed
		if output_folder == None:
			output_folder = os.path.join('..', 'output/')
		if not os.path.exists(output_folder):
			os.mkdir(output_folder)
	    # Create output file for each source found
		output_file_names = list()
		output_name_stem = os.path.join(output_folder, _stem)
		i = 1
		for s in audio_signals:
			output_file_name = output_name_stem + str(i) + '.wav'
			s.write_audio_to_file(output_file_name)
			output_file_names.append(output_file_name)
			i += 1
		return output_file_names

	def output_results(self, _audio_signals, _stem="output"):
		# depending on the settings, returns raw audio signals,
		# or saves and returns list of file names
		if self.save_to_file:
			return self.save_audio_to_file(_audio_signals, _stem)
		else:
			return _audio_signals
	
	def repet(self, exact_period=None, min_period=None, max_period=None):
		audio_data = self.audio_data
		if exact_period:
			repet = nussl.Repet(audio_data, period=exact_period)
		elif min_period and max_period:
			repet = nussl.Repet(audio_data, min_period=min_period, max_period=max_period)
		else:
			repet = nussl.Repet(audio_data)
		repet.run()
		return self.output_results(repet.make_audio_signals(), "repet")

	def repet_sim(self):
		audio_data = self.audio_data
		repet_sim = nussl.RepetSim(audio_data)
		repet_sim.run()
		return self.output_results(repet_sim.make_audio_signals(), "repet_sim")

	def hpss(self):
		audio_data = self.audio_data
		hpss = nussl.HPSS(audio_data)
		hpss.run()
		return self.output_results(hpss.make_audio_signals(), "hpss")

	def melodia(self):
		# this needs dependencies. I may just remove it, _jare_.
		audio_data = self.audio_data
		melodia = nussl.Melodia(audio_data)
		melodia.run()
		return self.output_results(melodia.make_audio_signals(), "melodia")

	def nmf_mfcc(self, _num_sources=None):
		if _num_sources is None:
			_num_sources = self.num_sources
		audio_data = self.audio_data
		nmf_mfcc = nussl.NMF_MFCC(audio_data, num_sources=_num_sources)
		masks = nmf_mfcc.run()
		return self.output_results(nmf_mfcc.make_audio_signals(), "nmf_mfcc")
		
	def plot(self, channel=None, x_label_time=True, title=None, file_path_name=None):
		self.audio_data.plot_time_domain(channel, x_label_time, title, file_path_name)

	def another_method(self):
		pass
