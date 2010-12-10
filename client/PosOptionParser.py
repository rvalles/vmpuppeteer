from optparse import OptionParser, Option, IndentedHelpFormatter
#http://stackoverflow.com/questions/642648/how-do-i-format-positional-argument-help-using-pythons-optparse
class PosOptionParser(OptionParser):
	def format_help(self, formatter=None):
		class Positional(object):
			def __init__(self, args):
				self.option_groups = []
				self.option_list = args
		positional = Positional(self.positional)
		formatter = IndentedHelpFormatter()
		formatter.store_option_strings(positional)
		output = ['\n', formatter.format_heading("Positional Arguments")]
		formatter.indent()
		pos_help = [formatter.format_option(opt) for opt in self.positional]
		pos_help = [line.replace('--','') for line in pos_help]
		output += pos_help
		return OptionParser.format_help(self, formatter) + ''.join(output)
	def add_positional_argument(self, option):
		try:
			args = self.positional
		except AttributeError:
			args = []
			args.append(option)
			self.positional = args
	def set_out(self, out):
		self.out = out

