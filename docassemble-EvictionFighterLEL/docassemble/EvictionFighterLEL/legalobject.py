from docassemble.base.core import DAObject, DAList
from docassemble.base.util import get_config
from docassemble.base.functions import word
from .airtable import Airtable

base_key = 'appA5wMpmdl4Vo8Kb'
api_key=get_config('airtable api key')

def object_from_a_id(a_id):
	funcobject = LegalObject()
	table_name = 'Elements'
	api_response = Airtable(base_key, table_name, api_key)
	el = api_response.get(a_id)
	if 'field' in el['fields']:
		funcobject.field = el['fields']['field']
	if 'label' in el['fields']:
		funcobject.name = el['fields']['label']
		funcobject.label = el['fields']['label']
	if 'typeofhousing' in el['fields']:
		funcobject.typeofhousing = el['fields']['typeofhousing']
	funcobject.id = el['id']
	if 'datatype' in el['fields']:
		funcobject.datatype = el['fields']['datatype']
	else:
		funcobject.datatype = 'yesno'
	if 'Active' in el['fields']:
		funcobject.active = el['fields']['Active']
	else:
		funcobject.active = False
	if 'pleadingsection' in el['fields']:
		funcobject.pleadingsection = el['fields']['pleadingsection']
	else:
		funcobject.pleadingsection = 'none'
	if 'help' in el['fields']:
		funcobject.help = el['fields']['help']
	if 'image' in el['fields']:
		funcobject.image = el['fields']['image']
	if 'default' in el['fields']:
		funcobject.default = el['fields']['default']
	if 'note' in el['fields']:
		funcobject.note = el['fields']['note']
	if 'children' in el['fields']:
		funcobject.childrenlist = el['fields']['children']
	if 'facts' in el['fields']:
		funcobject.factslist = el['fields']['facts']
	if 'parent' in el['fields']:
		funcobject.parent = el['fields']['parent']
	if 'question' in el['fields']:
		funcobject.question = el['fields']['question']
	if 'explanation' in el['fields']:
		funcobject.explanation = el['fields']['explanation']
	if 'explanationbottom' in el['fields']:
		funcobject.explanationbottom = el['fields']['explanationbottom']
	if 'explanationifmet' in el['fields']:
		funcobject.explanationifmet = el['fields']['explanationifmet']
	if 'explanationifnotmet' in el['fields']:
		funcobject.explanationifnotmet = el['fields']['explanationifnotmet']
	if 'follabel' in el['fields']:
		funcobject.initializeAttribute('facts', FactObjectList)
		funcobject.facts.label = el['fields']['follabel']
	if 'folhtml' in el['fields']:
	   funcobject.facts.html = el['fields']['folhtml']
	if 'folexplanation' in el['fields']:
		funcobject.facts.explanation = el['fields']['folexplanation']
	if 'folquestion' in el['fields']:
		funcobject.facts.question = el['fields']['folquestion']
	if 'comparisontype' in el['fields']:
		funcobject.facts.comparisontype = el['fields']['comparisontype']
	if 'title' in el['fields']:
		funcobject.title = el['fields']['title']
	if 'law' in el['fields']:
		funcobject.law = el['fields']['law']
	if 'conclusion' in el['fields']:
		funcobject.conclusion = el['fields']['conclusion']
	if 'strength' in el['fields']:
		funcobject.strength = el['fields']['strength']
	return funcobject

def fact_from_a_id(a_id):
	funcobject = FactObject()
	table_name = 'Facts'
	api_response = Airtable(base_key, table_name, api_key)
	el = api_response.get(a_id)
	funcobject.field = el['fields']['fieldold']
	funcobject.label = el['fields']['label']
	funcobject.id = el['id']
	funcobject.datatype = el['fields']['datatype']
	if 'help' in el['fields']:
		funcobject.help = el['fields']['help']
	if 'hint' in el['fields']:
		funcobject.hint = el['fields']['hint']
	if 'image' in el['fields']:
		funcobject.image = el['fields']['image']
	if 'default' in el['fields']:
		funcobject.default = el['fields']['default']
	if 'note' in el['fields']:
		funcobject.note = el['fields']['note']
	if 'parent' in el['fields']:
		funcobject.parent = el['fields']['parent'][0]
	if 'question' in el['fields']:
		funcobject.question = el['fields']['question']
	if 'explanation' in el['fields']:
		funcobject.explanation = el['fields']['explanation']
	if 'explanationbottom' in el['fields']:
		funcobject.explanationbottom = el['fields']['explanationbottom']
	if 'explanationifmet' in el['fields']:
		funcobject.explanationifmet = el['fields']['explanationifmet']
	if 'explanationifnotmet' in el['fields']:
		funcobject.explanationifnotmet = el['fields']['explanationifnotmet']
	if 'prefact' in el['fields']:
		funcobject.prefact = el['fields']['prefact']
	else:
		funcobject.prefact = ""
	if 'postfact' in el['fields']:
		funcobject.postfact = el['fields']['postfact']
	else:
		funcobject.postfact = ""
	if 'typeofevidence' in el['fields'] and not el['fields']['typeofevidence'] == 'NA':
		funcobject.initializeAttribute('evidence', EvidenceList.using(object_type=Evidence))
		funcobject.evidence.typeofevidence = el['fields']['typeofevidence']
		if 'evlabel' in el['fields']:
			funcobject.evidence.label = el['fields']['evlabel']
		else:
			funcobject.evidence.label = ""
		if 'evexplanation' in el['fields']:
			funcobject.evidence.explanation = el['fields']['evexplanation']
		else:
			funcobject.evidence.explanation = ""
		if 'evquestion' in el['fields']:
			funcobject.evidence.question = el['fields']['evquestion']
		else:
			funcobject.evidence.question = ""
		if 'typeofevidencedefault' in el['fields']:
			funcobject.evidence.typeofevidencedefault = el['fields']['typeofevidencedefault']
	return funcobject
	
class LegalObject(DAObject):
	def ___init___(self, *pargs, **kwargs):
		self.initializeAttribute('children', LegalObjectList.using(object_type=LegalObject))
		self.initializeAttribute('facts', FactObjectList.using(object_type=FactObject))
		return super(LegalObject, self).init(*pargs, **kwargs)

	def questioncode(self):
		questioncode = []
		for child in self.children:
			adict = {}
			adict[child.id] = child.label
			if hasattr(child,'help'):
				adict[u'help'] = child.help
			if hasattr(child,'default'):
				adict[u'default'] = child.default
			questioncode.append(adict)
		return questioncode
		
	def nested_explain(self):
		fr = ""
		fr = str(self.label)
		fr += "\n"
		if self.ismet:
			fr += str(self.explanationifmet)
		else:
			fr += str(self.explanationifnotmet)
		fr += "\n"
		if hasattr(self, 'facts'):
			self.facts.nested_fact()
		if hasattr(self, 'children'):
			for child in self.children:
				if child.isrelevant:
					child.nested_explain()
		return fr
  
class LegalObjectList(DAList):

	def is_met(self):
		if self.any_or_all == "Any":
			counter = 0
			for legalobject in self:
				if legalobject.ismet:
					return True
				if not legalobject.isrelevant:
					counter += 1
			if counter == len(self):
				return True
			return False
		else:
			counter = 0
			for legalobject in self:
				if legalobject.ismet:
					counter += 1
				else:
					return False
				if not legalobject.isrelevant and not legalobject.ismet:
					counter ++ 1
			if counter == len(self):
				return True
			return False


class FactObject(DAObject):
	def ___init___(self, *pargs, **kwargs):
 		self.initializeAttribute('children', LegalObjectList.using(object_type=LegalObject))
		return super(FactObject, self).init(*pargs, **kwargs)
		
	
class FactObjectList(DAList):

	def questioncode(self):
		questioncode = []
		for factt in self:
			adict = {}
			adict['field'] = factt.field
			adict['label'] = factt.label
			adict['datatype'] = factt.datatype
			if hasattr(factt,'help'):
				adict[u'help'] = factt.help
			if hasattr(factt,'hint'):
				adict[u'hint'] = factt.hint
			if hasattr(factt,'image'):
				adict[u'image'] = factt.image
			if hasattr(factt,'default'):
				adict[u'default'] = factt.default
			if hasattr(factt,'note'):
				adict[u'note'] = factt.note
			questioncode.append(adict)
		return questioncode
		
	def nested_fact(self):
		for fact in self:
			ff = fact.factstatement
			ff += "\n"
			if hasattr(self,'evidence'):
				ff += "You can prove this with "
				for ev in fact.evidence:
					if ev.typeofevidence == 'Documents':
						ff += str(ev.title)
					elif ev.typeofevidence == 'Testimony':
						ff += "your testimony."
					elif ev.typeofevidence == 'plaintiffevidence':
						ff += "Plaintiff's "
						if ev.paragraphOrExhibit == 'paragraph':
							ff += " Paragraph "
						else:
							ff += " Exhibit "
						ff += str(ev.poenumber)
				ff += "\n"
		if hasattr(self, 'children'):
			for child in self.children:
				if child.isrelevant:
					ff += child.nested_explain()
		return ff


class EvidenceList(DAList):
		
	pass

class Evidence(DAObject):
  
	pass

