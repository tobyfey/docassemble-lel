# LEL Code
## Intro Blocks 
### Imports and Metadata

```python
from docassemble.base.core import DAObject, DAList
from docassemble.base.util import get_config
from docassemble.base.functions import word
from .airtable import Airtable
```

```yaml
metadata:
  title: Eviction Fighter
  short title: evictionfighter
---
modules:
  - docassemble.base.util
  - .airtable
  - .auth
  - .params
  - .legalobject
---
imports:
  - requests
  - yaml
  - json
---
```

### Variables 

```python
base_key = 'appA5wMpmdl4Vo8Kb'
api_key=get_config('airtable api key')
```

### Objects

```yaml
objects:
  - parentlegalobjects: LegalObjectList
  - relevantlegalobjects: LegalObjectList.using(object_type=LegalObject,auto_gather=False)
  - relevantnotmetlegalobjects: LegalObjectList
  - childrendict: DADict
---
generic object: LegalObject
objects:
  - x.children: LegalObjectList.using(object_type=LegalObject,auto_gather=False)
  - x.facts: FactObjectList.using(object_type=FactObject,auto_gather=False)
---
```

## Selecting Legal Action

```yaml
mandatory: True
code: |
  parentlegalobjects.auto_gather = False
  relevantlegalobjects.auto_gather = False
  if relevantlegalobject:
    relevantlegalobject.isrelevant = True
    relevantlegalobjects.append(relevantlegalobject,set_instance_name=True)
  relevantlegalobjects.gathered = True
---
```

```yaml
question: Type of Housing
field: typeofhousing
default: A1 Private Housing
choices:
  - A1 Private Housing
  - A2 Mobile Home Lot Rental
  - A3 Section 8 Certificates and Vouchers
  - A4 HUD Subsidized Projects
  - A5 Moderate Rehabilitation Projects
  - A6 Project-Based Certificate Projects
  - A7 Rural Housing Service Projects
  - A8 Public Housing
---
```

```yaml
question: What do you need help with?
fields:
  - I need help with: relevantlegalobject
    datatype: object
    choices: parentlegalobjects
---
mandatory: True
code: |
  base_key = 'appA5wMpmdl4Vo8Kb'
  table_name = 'Elements'
  api_key = get_config('airtable api key')
  api_response = Airtable(base_key, table_name, api_key)
  el = api_response.get_all(formula="and({parent} = 'parent', NOT({Active}=''))")
  counter = 0
  for child in el:
    funcobject = LegalObject()
    funcobject.instanceName = 'funcobject'
    funcobject.variablefield = el[counter]['fields']['field']
	  funcobject.name = el[counter]['fields']['label']
    funcobject.label = el[counter]['fields']['label']
    funcobject.id = el[counter]['id']
    if 'datatype' in el[counter]['fields']:
      funcobject.datatype = el[counter]['fields']['datatype']
	  if 'help' in el[counter]['fields']:
	    funcobject.help = el[counter]['fields']['help']
    if 'hint' in el[counter]['fields']:
	    funcobject.help = el[counter]['fields']['hint']
    if 'image' in el[counter]['fields']:
	    funcobject.image = el[counter]['fields']['image']
    if 'default' in el[counter]['fields']:
	    funcobject.default = el[counter]['fields']['default']
    if 'note' in el[counter]['fields']:
	    funcobject.note = el[counter]['fields']['note']
    if 'children' in el[counter]['fields']:
	    funcobject.childrenlist = el[counter]['fields']['children']
    if 'facts' in el[counter]['fields']:
	    funcobject.factslist = el[counter]['fields']['facts']
    if 'parent' in el[counter]['fields']:
	    funcobject.parent = el[counter]['fields']['parent'][0]
    if 'question' in el[counter]['fields']:
	    funcobject.question = el[counter]['fields']['question']
    if 'explanation' in el[counter]['fields']:
	    funcobject.explanation = el[counter]['fields']['explanation']
    if 'explanationbottom' in el[counter]['fields']:
	    funcobject.explanationbottom = el[counter]['fields']['explanationbottom']
    if 'explanationifmet' in el[counter]['fields']:
	    funcobject.explanationifmet = el[counter]['fields']['explanationifmet']
    if 'explanationifnotmet' in el[counter]['fields']:
	    funcobject.explanationifnotmet = el[counter]['fields']['explanationifnotmet']
    parentlegalobjects.append(funcobject,set_instance_name=True)
    counter += 1
  parentlegalobjects.gathered = True
---
```

## Building Children Elements

```python
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
	if 'follabel' in el['fields']:
		funcobject.initializeAttribute('facts', FactObjectList)
	if 'folhtml' in el['fields']:
	   funcobject.facts.html = el['fields']['folhtml']
	if 'follabel' in el['fields']:
		funcobject.facts.label = el['fields']['follabel']
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
	return funcobject
```

### Type Of Housing Filter

```yaml
generic object: LegalObject
code: |
  for atid in x.childrenlist:
    tempobject = object_from_a_id(atid)
    if tempobject.active:
      if typeofhousing in tempobject.typeofhousing:
        x.children.append(tempobject,set_instance_name=True)
  x.children.gathered = True
---
generic object: LegalObject
sets: 
  - x.facts
code: |
  if hasattr(x,'factslist'):
    x.facts.there_are_any = True
    for fid in x.factslist:
      x.facts.append(fact_from_a_id(fid),set_instance_name=True)
    x.facts.there_is_another = False
---
```

## Asking Which Children Elements Are Relevant

```yaml
generic object: LegalObject
question:  ${ x.label }
subquestion: |
  % if hasattr(x,'explanation'):
  ${ x.explanation }
  % endif
  
  % if hasattr(x,'question'):
  ${ x.question }
  % endif
  
fields:
  - no label: x.childrendict
    datatype: checkboxes
    code: x.questioncode()
---
```

## Not really sure what this does

```yaml
generic object: LegalObject
sets: x.children[0].isrelevant
code: |
  for chi in x.children:
    if x.childrendict[chi.id]:
      chi.isrelevant = False
    else:
      chi.isrelevant = True
---
```

## Setting ismet based on children and facts

```yaml
generic object: LegalObject
code: |
  if not hasattr(x, 'factslist') or x.facts.ismet:
    if not hasattr(x, 'childrenlist') or x.children.ismet:
      x.ismet = True
    else:
      x.ismet = False
	else:
		x.ismet = False
---
```

### .ismet based on any_or_all

```python
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
```

### ismet based on List

```yaml
generic object: LegalObjectList
code: |
  counter = 0
  for legalobject in x:
		if legalobject.isrelevant and not legalobject.ismet:
		  x.ismet = False
    else:
      counter += 1
  if counter == len(x):
    x.ismet = True
  else:
    x.ismet = False
	
---
```

### ismet in class?

```python
class LegalObject(DAObject):
	def ___init___(self, *pargs, **kwargs):
		self.initializeAttribute('children', LegalObjectList.using(object_type=LegalObject))
		self.initializeAttribute('facts', FactObjectList.using(object_type=FactObject))
		return super(LegalObject, self).init(*pargs, **kwargs)




	def is_met(self):
		if not hasattr(self, 'children') or self.children.ismet:
			if not hasattr(self, 'facts') or self.facts.ismet:
				return True
			else:
				return False
		else:
			return False

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
```

```python
class FactObject(DAObject):
	def ___init___(self, *pargs, **kwargs):
		self.initializeAttribute('children', LegalObjectList.using(object_type=LegalObject))
		return super(LegalObject, self).init(*pargs, **kwargs)

```

```python
def fact_from_a_id(a_id):
	funcobject = FactObject()
	table_name = 'Facts'
	api_response = Airtable(base_key, table_name, api_key)
	el = api_response.get(a_id)
	funcobject.field = el['fields']['field']
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
	if 'children' in el['fields']:
		funcobject.childrenlist = el['fields']['children']
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
	return funcobject
```


```yaml
generic object: FactObjectList
sets: x[0]
question:  ${ x.label }
subquestion: |
  ${ x.explanation }
  
  ${ x.question }

  % if hasattr(x,'html'):
  ${ x.html }
  % endif
  
  
fields:
  code: x.questioncode()
---
```

```python
class FactObjectList(DAList):

	def questioncode(self):
		questioncode = []
		for factt in self:
			adict = {}
			adict['field'] = factt.instanceName
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
		
	def is_met(self):
		if self.comparisontype == "Equals":
			if self[0].field == self[1].field:
				return True
			else:
				return False
		elif self.comparisontype == "AllTrue":
			for fact in self:
				if self.field == False:
					return False
				else:
					return True
		elif self.comparisontype == "CompareDate":
			if self[0].field.plus(days=3) < self[1].field:
				return True
			else:
				return False
```

```yaml
generic object: FactObjectList
sets:
  - x.ismet
code: |
  if x.comparisontype == "Equals":
		if x[0] == x[1]:
			x.ismet = True
		else:
			x.ismet = False
  if x.comparisontype == "2AllTrue":
    if x[0] and x[1]:
      x.ismet = False
    else:
      x.ismet = True
  if x.comparisontype == "1AllTrue":
    if x[0]:
      x.ismet = False
    else:
      x.ismet = True
  if x.comparisontype == "3AllTrue":
    if x[0] and x[1] and x[2]:
      x.ismet = False
    else:
      x.ismet = True
  if x.comparisontype == "4AnyTrue":
    if x[0] and x[1] and x[2] and x[3]:
      x.ismet = True
    else:
      x.ismet = False
  if x.comparisontype == "CompareDate":
    if x[0].plus(days=3) <= x[1]:
      x.ismet = True
    else:
      x.ismet = False
  if x.comparisontype == "CompareDateAmount":
    if x[0] >= x[2]:
      if x[1] >= x[3]:
        x.ismet = False
      else:
        x.ismet = True
    else:
      x.ismet = True
---
```

```yaml
question: Questions for the Caption
fields:
  - Name of Court in All Caps: courtNameAC
    default: Default Municipal Court
  - County in All Caps: countyAC
    default: BUTLER
  - Plaintiff: plaintiff
    default: Larry Landlord
  - Defendant: defendant
    default: Terry Tenant
  - Case Number: casenumber
    default: 18-CVG-99999
  - Judge: judge
    required: False
  - Title: title
    default: Answer
---
question: Questions for the Signature
fields:
  - Defendant street address: defendantstreetaddress
    default: 123 Main St.
  - Defendant City State Zip: defendantcitystatezip
    default: Default, OH 43611
  - Defendant Phone Number: defendantphonenumber
    required: False
  - Lawyer: lawyer
    default: Larry Lawyer
  - Lawyer street address: lawyerstreetaddress 
    default: 321 High St.
  - Lawyer City State Zip: lawyercitystatezip
    default: Suburbs, OH 43666
---
```

```python
class EvidenceList(DAList):
	def ___init___(self, *pargs, **kwargs):
		self.initializeAttribute('children', LegalObjectList.using(object_type=LegalObject))
		return super(LegalObject, self).init(*pargs, **kwargs)

```

```yaml
mandatory: True
question: Summary 
subquestion: |


  % for rlo in relevantlegalobjects:
  
  **${ rlo }**
  
  	% if rlo.ismet:
  
  		${ rlo.explanationifmet }
  
  		Here is an explanation of why the defenses you investigated in this interview will not prevent an eviction.
  
  		% if hasattr(rlo, 'children'):
  
  			% for rloc in rlo.children:
  
  				% if rloc.isrelevant:
  
  					${ rloc.explanationifmet }
  
  					% if hasattr(rloc, 'children'):
  
 						% for rlocc in rloc.children:
  
  							% if rlocc.isrelevant:
  
  								${ rlocc.explanationifmet }
  
							% endif  
  						% endfor
  					% endif
  				% endif
  			% endfor
  		% endif
  
  	% else:
  
  ${ rlo.explanationifnotmet }

  % if hasattr(rlo, 'children'):
  
  % for rloc in rlo.children:

  % if rloc.isrelevant:

  % if not rloc.ismet:
  
  ${ rloc.explanationifnotmet }
  
  % if hasattr(rloc, 'children'):
  
  % for rlocc in rloc.children:
  
  % if rlocc.isrelevant:
  
  % if not rlocc.ismet:
  
  1. ${ rlocc.explanationifnotmet }
  
  % endif
  % endif
  % endfor
  % endif
  % endif
  % endif
  % endfor
  % endif
  % endif
  % endfor
attachment:
  - name: Eviction Answer
    filename: EvictionAnswer
    content file:
      - answer.md
```

